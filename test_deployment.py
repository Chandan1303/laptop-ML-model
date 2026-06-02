#!/usr/bin/env python
"""
Pre-deployment test script for Laptop ML Predictor
Run this before deploying to catch potential runtime errors
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test all required packages can be imported"""
    print("Testing imports...")
    try:
        import django
        import gunicorn
        import whitenoise
        import sklearn
        import pandas
        import numpy
        import joblib
        print("✅ All required packages imported successfully")
        print(f"   - Django: {django.__version__}")
        print(f"   - scikit-learn: {sklearn.__version__}")
        print(f"   - pandas: {pandas.__version__}")
        print(f"   - numpy: {numpy.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_model_files():
    """Test all ML model files exist and can be loaded"""
    print("\nTesting model files...")
    import joblib
    
    base_dir = Path(__file__).resolve().parent
    model_files = {
        'Brand Model': 'laptop_model.pkl',
        'CPU Encoder': 'cpu_encoder.pkl',
        'OS Encoder': 'os_encoder.pkl',
        'Graphics Encoder': 'gfx_encoder.pkl',
        'Brand Encoder': 'brand_encoder.pkl',
        'Price Model': 'price_model.pkl',
        'Price Brand Encoder': 'price_brand_encoder.pkl',
        'Price CPU Encoder': 'price_cpu_encoder.pkl',
        'Price OS Encoder': 'price_os_encoder.pkl',
        'Price Graphics Encoder': 'price_gfx_encoder.pkl',
    }
    
    all_exist = True
    for name, filename in model_files.items():
        filepath = base_dir / filename
        if filepath.exists():
            try:
                joblib.load(filepath)
                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"✅ {name}: {filename} ({size_mb:.2f} MB)")
            except Exception as e:
                print(f"⚠️  {name}: {filename} exists but failed to load: {e}")
                all_exist = False
        else:
            print(f"❌ {name}: {filename} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_django_settings():
    """Test Django settings are properly configured"""
    print("\nTesting Django settings...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_predictor.settings')
    
    try:
        import django
        django.setup()
        from django.conf import settings
        
        checks = []
        
        # Check ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            print(f"✅ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS}")
            checks.append(True)
        else:
            print("⚠️  ALLOWED_HOSTS is empty (ok for dev, bad for production)")
            checks.append(False)
        
        # Check STATIC_ROOT
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            print(f"✅ STATIC_ROOT configured: {settings.STATIC_ROOT}")
            checks.append(True)
        else:
            print("❌ STATIC_ROOT not configured")
            checks.append(False)
        
        # Check WhiteNoise
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            print("✅ WhiteNoise middleware configured")
            checks.append(True)
        else:
            print("❌ WhiteNoise middleware NOT configured")
            checks.append(False)
        
        # Check SECRET_KEY
        if settings.SECRET_KEY:
            if settings.SECRET_KEY.startswith('django-insecure-'):
                print("⚠️  SECRET_KEY uses default insecure key (set SECRET_KEY env var for production)")
            else:
                print("✅ SECRET_KEY is configured")
            checks.append(True)
        else:
            print("❌ SECRET_KEY not set")
            checks.append(False)
        
        return all(checks)
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False

def test_wsgi():
    """Test WSGI application can be loaded"""
    print("\nTesting WSGI application...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_predictor.settings')
    
    try:
        from laptop_predictor.wsgi import application
        print("✅ WSGI application loaded successfully")
        print(f"   Type: {type(application)}")
        return True
    except Exception as e:
        print(f"❌ WSGI application error: {e}")
        return False

def test_views():
    """Test views can import model files"""
    print("\nTesting views...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laptop_predictor.settings')
    
    try:
        import django
        django.setup()
        from predictor import views
        
        # Check if model loading worked
        if hasattr(views, 'model') and views.model:
            print("✅ Brand prediction model loaded in views")
        else:
            print("❌ Brand prediction model NOT loaded in views")
            return False
            
        if hasattr(views, 'price_model') and views.price_model:
            print("✅ Price prediction model loaded in views")
        else:
            print("❌ Price prediction model NOT loaded in views")
            return False
        
        # Check encoders
        if hasattr(views, 'le_brand') and views.le_brand:
            print(f"✅ Brand encoder loaded ({len(views.le_brand.classes_)} brands)")
        
        if hasattr(views, 'CPU_CHOICES') and views.CPU_CHOICES:
            print(f"✅ CPU choices loaded ({len(views.CPU_CHOICES)} options)")
        
        return True
    except Exception as e:
        print(f"❌ Views import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    """Test static files exist"""
    print("\nTesting static files...")
    base_dir = Path(__file__).resolve().parent
    static_dir = base_dir / 'static'
    
    if not static_dir.exists():
        print("❌ Static directory does not exist")
        return False
    
    required_files = [
        'css/style.css',
        'js/main.js',
    ]
    
    all_exist = True
    for rel_path in required_files:
        filepath = static_dir / rel_path
        if filepath.exists():
            print(f"✅ {rel_path}")
        else:
            print(f"❌ {rel_path} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_templates():
    """Test template files exist"""
    print("\nTesting templates...")
    base_dir = Path(__file__).resolve().parent
    templates_dir = base_dir / 'templates' / 'predictor'
    
    if not templates_dir.exists():
        print("❌ Templates directory does not exist")
        return False
    
    required_templates = [
        'index.html',
        'price.html',
        'patterns.html',
    ]
    
    all_exist = True
    for filename in required_templates:
        filepath = templates_dir / filename
        if filepath.exists():
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename} NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 70)
    print("DEPLOYMENT READINESS TEST")
    print("=" * 70)
    
    results = {
        'Imports': test_imports(),
        'Model Files': test_model_files(),
        'Django Settings': test_django_settings(),
        'WSGI Application': test_wsgi(),
        'Views': test_views(),
        'Static Files': test_static_files(),
        'Templates': test_templates(),
    }
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
    
    all_passed = all(results.values())
    
    print("=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Ready for deployment!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED - Fix issues before deploying")
        return 1

if __name__ == '__main__':
    sys.exit(main())
