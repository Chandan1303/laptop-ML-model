import pandas as pd
import numpy as np
import re


# ── Cleaning strategies ───────────────────────────────────────────────────────

def parse_price(val):
    if pd.isna(val): return np.nan
    cleaned = re.sub(r'[^\d.]', '', str(val))
    try: return float(cleaned)
    except: return np.nan

def parse_screen(val):
    if pd.isna(val): return np.nan
    m = re.search(r'(\d+\.?\d*)', str(val))
    return float(m.group(1)) if m else np.nan

def parse_storage(val):
    if pd.isna(val) or not isinstance(val, str): return np.nan
    v = val.lower()
    m = re.search(r'(\d+\.?\d*)\s*(tb|gb|mb)?', v)
    if not m: return np.nan
    n, u = float(m.group(1)), m.group(2)
    return n * 1024 if u == 'tb' else n / 1024 if u == 'mb' else n

def parse_ram(val):
    if pd.isna(val) or not isinstance(val, str): return np.nan
    m = re.search(r'(\d+\.?\d*)\s*(gb|mb)?', val.lower())
    if not m: return np.nan
    n = float(m.group(1))
    return n / 1024 if m.group(2) == 'mb' else n


# ── Clean Amazon dataset ──────────────────────────────────────────────────────

def clean_amazon(input_file='amazon_laptop_prices_v01 (1).csv',
                 output_file='cleaned_amazon_laptop_prices.csv'):
    df = pd.read_csv(input_file)

    df['Price']              = df['Price'].apply(parse_price)
    df['screen_size_inches'] = df['screen_size'].apply(parse_screen)
    df['harddisk_gb']        = df['harddisk'].apply(parse_storage)
    df['ram_gb']             = df['ram'].apply(parse_ram)

    for col in ['screen_size_inches', 'harddisk_gb', 'ram_gb', 'rating', 'Price']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    for col in ['brand', 'cpu', 'OS', 'graphics']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')

    df = df.drop(columns=['screen_size', 'harddisk', 'ram'], errors='ignore')
    df.to_csv(output_file, index=False)
    print(f"[clean_amazon] Saved {len(df)} rows → {output_file}")
    return df


# ── Clean messy dataset ───────────────────────────────────────────────────────

def clean_messy(input_file='single_amazon_laptop_messy_dataset_1-10.csv',
                output_file='cleaned_messy_laptop_data_v2.csv'):
    df = pd.read_csv(input_file)

    df['price_cleaned']      = df['price'].apply(parse_price)
    df['screen_size_inches'] = df['screen_size'].apply(parse_screen)
    df['hard_disk_gb']       = df['hard_disk_size'].apply(parse_storage)
    df['ram_gb']             = df['ram'].str.extract(r'(\d+)').astype(float)

    for col in ['rating', 'price_cleaned', 'screen_size_inches', 'hard_disk_gb', 'ram_gb']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    for col in ['brand', 'cpu_model', 'os', 'graphics_card']:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')

    mapping = {
        'brand': 'Brand', 'rating': 'Rating', 'price_cleaned': 'Price',
        'screen_size_inches': 'Screen_Size', 'hard_disk_gb': 'Storage_GB',
        'cpu_model': 'CPU', 'ram_gb': 'RAM_GB', 'os': 'OS', 'graphics_card': 'Graphics'
    }
    available = {k: v for k, v in mapping.items() if k in df.columns}
    df = df[list(available.keys())].rename(columns=available)
    df.to_csv(output_file, index=False)
    print(f"[clean_messy] Saved {len(df)} rows → {output_file}")
    return df


if __name__ == '__main__':
    clean_amazon()
    clean_messy()
