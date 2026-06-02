import pandas as pd
import numpy as np
import re
import joblib
from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


# =============================================================
# CREATIONAL PATTERNS
# =============================================================

# -------------------------------------------------------------
# 1. SINGLETON PATTERN
#    ModelRepository — only ONE instance manages all .pkl files
# -------------------------------------------------------------
class ModelRepository:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.paths = {
                'model': 'laptop_model.pkl',
                'cpu':   'cpu_encoder.pkl',
                'os':    'os_encoder.pkl',
                'gfx':   'gfx_encoder.pkl',
                'brand': 'brand_encoder.pkl',
            }
        return cls._instance

    def save(self, model, encoders):
        joblib.dump(model, self.paths['model'])
        for key, enc in encoders.items():
            joblib.dump(enc, self.paths[key])
        print("[Repository] All artifacts saved.")

    def load(self):
        model = joblib.load(self.paths['model'])
        encoders = {k: joblib.load(p) for k, p in self.paths.items() if k != 'model'}
        return model, encoders


# -------------------------------------------------------------
# 2. FACTORY METHOD PATTERN
#    CleanerFactory — creates the right cleaner based on source
# -------------------------------------------------------------
class BaseCleaner(ABC):
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.df = None

    @abstractmethod
    def clean_columns(self): pass

    @abstractmethod
    def impute_missing(self): pass

    @abstractmethod
    def select_features(self): pass

    def run(self):
        self.df = pd.read_csv(self.input_file)
        self.clean_columns()
        self.impute_missing()
        self.select_features()
        self.df.to_csv(self.output_file, index=False)
        print(f"[Cleaner] Saved: {self.output_file}")
        return self.df


class CleanerFactory:
    @staticmethod
    def create(source: str) -> BaseCleaner:
        if source == 'amazon':
            return AmazonCleaner(
                'amazon_laptop_prices_v01 (1).csv',
                'cleaned_amazon_laptop_prices.csv'
            )
        elif source == 'messy':
            return MessyCleaner(
                'single_amazon_laptop_messy_dataset_1-10.csv',
                'cleaned_messy_laptop_data_v2.csv'
            )
        raise ValueError(f"Unknown source: {source}")


# -------------------------------------------------------------
# 3. BUILDER PATTERN
#    ModelBuilder — step-by-step construction of the RF model
# -------------------------------------------------------------
class ModelBuilder:
    def __init__(self):
        self._n_estimators = 100
        self._max_depth = None
        self._random_state = 42

    def set_estimators(self, n):
        self._n_estimators = n
        return self

    def set_depth(self, depth):
        self._max_depth = depth
        return self

    def set_seed(self, seed):
        self._random_state = seed
        return self

    def build(self):
        return RandomForestClassifier(
            n_estimators=self._n_estimators,
            max_depth=self._max_depth,
            random_state=self._random_state
        )



# =============================================================
# STRUCTURAL PATTERNS
# =============================================================

# -------------------------------------------------------------
# 4. ADAPTER PATTERN
#    DatasetAdapter — bridges Amazon schema to unified schema
# -------------------------------------------------------------
class DatasetAdapter:
    COLUMN_MAP = {
        'brand': 'Brand', 'rating': 'Rating',
        'screen_size_inches': 'Screen_Size', 'harddisk_gb': 'Storage_GB',
        'ram_gb': 'RAM_GB', 'cpu': 'CPU', 'OS': 'OS', 'graphics': 'Graphics'
    }
    COMMON = ['Brand', 'Price', 'Rating', 'Screen_Size', 'Storage_GB', 'RAM_GB', 'CPU', 'OS', 'Graphics']

    @staticmethod
    def adapt(df):
        return df.rename(columns=DatasetAdapter.COLUMN_MAP)

    @staticmethod
    def merge(df1, df2):
        df1 = DatasetAdapter.adapt(df1)
        cols = [c for c in DatasetAdapter.COMMON if c in df1.columns and c in df2.columns]
        return pd.concat([df1[cols], df2[cols]], ignore_index=True)


# -------------------------------------------------------------
# 5. FACADE PATTERN
#    LaptopPredictor — single predict() hides all complexity
# -------------------------------------------------------------
class LaptopPredictor:
    def __init__(self):
        self._model, self._encoders = ModelRepository().load()

    def predict(self, price, rating, screen_size, storage_gb, ram_gb, cpu, os, graphics):
        df = pd.DataFrame([{
            'Price': price, 'Rating': rating, 'Screen_Size': screen_size,
            'Storage_GB': storage_gb, 'RAM_GB': ram_gb,
            'CPU': cpu, 'OS': os, 'Graphics': graphics
        }])
        df['CPU']      = self._encoders['cpu'].transform(df['CPU'])
        df['OS']       = self._encoders['os'].transform(df['OS'])
        df['Graphics'] = self._encoders['gfx'].transform(df['Graphics'])
        pred = self._model.predict(df)
        return self._encoders['brand'].inverse_transform(pred)[0]


