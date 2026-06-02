
import joblib
import pandas as pd
from django.shortcuts import render
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# ── Brand classifier ──────────────────────────────────────────────────────────
model     = joblib.load(BASE / 'laptop_model.pkl')
le_cpu    = joblib.load(BASE / 'cpu_encoder.pkl')
le_os     = joblib.load(BASE / 'os_encoder.pkl')
le_gfx    = joblib.load(BASE / 'gfx_encoder.pkl')
le_brand  = joblib.load(BASE / 'brand_encoder.pkl')

# ── Price regressor ───────────────────────────────────────────────────────────
price_model   = joblib.load(BASE / 'price_model.pkl')
p_le_brand    = joblib.load(BASE / 'price_brand_encoder.pkl')
p_le_cpu      = joblib.load(BASE / 'price_cpu_encoder.pkl')
p_le_os       = joblib.load(BASE / 'price_os_encoder.pkl')
p_le_gfx      = joblib.load(BASE / 'price_gfx_encoder.pkl')

CPU_CHOICES      = sorted(le_cpu.classes_.tolist())
OS_CHOICES       = sorted(le_os.classes_.tolist())
GRAPHICS_CHOICES = sorted(le_gfx.classes_.tolist())
BRAND_CHOICES    = sorted(p_le_brand.classes_.tolist())


def _safe_encode(encoder, value):
    """Encode a value; fall back to most-frequent class if unseen."""
    try:
        return encoder.transform([value])[0]
    except ValueError:
        return 0


def index(request):
    context = {
        'cpu_choices': CPU_CHOICES,
        'os_choices': OS_CHOICES,
        'graphics_choices': GRAPHICS_CHOICES,
    }
    if request.method == 'POST':
        try:
            price       = float(request.POST['price'])
            rating      = float(request.POST['rating'])
            screen_size = float(request.POST['screen_size'])
            storage_gb  = float(request.POST['storage_gb'])
            ram_gb      = float(request.POST['ram_gb'])
            cpu         = request.POST['cpu']
            os_val      = request.POST['os']
            graphics    = request.POST['graphics']

            df = pd.DataFrame([{
                'Price': price, 'Rating': rating, 'Screen_Size': screen_size,
                'Storage_GB': storage_gb, 'RAM_GB': ram_gb,
                'CPU': cpu, 'OS': os_val, 'Graphics': graphics
            }])
            df['CPU']      = le_cpu.transform(df['CPU'])
            df['OS']       = le_os.transform(df['OS'])
            df['Graphics'] = le_gfx.transform(df['Graphics'])

            pred  = model.predict(df)
            brand = le_brand.inverse_transform(pred)[0]

            proba      = model.predict_proba(df)[0]
            top3_idx   = proba.argsort()[-3:][::-1]
            top3       = [(le_brand.classes_[i], round(proba[i]*100, 1)) for i in top3_idx]

            context.update({
                'predicted_brand': brand,
                'top3': top3,
                'form_data': request.POST,
            })
        except Exception as e:
            context['error'] = str(e)

    return render(request, 'predictor/index.html', context)


