import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# 1. Load the cleaned datasets
df1 = pd.read_csv('cleaned_amazon_laptop_prices.csv')
df2 = pd.read_csv('cleaned_messy_laptop_data_v2.csv')

# 2. Align Column Names (Mapping df1 to match df2's format)
mapping = {
    'brand': 'Brand',
    'rating': 'Rating',
    'screen_size_inches': 'Screen_Size',
    'harddisk_gb': 'Storage_GB',
    'ram_gb': 'RAM_GB',
    'cpu': 'CPU',
    'OS': 'OS',
    'graphics': 'Graphics'
}
df1 = df1.rename(columns=mapping)


common_features = ['Brand', 'Price', 'Rating', 'Screen_Size', 'Storage_GB', 'RAM_GB', 'CPU', 'OS', 'Graphics']
df_combined = pd.concat([df1[common_features], df2[common_features]], ignore_index=True)


df_combined['Brand'] = df_combined['Brand'].str.strip().str.title()
brand_counts = df_combined['Brand'].value_counts()
df_final = df_combined[df_combined['Brand'].isin(brand_counts[brand_counts >= 5].index)].copy()


le_cpu = LabelEncoder()
le_os = LabelEncoder()
le_gfx = LabelEncoder()

df_final['CPU'] = le_cpu.fit_transform(df_final['CPU'].astype(str))
df_final['OS'] = le_os.fit_transform(df_final['OS'].astype(str))
df_final['Graphics'] = le_gfx.fit_transform(df_final['Graphics'].astype(str))

# Encode Target (Brand)
le_brand = LabelEncoder()
X = df_final.drop('Brand', axis=1)
y = le_brand.fit_transform(df_final['Brand'])

# 5. Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 6. Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)
model.fit(X_train, y_train)

# 7. Results
y_pred = model.predict(X_test)
print(f"Combined Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nTop Predictors (Feature Importance):")
importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)
print(importance)

# Save the final combined dataset for your project
df_final.to_csv('final_combined_laptop_data.csv', index=False)


import joblib

joblib.dump(model, "laptop_model.pkl")
joblib.dump(le_cpu, "cpu_encoder.pkl")
joblib.dump(le_os, "os_encoder.pkl")
joblib.dump(le_gfx, "gfx_encoder.pkl")
joblib.dump(le_brand, "brand_encoder.pkl")