# -------------------------------------------------------------
# 6. DECORATOR PATTERN
#    LoggingCleaner — wraps any cleaner and logs timing
# -------------------------------------------------------------
import time

class LoggingCleaner(BaseCleaner):
    def __init__(self, wrapped: BaseCleaner):
        self._wrapped = wrapped

    def clean_columns(self):
        self._wrapped.clean_columns()

    def impute_missing(self):
        self._wrapped.impute_missing()

    def select_features(self):
        self._wrapped.select_features()

    def run(self):
        start = time.time()
        print(f"[Decorator] Starting: {self._wrapped.__class__.__name__}")
        self._wrapped.df = pd.read_csv(self._wrapped.input_file)
        self._wrapped.clean_columns()
        self._wrapped.impute_missing()
        self._wrapped.select_features()
        self._wrapped.df.to_csv(self._wrapped.output_file, index=False)
        elapsed = time.time() - start
        print(f"[Decorator] Done in {elapsed:.2f}s → {self._wrapped.output_file}")
        return self._wrapped.df



# =============================================================
# BEHAVIORAL PATTERNS
# =============================================================

# -------------------------------------------------------------
# 7. STRATEGY PATTERN
#    Pluggable column-cleaning strategies
# -------------------------------------------------------------
class CleaningStrategy(ABC):
    @abstractmethod
    def clean(self, val): pass

class CurrencyStrategy(CleaningStrategy):
    def clean(self, val):
        if isinstance(val, str):
            v = re.sub(r'[₹$,.\s]', '', val)
            try: return float(v)
            except: return np.nan
        return val

class StorageStrategy(CleaningStrategy):
    def clean(self, val):
        if pd.isna(val) or not isinstance(val, str): return np.nan
        val = val.lower()
        m = re.search(r'(\d+\.?\d*)\s*(gb|tb|mb)?', val)
        if not m: return np.nan
        n, u = float(m.group(1)), m.group(2)
        return n * 1024 if u == 'tb' else n / 1024 if u == 'mb' else n

class RamStrategy(CleaningStrategy):
    def clean(self, val):
        if pd.isna(val) or not isinstance(val, str): return np.nan
        val = val.lower()
        m = re.search(r'(\d+\.?\d*)\s*(gb|mb)?', val)
        if not m: return np.nan
        n = float(m.group(1))
        return n / 1024 if m.group(2) == 'mb' else n

class ScreenSizeStrategy(CleaningStrategy):
    def clean(self, val):
        if pd.isna(val) or not isinstance(val, str): return np.nan
        val = val.lower()
        m = re.search(r'(\d+\.?\d*)', val)
        if not m: return np.nan
        n = float(m.group(1))
        return round(n / 2.54, 1) if 'cm' in val or 'centimetre' in val else n


# -------------------------------------------------------------
# 8. OBSERVER PATTERN
#    PipelineEventBus — stages notify listeners on completion
# -------------------------------------------------------------
class PipelineObserver(ABC):
    @abstractmethod
    def on_stage_complete(self, stage: str, info: dict): pass

class ConsoleLogger(PipelineObserver):
    def on_stage_complete(self, stage, info):
        print(f"[Observer] Stage '{stage}' complete → {info}")

class AccuracyTracker(PipelineObserver):
    def on_stage_complete(self, stage, info):
        if 'accuracy' in info:
            print(f"[Tracker] Model accuracy recorded: {info['accuracy']:.2f}%")

class PipelineEventBus:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer: PipelineObserver):
        self._observers.append(observer)

    def notify(self, stage: str, info: dict):
        for obs in self._observers:
            obs.on_stage_complete(stage, info)


# -------------------------------------------------------------
# 9. COMMAND PATTERN
#    Each pipeline stage is a command — execute / undo support
# -------------------------------------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self): pass

class CleanCommand(Command):
    def __init__(self, cleaner: BaseCleaner):
        self._cleaner = cleaner

    def execute(self):
        return self._cleaner.run()

class TrainCommand(Command):
    def __init__(self, df, bus: PipelineEventBus):
        self._df = df
        self._bus = bus

    def execute(self):
        df = self._df.copy()
        df['Brand'] = df['Brand'].str.strip().str.title()
        counts = df['Brand'].value_counts()
        df = df[df['Brand'].isin(counts[counts >= 5].index)]

        encoders = {
            'cpu':   LabelEncoder(),
            'os':    LabelEncoder(),
            'gfx':   LabelEncoder(),
            'brand': LabelEncoder(),
        }
        df['CPU']      = encoders['cpu'].fit_transform(df['CPU'].astype(str))
        df['OS']       = encoders['os'].fit_transform(df['OS'].astype(str))
        df['Graphics'] = encoders['gfx'].fit_transform(df['Graphics'].astype(str))

        X = df.drop('Brand', axis=1)
        y = encoders['brand'].fit_transform(df['Brand'])

        model = (ModelBuilder()
                 .set_estimators(200)
                 .set_depth(20)
                 .set_seed(42)
                 .build())

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test)) * 100
        print(f"[Train] Accuracy: {acc:.2f}%")

        self._bus.notify('training', {'accuracy': acc, 'samples': len(df)})
        return model, encoders

