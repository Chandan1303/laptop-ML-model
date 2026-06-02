import pandas as pd
import joblib
import numpy as np
import re
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ── Load raw dataset ──────────────────────────────────────────────────────────
df = pd.read_csv('amazon_laptop_prices_v01 (1).csv')

USD_TO_INR = 83.5

# ── Parse Price ───────────────────────────────────────────────────────────────
def parse_price(val):
    cleaned = re.sub(r'[^\d.]', '', str(val))
    try: return float(cleaned) * USD_TO_INR
    except: return np.nan

df['Price'] = df['Price'].apply(parse_price)
df = df.dropna(subset=['Price'])

# ── Parse screen size ─────────────────────────────────────────────────────────
def parse_screen(val):
    if pd.isna(val): return np.nan
    m = re.search(r'(\d+\.?\d*)', str(val))
    return float(m.group(1)) if m else np.nan

df['Screen_Size'] = df['screen_size'].apply(parse_screen)

# ── Parse storage ─────────────────────────────────────────────────────────────
def parse_storage(val):
    if pd.isna(val) or not isinstance(val, str): return np.nan
    v = val.lower()
    m = re.search(r'(\d+\.?\d*)\s*(tb|gb|mb)?', v)
    if not m: return np.nan
    n, u = float(m.group(1)), m.group(2)
    return n * 1024 if u == 'tb' else n / 1024 if u == 'mb' else n

df['Storage_GB'] = df['harddisk'].apply(parse_storage)

# ── Parse RAM ─────────────────────────────────────────────────────────────────
def parse_ram(val):
    if pd.isna(val): return np.nan
    m = re.search(r'(\d+)', str(val))
    return float(m.group(1)) if m else np.nan

df['RAM_GB'] = df['ram'].apply(parse_ram)

# ── Parse CPU speed (GHz) ─────────────────────────────────────────────────────
def parse_cpu_speed(val):
    if pd.isna(val): return np.nan
    m = re.search(r'(\d+\.?\d*)', str(val))
    return float(m.group(1)) if m else np.nan

df['CPU_Speed'] = df['cpu_speed'].apply(parse_cpu_speed)

# ── Total Sales (strong price proxy) ─────────────────────────────────────────
df['Total_Sales'] = pd.to_numeric(df['Total Sales'], errors='coerce')

# ── Normalize brand names ─────────────────────────────────────────────────────
brand_map = {
    'dell': 'Dell', 'hp': 'HP', 'lenovo': 'Lenovo', 'acer': 'Acer',
    'asus': 'Asus', 'msi': 'MSI', 'samsung': 'Samsung', 'lg': 'LG',
    'microsoft': 'Microsoft', 'apple': 'Apple', 'alienware': 'Alienware',
    'razer': 'Razer', 'gigabyte': 'Gigabyte', 'panasonic': 'Panasonic',
    'toughbook': 'Toughbook', 'rokc': 'Rokc',
}
df['Brand'] = df['brand'].str.strip().str.lower().map(brand_map)
df = df.dropna(subset=['Brand'])

# ── Fill missing categoricals ─────────────────────────────────────────────────
df['cpu']      = df['cpu'].fillna('Unknown').str.strip()
df['OS']       = df['OS'].fillna('Unknown').str.strip()
df['graphics'] = df['graphics'].fillna('Unknown').str.strip()
df['rating']   = pd.to_numeric(df['rating'], errors='coerce')

# ── Fill missing numerics with per-brand median ───────────────────────────────
for col in ['Screen_Size', 'Storage_GB', 'RAM_GB', 'rating', 'CPU_Speed', 'Total_Sales']:
    df[col] = df.groupby('Brand')[col].transform(lambda x: x.fillna(x.median()))
    df[col] = df[col].fillna(df[col].median())  # fallback global median

# ── Keep brands with >= 10 samples ───────────────────────────────────────────
counts = df['Brand'].value_counts()
df = df[df['Brand'].isin(counts[counts >= 10].index)].copy()

# ── Remove per-brand price outliers (2%–98%) ─────────────────────────────────
def clip_outliers(group):
    lo = group['Price'].quantile(0.02)
    hi = group['Price'].quantile(0.98)
    return group[(group['Price'] >= lo) & (group['Price'] <= hi)]

