import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.metrics import accuracy_score, classification_report

# Load cleaned datasets
df1 = pd.read_csv('cleaned_amazon_laptop_prices.csv')
df2 = pd.read_csv('cleaned_messy_laptop_data_v2.csv')

# Align columns
df1 = df1.rename(columns={
    'brand': 'Brand', 'rating': 'Rating',
    'screen_size_inches': 'Screen_Size', 'harddisk_gb': 'Storage_GB',
    'ram_gb': 'RAM_GB', 'cpu': 'CPU', 'OS': 'OS', 'graphics': 'Graphics'
})

common = ['Brand', 'Price', 'Rating', 'Screen_Size', 'Storage_GB', 'RAM_GB', 'CPU', 'OS', 'Graphics']
df = pd.concat([df1[common], df2[common]], ignore_index=True)

# ── Normalize brand names (fix Dell/DELL/dell etc.) ──────────────────────────
brand_map = {
    'dell': 'Dell', 'DELL': 'Dell',
    'hp': 'HP', 'Hp': 'HP',
    'lenovo': 'Lenovo', 'LENOVO': 'Lenovo',
    'acer': 'Acer', 'ACER': 'Acer',
    'asus': 'Asus', 'ASUS': 'Asus',
    'msi': 'MSI', 'Msi': 'MSI',
    'samsung': 'Samsung', 'SAMSUNG': 'Samsung',
    'lg': 'LG', 'Lg': 'LG',
    'microsoft': 'Microsoft', 'Microsoft': 'Microsoft',
    'apple': 'Apple', 'Apple': 'Apple',
    'alienware': 'Alienware', 'Alienware': 'Alienware',
    'razer': 'Razer', 'Razer': 'Razer',
    'gigabyte': 'Gigabyte', 'GIGABYTE': 'Gigabyte',
    'panasonic': 'Panasonic',
    'toughbook': 'Toughbook',
    'rokc': 'Rokc', 'ROKC': 'Rokc',
}
df['Brand'] = df['Brand'].str.strip().replace(brand_map)

# Keep only brands with enough samples
counts = df['Brand'].value_counts()
valid_brands = counts[counts >= 10].index
df = df[df['Brand'].isin(valid_brands)].copy()

print("Brand distribution after normalization:")
print(df['Brand'].value_counts())
print(f"\nTotal samples: {len(df)}, Brands: {df['Brand'].nunique()}")

# ── Encode categorical features ───────────────────────────────────────────────
le_cpu   = LabelEncoder()
le_os    = LabelEncoder()
le_gfx   = LabelEncoder()
le_brand = LabelEncoder()

df['CPU']      = le_cpu.fit_transform(df['CPU'].astype(str))
df['OS']       = le_os.fit_transform(df['OS'].astype(str))
df['Graphics'] = le_gfx.fit_transform(df['Graphics'].astype(str))

X = df.drop('Brand', axis=1)
y = le_brand.fit_transform(df['Brand'])

# ── Balance classes via oversampling minority brands ─────────────────────────
df_encoded = X.copy()
df_encoded['__label__'] = y

max_count = df_encoded['__label__'].value_counts().max()
# Cap oversample at 3x original or max_count, whichever is smaller
target = min(max_count, 300)

balanced_parts = []
for label in df_encoded['__label__'].unique():
    subset = df_encoded[df_encoded['__label__'] == label]
    if len(subset) < target:
        subset = resample(subset, replace=True, n_samples=target, random_state=42)
    balanced_parts.append(subset)

df_bal = pd.concat(balanced_parts)
X_bal = df_bal.drop('__label__', axis=1)
y_bal = df_bal['__label__'].values

print(f"\nAfter balancing: {len(X_bal)} samples")

# ── Train ─────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_bal, y_bal, test_size=0.2, random_state=42, stratify=y_bal
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=25,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred) * 100
print(f"\nAccuracy: {acc:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le_brand.classes_))

# ── Save ──────────────────────────────────────────────────────────────────────
joblib.dump(model,    'laptop_model.pkl')
joblib.dump(le_cpu,   'cpu_encoder.pkl')
joblib.dump(le_os,    'os_encoder.pkl')
joblib.dump(le_gfx,   'gfx_encoder.pkl')
joblib.dump(le_brand, 'brand_encoder.pkl')
df.to_csv('final_combined_laptop_data.csv', index=False)
print("\nAll artifacts saved.")

# ── Quick sanity checks ───────────────────────────────────────────────────────
print("\n--- Sanity Checks ---")
tests = [
    {'Price': 120000, 'Rating': 4.5, 'Screen_Size': 13.6, 'Storage_GB': 512,
     'RAM_GB': 16, 'CPU': 'Apple M2', 'OS': 'macOS 12 Monterey', 'Graphics': 'Integrated'},
    {'Price': 120000, 'Rating': 4.5, 'Screen_Size': 13.6, 'Storage_GB': 512,
     'RAM_GB': 16, 'CPU': 'Apple M1', 'OS': 'Mac OS', 'Graphics': 'Integrated'},
    {'Price': 65000, 'Rating': 4.2, 'Screen_Size': 15.6, 'Storage_GB': 512,
     'RAM_GB': 16, 'CPU': 'Intel Core i5', 'OS': 'Windows 11 Home', 'Graphics': 'Integrated'},
    {'Price': 90000, 'Rating': 4.3, 'Screen_Size': 14.0, 'Storage_GB': 512,
     'RAM_GB': 16, 'CPU': 'Intel Core i7', 'OS': 'Windows 11 Pro', 'Graphics': 'Nvidia GeForce RTX 3060'},
]
for t in tests:
    import pandas as pd2
    row = pd.DataFrame([t])
    row['CPU']      = le_cpu.transform(row['CPU'])
    row['OS']       = le_os.transform(row['OS'])
    row['Graphics'] = le_gfx.transform(row['Graphics'])
    pred = model.predict(row)
    proba = model.predict_proba(row)[0]
    top3 = sorted(zip(le_brand.classes_, proba), key=lambda x: -x[1])[:3]
    print(f"CPU={t['CPU'][:20]}, OS={t['OS'][:20]} => {le_brand.inverse_transform(pred)[0]}")
    print(f"  top3: {[(b, round(p*100,1)) for b,p in top3]}")
