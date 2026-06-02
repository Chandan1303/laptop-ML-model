# Laptop Price Prediction System

A Django-based machine learning web application for predicting laptop specifications and prices using Random Forest models.

🚀 **[Live Demo](https://your-app-name.onrender.com)** (Replace after deployment)

## Features

- **Specification Prediction**: Predict laptop specs (CPU, GPU, OS, RAM, Storage) based on brand and budget
- **Price Prediction**: Estimate laptop prices based on specifications
- **Pattern Analysis**: Visualize pricing patterns and trends across different brands
- **Real-time Predictions**: Interactive web interface for instant predictions
- **10 Design Patterns**: Implements Creational, Structural, and Behavioral patterns

## Tech Stack

- **Backend**: Django 4.x + Gunicorn
- **Machine Learning**: scikit-learn (Random Forest Classifier/Regressor)
- **Data Processing**: pandas, numpy
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render with WhiteNoise for static files

## Project Structure

```
├── laptop_predictor/       # Django project settings
├── predictor/              # Main Django app
│   ├── views.py           # View logic for predictions
│   ├── urls.py            # URL routing
│   └── templatetags/      # Custom template filters
├── templates/             # HTML templates
├── static/               # CSS, JS, and images
├── train.py              # Train specification model
├── train_price_model.py  # Train price prediction model
├── pipeline.py           # Prediction pipeline with design patterns
├── retrain.py            # Model retraining script
├── clean.py              # Data cleaning utilities
├── *.pkl                 # Trained models and encoders
├── render.yaml           # Render deployment config
└── build.sh              # Production build script
```

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Chandan1303/laptop-ML-model.git
cd laptop-ML-model
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional for local dev):
```bash
# Create .env file (optional)
cp .env.example .env
# Edit .env and set DEBUG=True for development
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Collect static files (for production-like testing):
```bash
python manage.py collectstatic --no-input
```

7. Start the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to `http://localhost:8000`

## Production Deployment

### Deploy to Render (Recommended)

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment instructions.

**Quick Steps:**

1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables:
   - `SECRET_KEY` (auto-generate)
   - `DEBUG=False`
   - `ALLOWED_HOSTS=.onrender.com`
4. Deploy automatically

**Build Command**: `./build.sh`  
**Start Command**: `gunicorn laptop_predictor.wsgi:application`

### Pre-Deployment Testing

Run comprehensive tests before deploying:

```bash
python test_deployment.py
```

This checks:
- Package imports
- Model file loading
- Django configuration
- WSGI application
- Static files and templates

## Usage

### Specification Prediction
1. Navigate to the home page
2. Select a laptop brand
3. Enter your budget
4. Click "Predict" to get recommended specifications

### Price Prediction
1. Navigate to the price prediction page (`/price/`)
2. Select brand, CPU, GPU, OS
3. Enter RAM and storage specifications
4. Get instant price estimates

### Pattern Analysis
View pricing trends and patterns across different brands and specifications at `/patterns/`.

## Design Patterns Implementation

This project demonstrates 10 software design patterns:

**Creational Patterns:**
1. **Singleton** - ModelRepository (single model manager)
2. **Factory Method** - CleanerFactory (dataset cleaner creation)
3. **Builder** - ModelBuilder (step-by-step model construction)

**Structural Patterns:**
4. **Adapter** - DatasetAdapter (schema compatibility)
5. **Facade** - LaptopPredictor (simplified prediction interface)
6. **Decorator** - LoggingCleaner (adds logging to cleaners)

**Behavioral Patterns:**
7. **Strategy** - CurrencyStrategy, StorageStrategy (pluggable algorithms)
8. **Observer** - PipelineEventBus (event notification system)
9. **Command** - CleanCommand, TrainCommand (encapsulated operations)
10. **Template Method** - AmazonCleaner, MessyCleaner (algorithm skeleton)

View detailed pattern explanations at `/patterns/`.

## Models

The application uses two main Random Forest models:
- **Specification Model** (`laptop_model.pkl` - 55.98 MB): Predicts optimal specs based on brand and price
- **Price Model** (`price_model.pkl` - 31.76 MB): Predicts price based on specifications

Models are pre-trained and saved as `.pkl` files for quick inference.

## Team

Built by **Chandan** and team as a multi-subject integration project combining:
- Full Stack Development (Django)
- Machine Learning (scikit-learn)
- Software Architecture & Design Patterns (SADP)

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License