df = df.groupby('Brand', group_keys=False).apply(clip_outliers).reset_index(drop=True)

print(f"Samples: {len(df)}")
print(f"Brands:  {sorted(df['Brand'].unique())}")
print(f"Price range: Rs. {df['Price'].min():,.0f} – Rs. {df['Price'].max():,.0f}")
print("\nMean price per brand:")
print(df.groupby('Brand')['Price'].mean()
        .sort_values(ascending=False)
        .apply(lambda x: f"Rs. {x:,.0f}").to_string())

# ── Encode categoricals ───────────────────────────────────────────────────────
le_brand_p = LabelEncoder()
le_cpu_p   = LabelEncoder()
le_os_p    = LabelEncoder()
le_gfx_p   = LabelEncoder()

df['Brand']    = le_brand_p.fit_transform(df['Brand'].astype(str))
df['cpu']      = le_cpu_p.fit_transform(df['cpu'].astype(str))
df['OS']       = le_os_p.fit_transform(df['OS'].astype(str))
df['graphics'] = le_gfx_p.fit_transform(df['graphics'].astype(str))

features = ['Brand', 'rating', 'Screen_Size', 'Storage_GB', 'RAM_GB',
            'cpu', 'OS', 'graphics', 'CPU_Speed', 'Total_Sales']
X = df[features].copy()
X.columns = ['Brand', 'Rating', 'Screen_Size', 'Storage_GB', 'RAM_GB',
             'CPU', 'OS', 'Graphics', 'CPU_Speed', 'Total_Sales']
y = df['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,
    min_samples_leaf=3,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
print(f"\nMAE:  Rs. {mae:,.0f}")
print(f"R2:   {r2:.3f}")
print(f"MAPE: {mape:.1f}%")

imp = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
print("\nFeature importances:")
print(imp.sort_values('Importance', ascending=False).to_string(index=False))

# ── Sanity checks ─────────────────────────────────────────────────────────────
print("\n--- Sanity checks ---")
tests = [
    ('Apple',    8,  256, 13.3, 4.8, 'Unknown',       'Mac OS',          'Integrated', 3.5, 50000),
    ('Dell',     8,  512, 15.6, 4.2, 'Intel Core i5', 'Windows 11 Home', 'Integrated', 2.4, 30000),
    ('Lenovo',  16,  512, 14.0, 4.3, 'Intel Core i7', 'Windows 11 Pro',  'Dedicated',  2.8, 40000),
    ('MSI',     32, 1000, 15.6, 4.6, 'Intel Core i9', 'Windows 11 Home', 'Dedicated',  5.0, 25000),
    ('HP',       8,  256, 15.6, 4.0, 'Intel Core i3', 'Windows 11 Home', 'Integrated', 1.2, 20000),
]
for brand, ram, storage, screen, rating, cpu, os_val, gfx, cpu_spd, sales in tests:
    def enc(encoder, val):
        return encoder.transform([val])[0] if val in encoder.classes_ else 0
    row = pd.DataFrame([{
        'Brand': enc(le_brand_p, brand), 'Rating': rating, 'Screen_Size': screen,
        'Storage_GB': storage, 'RAM_GB': ram,
        'CPU': enc(le_cpu_p, cpu), 'OS': enc(le_os_p, os_val),
        'Graphics': enc(le_gfx_p, gfx), 'CPU_Speed': cpu_spd, 'Total_Sales': sales
    }])
    pred = model.predict(row)[0]
    print(f"  {brand:10} {ram:3}GB  {cpu[:18]:18}  => Rs. {pred:,.0f}")

joblib.dump(model,      'price_model.pkl')
joblib.dump(le_brand_p, 'price_brand_encoder.pkl')
joblib.dump(le_cpu_p,   'price_cpu_encoder.pkl')

joblib.dump(le_os_p,    'price_os_encoder.pkl')
joblib.dump(le_gfx_p,   'price_gfx_encoder.pkl')
print("\nSaved: price_model.pkl and all encoders")