def predict_price(request):
    context = {
        'brand_choices':    BRAND_CHOICES,
        'cpu_choices':      sorted(p_le_cpu.classes_.tolist()),
        'os_choices':       sorted(p_le_os.classes_.tolist()),
        'graphics_choices': sorted(p_le_gfx.classes_.tolist()),
    }
    if request.method == 'POST':
        try:
            brand       = request.POST['brand']
            rating      = float(request.POST['rating'])
            screen_size = float(request.POST['screen_size'])
            storage_gb  = float(request.POST['storage_gb'])
            ram_gb      = float(request.POST['ram_gb'])
            cpu         = request.POST['cpu']
            os_val      = request.POST['os']
            graphics    = request.POST['graphics']
            cpu_speed   = float(request.POST.get('cpu_speed', 2.4))
            total_sales = float(request.POST.get('total_sales', 30000))

            df = pd.DataFrame([{
                'Brand':       _safe_encode(p_le_brand, brand),
                'Rating':      rating,
                'Screen_Size': screen_size,
                'Storage_GB':  storage_gb,
                'RAM_GB':      ram_gb,
                'CPU':         _safe_encode(p_le_cpu, cpu),
                'OS':          _safe_encode(p_le_os, os_val),
                'Graphics':    _safe_encode(p_le_gfx, graphics),
                'CPU_Speed':   cpu_speed,
                'Total_Sales': total_sales,
            }])

            predicted_price = price_model.predict(df)[0]

            context.update({
                'predicted_price':     round(predicted_price, 2),
                'predicted_price_fmt': f"{predicted_price:,.0f}",
                'form_data':           request.POST,
            })
        except Exception as e:
            context['error'] = str(e)

    return render(request, 'predictor/price.html', context)


