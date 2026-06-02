# Laptop Price Prediction System

A Django-based machine learning web application for predicting laptop specifications and prices using Random Forest models.

## Features

- **Specification Prediction**: Predict laptop specs (CPU, GPU, OS, RAM, Storage) based on brand and budget
- **Price Prediction**: Estimate laptop prices based on specifications
- **Pattern Analysis**: Visualize pricing patterns and trends across different brands
- **Real-time Predictions**: Interactive web interface for instant predictions

## Tech Stack

- **Backend**: Django 4.x
- **Machine Learning**: scikit-learn (Random Forest Classifier/Regressor)
- **Data Processing**: pandas, numpy
- **Frontend**: HTML, CSS, JavaScript

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
├── pipeline.py           # Prediction pipeline
├── retrain.py            # Model retraining script
├── clean.py              # Data cleaning utilities
└── *.pkl                 # Trained models and encoders

## Installation

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
pip install django scikit-learn pandas numpy
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://localhost:8000`

## Usage

### Specification Prediction
1. Navigate to the home page
2. Select a laptop brand
3. Enter your budget
4. Click "Predict" to get recommended specifications

### Price Prediction
1. Navigate to the price prediction page
2. Select brand, CPU, GPU, OS
3. Enter RAM and storage specifications
4. Get instant price estimates

### Pattern Analysis
View pricing trends and patterns across different brands and specifications.

## Models

The application uses two main Random Forest models:
- **Specification Model**: Predicts optimal specs based on brand and price
- **Price Model**: Predicts price based on specifications

Models are pre-trained and saved as `.pkl` files for quick inference.

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License