class SaveCommand(Command):
    def __init__(self, model, encoders):
        self._model = model
        self._encoders = encoders

    def execute(self):
        ModelRepository().save(self._model, self._encoders)


# -------------------------------------------------------------
# 10. TEMPLATE METHOD PATTERN
#     AmazonCleaner / MessyCleaner — same skeleton, diff steps
# -------------------------------------------------------------
class AmazonCleaner(BaseCleaner):
    def clean_columns(self):
        self.df['Price']            = self.df['Price'].apply(CurrencyStrategy().clean)
        self.df['screen_size_inches'] = self.df['screen_size'].apply(ScreenSizeStrategy().clean)
        self.df['harddisk_gb']      = self.df['harddisk'].apply(StorageStrategy().clean)
        self.df['ram_gb']           = self.df['ram'].apply(RamStrategy().clean)

    def impute_missing(self):
        for col in ['screen_size_inches', 'harddisk_gb', 'ram_gb', 'rating', 'Price']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].median())
        for col in ['brand', 'cpu', 'OS', 'graphics']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('Unknown')

    def select_features(self):
        self.df = self.df.drop(columns=['screen_size', 'harddisk', 'ram'], errors='ignore')


class MessyCleaner(BaseCleaner):
    def clean_columns(self):
        self.df['price_cleaned']      = self.df['price'].apply(CurrencyStrategy().clean)
        self.df['screen_size_inches'] = self.df['screen_size'].apply(ScreenSizeStrategy().clean)
        self.df['hard_disk_gb']       = self.df['hard_disk_size'].apply(StorageStrategy().clean)
        self.df['ram_gb']             = self.df['ram'].str.extract(r'(\d+)').astype(float)

    def impute_missing(self):
        for col in ['rating', 'price_cleaned', 'screen_size_inches', 'hard_disk_gb', 'ram_gb']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(self.df[col].median())
        for col in ['brand', 'cpu_model', 'os', 'graphics_card']:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna('Unknown')

    def select_features(self):
        mapping = {
            'brand': 'Brand', 'rating': 'Rating', 'price_cleaned': 'Price',
            'screen_size_inches': 'Screen_Size', 'hard_disk_gb': 'Storage_GB',
            'cpu_model': 'CPU', 'ram_gb': 'RAM_GB', 'os': 'OS', 'graphics_card': 'Graphics'
        }
        available = {k: v for k, v in mapping.items() if k in self.df.columns}
        self.df = self.df[list(available.keys())].rename(columns=available)



# =============================================================
# PIPELINE ORCHESTRATOR — wires all patterns together
# =============================================================
class MLPipeline:
    def __init__(self):
        self.bus = PipelineEventBus()
        self.bus.subscribe(ConsoleLogger())
        self.bus.subscribe(AccuracyTracker())

    def run(self):
        # --- Stage 1: Clean (Factory + Decorator + Command) ---
        print("\n=== Stage 1: Cleaning ===")
        c1 = LoggingCleaner(CleanerFactory.create('amazon'))
        c2 = LoggingCleaner(CleanerFactory.create('messy'))
        df1 = CleanCommand(c1).execute()
        df2 = CleanCommand(c2).execute()
        self.bus.notify('cleaning', {'files': 2})

        # --- Stage 2: Adapt + Merge (Adapter) ---
        print("\n=== Stage 2: Merging ===")
        df_combined = DatasetAdapter.merge(df1, df2)
        df_combined.to_csv('final_combined_laptop_data.csv', index=False)
        self.bus.notify('merging', {'rows': len(df_combined)})

        # --- Stage 3: Train (Builder + Command + Observer) ---
        print("\n=== Stage 3: Training ===")
        model, encoders = TrainCommand(df_combined, self.bus).execute()

        # --- Stage 4: Save (Repository + Command) ---
        print("\n=== Stage 4: Saving ===")
        SaveCommand(model, encoders).execute()
        self.bus.notify('saving', {'status': 'done'})

    def predict(self, **kwargs):
        print("\n=== Prediction (Facade) ===")
        result = LaptopPredictor().predict(**kwargs)
        print(f"Predicted Brand: {result}")
        return result


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == '__main__':
    pipeline = MLPipeline()
    pipeline.run()

    pipeline.predict(
        price=61000, rating=4.3, screen_size=14.0,
        storage_gb=512, ram_gb=16,
        cpu='Intel Core i5', os='Windows 10', graphics='Integrated'
    )