DESIGN_PATTERNS = [
    {
        'number': 1,
        'category': 'Creational',
        'category_color': 'blue',
        'name': 'Singleton',
        'icon': 'fa-circle-dot',
        'class_name': 'ModelRepository',
        'purpose': 'Ensures only ONE instance manages all .pkl model files across the entire app.',
        'used_in': 'pipeline.py → ModelRepository.__new__',
        'code_snippet': '_instance = None\ndef __new__(cls):\n    if cls._instance is None:\n        cls._instance = super().__new__(cls)\n    return cls._instance',
    },
    {
        'number': 2,
        'category': 'Creational',
        'category_color': 'blue',
        'name': 'Factory Method',
        'icon': 'fa-industry',
        'class_name': 'CleanerFactory',
        'purpose': 'Creates the correct dataset cleaner (Amazon or Messy) based on a source string — caller never instantiates directly.',
        'used_in': 'pipeline.py → CleanerFactory.create("amazon" | "messy")',
        'code_snippet': '@staticmethod\ndef create(source: str) -> BaseCleaner:\n    if source == "amazon": return AmazonCleaner(...)\n    elif source == "messy": return MessyCleaner(...)',
    },
    {
        'number': 3,
        'category': 'Creational',
        'category_color': 'blue',
        'name': 'Builder',
        'icon': 'fa-cubes',
        'class_name': 'ModelBuilder',
        'purpose': 'Constructs a RandomForestClassifier step-by-step with a fluent interface — separates construction from representation.',
        'used_in': 'pipeline.py → ModelBuilder().set_estimators(200).set_depth(20).build()',
        'code_snippet': 'ModelBuilder()\n  .set_estimators(200)\n  .set_depth(20)\n  .set_seed(42)\n  .build()',
    },
    {
        'number': 4,
        'category': 'Structural',
        'category_color': 'orange',
        'name': 'Adapter',
        'icon': 'fa-plug',
        'class_name': 'DatasetAdapter',
        'purpose': 'Bridges the Amazon CSV schema (lowercase cols) to the unified schema (Title case) so both datasets can be merged seamlessly.',
        'used_in': 'pipeline.py → DatasetAdapter.adapt(df1) + DatasetAdapter.merge(df1, df2)',
        'code_snippet': 'COLUMN_MAP = {"brand":"Brand", "ram_gb":"RAM_GB", ...}\n@staticmethod\ndef adapt(df): return df.rename(columns=COLUMN_MAP)',
    },
    {
        'number': 5,
        'category': 'Structural',
        'category_color': 'orange',
        'name': 'Facade',
        'icon': 'fa-mask',
        'class_name': 'LaptopPredictor',
        'purpose': 'Exposes a single predict() method that hides all complexity — loading model, encoding inputs, running inference, decoding output.',
        'used_in': 'pipeline.py → LaptopPredictor().predict(price, rating, ...)',
        'code_snippet': 'class LaptopPredictor:\n    def predict(self, price, rating, ...):\n        # encode → infer → decode\n        return brand_name',
    },
    {
        'number': 6,
        'category': 'Structural',
        'category_color': 'orange',
        'name': 'Decorator',
        'icon': 'fa-layer-group',
        'class_name': 'LoggingCleaner',
        'purpose': 'Wraps any BaseCleaner and adds timing + logging behaviour without modifying the original cleaner class.',
        'used_in': 'pipeline.py → LoggingCleaner(CleanerFactory.create("amazon"))',
        'code_snippet': 'class LoggingCleaner(BaseCleaner):\n    def run(self):\n        start = time.time()\n        self._wrapped.run()\n        print(f"Done in {time.time()-start:.2f}s")',
    },
    {
        'number': 7,
        'category': 'Behavioral',
        'category_color': 'green',
        'name': 'Strategy',
        'icon': 'fa-chess',
        'class_name': 'CurrencyStrategy / StorageStrategy / RamStrategy / ScreenSizeStrategy',
        'purpose': 'Pluggable column-cleaning algorithms — each strategy handles one data type. Swap strategies without changing the cleaner.',
        'used_in': 'pipeline.py → CurrencyStrategy().clean(val), StorageStrategy().clean(val)',
        'code_snippet': 'class CurrencyStrategy(CleaningStrategy):\n    def clean(self, val):\n        v = re.sub(r"[₹$,]", "", val)\n        return float(v)',
    },
    {
        'number': 8,
        'category': 'Behavioral',
        'category_color': 'green',
        'name': 'Observer',
        'icon': 'fa-bell',
        'class_name': 'PipelineEventBus / ConsoleLogger / AccuracyTracker',
        'purpose': 'Pipeline stages publish events; observers (ConsoleLogger, AccuracyTracker) react automatically — decoupled notification system.',
        'used_in': 'pipeline.py → bus.notify("training", {"accuracy": acc})',
        'code_snippet': 'bus.subscribe(ConsoleLogger())\nbus.subscribe(AccuracyTracker())\n# later...\nbus.notify("training", {"accuracy": 89.2})',
    },
    {
        'number': 9,
        'category': 'Behavioral',
        'category_color': 'green',
        'name': 'Command',
        'icon': 'fa-terminal',
        'class_name': 'CleanCommand / TrainCommand / SaveCommand',
        'purpose': 'Each pipeline stage is encapsulated as a command object with execute(). Enables queuing, logging, and potential undo support.',
        'used_in': 'pipeline.py → CleanCommand(cleaner).execute(), TrainCommand(df, bus).execute()',
        'code_snippet': 'CleanCommand(c1).execute()   # clean\nTrainCommand(df, bus).execute()  # train\nSaveCommand(model, enc).execute()  # save',
    },
    {
        'number': 10,
        'category': 'Behavioral',
        'category_color': 'green',
        'name': 'Template Method',
        'icon': 'fa-file-code',
        'class_name': 'AmazonCleaner / MessyCleaner',
        'purpose': 'BaseCleaner defines the skeleton (clean_columns → impute_missing → select_features). Subclasses fill in the dataset-specific steps.',
        'used_in': 'pipeline.py → AmazonCleaner.run(), MessyCleaner.run()',
        'code_snippet': 'class BaseCleaner:\n    def run(self):  # template\n        self.clean_columns()\n        self.impute_missing()\n        self.select_features()',
    },
]


def patterns(request):
    creational  = [p for p in DESIGN_PATTERNS if p['category'] == 'Creational']
    structural  = [p for p in DESIGN_PATTERNS if p['category'] == 'Structural']
    behavioral  = [p for p in DESIGN_PATTERNS if p['category'] == 'Behavioral']
    return render(request, 'predictor/patterns.html', {
        'patterns': DESIGN_PATTERNS,
        'creational': creational,
        'structural': structural,
        'behavioral': behavioral,
    })
