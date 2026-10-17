# LaptopPilot
## Machine-Learning-Based Laptop Brand and Price Prediction System

**Project Report**

Prepared by:

- Dayanand Shivananda Sagar — 4NI23IS252
- Chandan Shridhar Hegde — 4NI23IS253
- Harsha S — 4NI24IS408
- Mohammad Masood Hassan H A — 4NI24IS412

Department of Information Science and Engineering  
The National Institute of Engineering, Mysuru  
Academic Year: 2025–2026

> Replace or confirm institutional, guide, semester and academic-year details to match the final submission requirements.

---

# ABSTRACT

Selecting a laptop involves comparing many specifications, including brand, price, processor, operating system, graphics, memory, storage, display size and customer rating. The number of available models and the inconsistent way product information is presented can make comparisons difficult. This project, **LaptopPilot**, is a web-based machine-learning application designed to help users explore laptop information through two prediction functions: laptop-brand prediction from a set of specifications and laptop-price estimation from product characteristics.

The application combines a Django web backend with trained machine-learning models developed using Python, pandas, NumPy and scikit-learn. The brand classifier uses a Random Forest model to estimate a likely brand from price, rating, screen size, storage capacity, RAM, CPU, operating system and graphics information. The price estimator uses a Random Forest regressor and laptop attributes, including brand, rating, display size, storage, RAM, CPU, operating system, graphics, processor speed and total sales, to estimate a price in Indian rupees. Categorical values are encoded during model training, and the trained estimators and encoders are persisted as joblib artifacts for inference.

LaptopPilot provides interactive pages for brand prediction, price prediction and design-pattern information. It validates submitted values, checks selected brand and hardware combinations against configured compatibility rules, and presents prediction results through a browser-based interface. The application also includes user registration, login, email verification and password-reset flows. The project demonstrates an end-to-end workflow covering dataset cleaning, feature preparation, supervised learning, model integration, web development and software quality assurance.

The system is intended as a decision-support and educational application rather than a substitute for current retailer quotations. Prediction quality depends on the coverage and quality of the training data, and the outputs may not reflect live inventory, discounts, regional taxes or changes in currency exchange rates. The existing QA documentation records tests for the main routes, form behavior, validation and prediction flows. The report describes the design, implementation, testing, limitations and possible future improvements of LaptopPilot.

**Keywords:** LaptopPilot, machine learning, Random Forest, laptop price prediction, brand classification, Django, web application, software testing.

---

# CONTENTS

1. Introduction
2. Literature Survey
3. System Requirements and Analysis
4. System Design
5. System Implementation
6. System Testing
7. Conclusion
8. Application Screenshots
9. Future Enhancements
10. References

> Add page numbers after transferring this content into the institution's report template and finalizing the layout.

---

# CHAPTER 1
# INTRODUCTION

## 1.1 Background

Laptop computers are used for education, software development, business, communication, entertainment and many other activities. A laptop's suitability depends on the relationship between its price and its specifications. Processor family, memory, storage, display size, graphics capability, operating system and brand reputation all influence a buyer's decision. Comparing products is challenging when these attributes are described inconsistently or distributed across different product listings.

Machine learning provides techniques for learning patterns from previously observed examples. Given a structured dataset of laptop specifications and associated outcomes, a classification model can estimate a brand category, while a regression model can estimate a numerical price. These predictions can be surfaced through a web application so that users can submit values and receive results without running scripts locally.

LaptopPilot applies this approach to two related tasks. The first task estimates a laptop brand from product attributes and a stated price. The second estimates the price associated with a selected brand and a set of specifications. The project also uses a Django application to connect the trained models to browser-based forms and result pages.

## 1.2 Problem Statement

Laptop product information is often presented in different formats, with specifications expressed as text, numbers or a mixture of both. Manual comparison is time-consuming, and a user may have difficulty determining whether a proposed price is reasonable for a given configuration. A simple, centralized application is needed to accept laptop attributes, standardize them for model inference and return an understandable prediction.

The project addresses the following problem:

> Develop a web-based system that uses historical laptop product data and supervised machine-learning models to estimate a laptop brand from selected attributes and estimate a laptop price from a specified configuration.

## 1.3 Objectives

- Develop a browser-accessible application for laptop brand prediction.
- Develop a separate price-prediction function for laptop configurations.
- Prepare categorical and numerical input features in a consistent form for inference.
- Train and persist classification and regression models for reuse by the web application.
- Validate missing, malformed, unrealistic and incompatible form inputs.
- Present results and useful context through a clear web interface.
- Provide user registration and authentication for protected prediction pages.
- Test the principal user journeys and document known limitations.
- Demonstrate common software design patterns in the supporting data-processing and training pipeline.

## 1.4 Scope

LaptopPilot includes:

- A Django web application with home, price-prediction and design-pattern pages.
- A Random Forest classifier that predicts a laptop brand from specification features.
- A Random Forest regressor that estimates laptop price.
- Persisted model and label-encoder files loaded by the Django application.
- Data cleaning and training scripts for laptop datasets in CSV format.
- Input validation and configurable brand-to-feature compatibility rules.
- Account registration, login, email verification and password-reset routes.
- A map/location presentation for the predicted brand's mapped country, where configured.
- Automated Django tests and QA documentation for application behavior.
- A Render-oriented deployment configuration using Gunicorn and WhiteNoise.

The system does not guarantee the availability, stock status or current selling price of a product. It does not replace retailer catalogues, professional purchasing advice or a live product search service.

## 1.5 Existing System

Laptop buyers commonly compare product listings manually, use retailer filters, consult review sites or rely on a seller's recommendation. These methods can be effective but require users to inspect multiple listings and interpret specifications expressed in different formats. A product listing may also omit some details or use model-specific terminology that makes direct comparisons difficult.

In a manual workflow, brand and price judgments are not necessarily derived from a consistent set of historical examples. A user may have no quick way to estimate the likely brand category for a configuration or to compare a proposed configuration's estimated price with patterns in the available dataset.

## 1.6 Limitations of the Existing Approach

- Product information is distributed across websites and listings.
- Specification names and units may differ between data sources.
- Comparing several configurations manually takes time.
- Historical product patterns are not always available in a single interface.
- Prices change over time with discounts, taxes, availability and market conditions.
- Manual comparison does not provide a repeatable model-based estimate.

## 1.7 Proposed System

The proposed system, LaptopPilot, brings laptop data processing, trained models and user-facing prediction forms together in one web application. A user supplies laptop attributes through a form. The Django view validates and normalizes the submitted values, transforms categorical values using the corresponding encoders, and sends the prepared feature row to the appropriate model. The returned class or numerical estimate is then displayed in the web page.

For brand prediction, the system returns a predicted brand and a ranked set of class probabilities where supported by the classifier. Compatibility rules are used to check whether the selected CPU, operating system and graphics combination is plausible for known brands. For price prediction, the application applies a regression model to the submitted configuration and presents the estimated price. Django authentication protects the principal prediction pages.

## 1.8 Advantages of the Proposed System

- Centralizes the two prediction tasks in one web application.
- Reuses trained model artifacts instead of retraining for every request.
- Provides a consistent feature-processing path from form input to model inference.
- Applies server-side checks to reject or report invalid values.
- Offers a browser interface that does not require the user to operate Python scripts.
- Demonstrates the integration of machine learning with a conventional web framework.
- Includes test coverage and QA records for major application flows.

---

# CHAPTER 2
# LITERATURE SURVEY

The literature survey considers supervised learning, Random Forest methods, data preparation, web-based machine-learning applications and software testing. Together, these topics provide a foundation for building LaptopPilot.

## 2.1 Supervised Learning for Classification and Regression

Supervised learning uses examples containing input features and known outcomes. A classification model learns to assign an input to one of a finite number of categories, such as laptop brands. A regression model learns to estimate a numerical target, such as a price. Both tasks require representative training data, suitable feature preparation and evaluation on data not used to fit the model.

LaptopPilot uses these two problem formulations separately: brand is the categorical target for the classifier, and price is the numerical target for the regressor. This separation allows each model to be trained with a task-appropriate objective and evaluation method.

## 2.2 Random Forest

Random Forest is an ensemble method that combines predictions from multiple decision trees. For classification, the trees vote across possible classes; for regression, their numerical predictions are aggregated. Random feature selection and sampling help the ensemble model complex relationships while reducing dependence on a single tree.

Random Forest is used in LaptopPilot because it supports both classification and regression, can model nonlinear relationships, and provides feature-importance estimates. These properties make it a practical baseline for structured laptop data. Model performance still depends on data quality, feature definitions and evaluation methodology; using an ensemble does not by itself guarantee accurate or unbiased results.

## 2.3 Data Preparation and Categorical Encoding

Product datasets often contain numeric values embedded in strings, inconsistent units, missing values and different column names. Data preparation therefore includes parsing numeric attributes, standardizing schemas, handling missing values and preparing categories for model input.

LaptopPilot's scripts use pandas and NumPy for data manipulation and scikit-learn label encoders for categorical values such as CPU, operating system, graphics and brand. The training and inference stages must use compatible feature ordering and the same fitted encoders. Persisting the encoders alongside each model helps maintain this correspondence.

Label encoding assigns an integer to each observed category. This is a convenient representation for the current pipeline, but the integer values do not represent a meaningful ordering between categories. Alternative encodings, such as one-hot encoding or native categorical methods, may be considered and compared in future work.

## 2.4 Machine Learning in Web Applications

A web-based prediction application typically separates the user interface, request handling, feature preparation, model inference and response rendering. This structure makes it possible to present model functionality to users while keeping model artifacts and processing logic on the server.

LaptopPilot uses Django views to receive requests, validate values and invoke models. HTML templates render pages and results, while static CSS and JavaScript provide presentation and browser-side behavior. The trained artifacts are loaded by the application for prediction.

## 2.5 Software Testing and Quality Assurance

Testing verifies that an application behaves as expected for valid and invalid inputs. Black-box tests check visible behavior such as page rendering, form fields, navigation and output. White-box tests examine internal branches and validation rules. Django's test framework supports request-level testing of routes and view behavior.

The project QA records describe tests covering the main screens, valid prediction requests, invalid or missing form values, compatibility behavior and map fallback behavior. Testing is important because prediction quality and application correctness are different concerns: a web route can work correctly even if a model is not sufficiently accurate for a particular population.

## 2.6 Key Takeaways

1. **Classification and regression solve different prediction problems.** Brand prediction is a classification task, while price estimation is a regression task.
2. **Random Forest provides a practical structured-data baseline.** Its effectiveness must be verified using held-out data and appropriate metrics.
3. **Preprocessing consistency is essential.** Training and inference must use the same feature definitions, categorical encoders and feature order.
4. **Historical prices are not live quotations.** Price predictions should be interpreted as estimates based on the training data.
5. **Web integration requires input validation.** Malformed and unrealistic values must be handled before they reach model inference.
6. **Functional testing does not replace model evaluation.** Application-flow tests and predictive-performance evaluation should be reported separately.

---

# CHAPTER 3
# SYSTEM REQUIREMENTS AND ANALYSIS

## 3.1 Functional Requirements

The system shall:

- Display the LaptopPilot landing page and provide navigation to supported features.
- Allow an authenticated user to submit laptop specifications for brand prediction.
- Return a predicted brand and, where available, ranked class-probability information.
- Allow an authenticated user to submit a laptop configuration for price prediction.
- Return the model's estimated price in Indian rupees.
- Validate required fields, numeric formats, realistic value ranges and compatible choices.
- Preserve submitted values when a form is returned with a validation error.
- Provide account registration, login, logout, email-verification and password-reset flows.
- Display the design-pattern information page.
- Display an appropriate map or fallback state depending on available map configuration.
- Return understandable error feedback rather than exposing a failed prediction as a valid result.

## 3.2 Non-Functional Requirements

- **Usability:** Forms and result areas should be understandable to users with basic web experience.
- **Reliability:** Valid requests should return a result without requiring model training during the request.
- **Performance:** Model inference should be suitable for interactive web requests under the expected demonstration workload.
- **Maintainability:** Model training, data cleaning, Django views, templates and static assets should remain logically separated.
- **Portability:** The project should run in a compatible Python environment with its declared dependencies installed.
- **Security:** Authentication, CSRF protection, secret configuration and email credentials should be handled appropriately for the deployment environment.
- **Scalability:** The current application is designed for project-scale use; production scaling would require additional monitoring and infrastructure decisions.

## 3.3 Software Requirements

- Operating System: Windows or a compatible Linux deployment environment.
- Programming Language: Python.
- Web Framework: Django.
- Machine-Learning Library: scikit-learn.
- Data Processing Libraries: pandas and NumPy.
- Model Persistence: joblib.
- Frontend: HTML, CSS and JavaScript with Django templates.
- Application Server for deployment: Gunicorn.
- Static-file middleware: WhiteNoise.
- Database configuration: SQLite in the current Django settings.
- Development and testing: Visual Studio Code, Git, browser and Django test runner.
- Optional external service: Google Maps JavaScript API for map display when a valid key is configured.

> Confirm the exact Python and Django versions against the final deployment environment. Dependency declarations and environment configuration should be kept synchronized before production deployment.

## 3.4 Hardware Requirements

The system has no specialized hardware requirement. A standard development computer capable of running Python, a web browser and the Django application is sufficient for interactive use. Model training may require additional CPU time and memory depending on dataset size and the number of trees.

Recommended development setup:

- A modern multi-core processor.
- At least 8 GB RAM for comfortable development and local testing.
- Adequate free storage for source datasets, trained model files and dependencies.
- A supported browser and stable internet access for package installation, deployment and optional external map resources.

These are practical recommendations, not experimentally established minimum hardware requirements.

## 3.5 Data Requirements

The training scripts refer to laptop-price CSV datasets, including:

- `amazon_laptop_prices_v01 (1).csv`
- `single_amazon_laptop_messy_dataset_1-10.csv`
- Cleaned variants generated by the pipeline.

The model data includes fields such as brand, price, rating, screen size, hard-disk/storage capacity, RAM, CPU, operating system and graphics. The price-regression training script also derives CPU speed and uses a total-sales field. Numeric values may need extraction from strings and unit normalization before they can be used consistently.

The quality and representativeness of these datasets determine the practical usefulness of model predictions. Dataset size, collection dates, licensing, geographic coverage and exact provenance should be documented from the original data provider before formal publication.

## 3.6 Existing System

The existing user workflow relies on manually searching retailer catalogues, comparing specifications and interpreting prices. Individual datasets and product pages may use different terminology or units. Users do not necessarily have a single interface that accepts a configuration and returns a model-based brand or price estimate.

## 3.7 Drawbacks of the Existing System

- Product comparison can require multiple searches and manual calculations.
- Listings may use inconsistent names and units for specifications.
- Historical patterns may not be easy for an individual user to interpret.
- A manual estimate can vary between users.
- Current prices are affected by time-sensitive discounts, location and inventory.

## 3.8 Proposed System

LaptopPilot provides a Django application with trained Random Forest models. The data-preparation scripts standardize and combine the input features, train separate models and serialize the estimators and encoders. During a web request, the application validates the user-submitted fields, prepares the input row, performs inference and renders the result.

The classifier uses price, rating, screen size, storage, RAM, CPU, operating system and graphics as input features and predicts a brand. The regressor uses brand, rating, screen size, storage, RAM, CPU, operating system, graphics, CPU speed and total sales as input features and predicts price.

## 3.9 Advantages of the Proposed System

- Provides an integrated interface for two laptop-related prediction tasks.
- Makes model inference accessible through a web browser.
- Reuses fitted model and encoder artifacts.
- Performs server-side validation and brand-feature compatibility checks.
- Includes authentication and QA tests for major user flows.
- Uses modular scripts for dataset cleaning, model training and prediction.

## 3.10 Limitations and Risks

- Predictions depend on the source data and may not generalize to unseen product categories.
- A dataset can contain duplicate, stale, biased or inconsistent product records.
- Label-encoded categorical values can impose artificial numeric relationships on some tree implementations.
- The price training script uses a configured USD-to-INR conversion factor; this is not a live exchange-rate service.
- Retail prices change due to sales, taxes, location, stock, seller and product age.
- Total sales may be strongly associated with product price and may not be available at prediction time; its suitability as a production feature requires further validation.
- Brand compatibility rules are manually configured and may not represent every product generation or regional configuration.
- Email and map functionality depend on deployment configuration and external services.
- Loading large model artifacts can increase application startup time and storage needs.

---

# CHAPTER 4
# SYSTEM DESIGN

## 4.1 Design Methodology

LaptopPilot follows a data-to-prediction workflow consisting of dataset ingestion, data cleaning, feature construction, model training, artifact storage, web-request validation, model inference and result rendering.

### Stage 1: Dataset ingestion

The training and pipeline scripts read laptop records from CSV files. Different source datasets may have different field names and formats.

### Stage 2: Cleaning and schema alignment

The pipeline uses source-specific cleaners and an adapter to map fields into a shared schema. Cleaning strategies parse currency, storage, RAM and screen-size values. Missing numerical and categorical values are handled by the source-specific cleaning routines.

### Stage 3: Feature preparation

Categorical attributes are transformed with fitted label encoders. The classifier and regressor use separate feature sets and encoders appropriate to their targets.

### Stage 4: Model training and evaluation

The brand model is a Random Forest classifier trained with a stratified 80/20 train-test split and a fixed random seed in the training scripts. The price model is a Random Forest regressor trained with an 80/20 split and a fixed random seed. The price-training script calculates mean absolute error, R-squared and mean absolute percentage error on its held-out test set.

### Stage 5: Artifact persistence

The trained estimators and their encoders are saved as joblib `.pkl` files. The Django application loads these files and uses them for inference.

### Stage 6: Web interaction and response

The user submits a form. Django validates and normalizes values, checks relevant compatibility rules, creates a model input row and invokes the classifier or regressor. The result or validation error is rendered in the corresponding template.

## 4.2 System Architecture

The application can be understood as the following logical layers:

1. **Presentation layer:** Django HTML templates, CSS and JavaScript.
2. **Request and application layer:** Django URLs, views, authentication and validation.
3. **Prediction layer:** Random Forest classifier, Random Forest regressor and fitted encoders.
4. **Data preparation layer:** CSV cleaning, schema adaptation, feature engineering and training scripts.
5. **Persistence layer:** joblib model artifacts and the configured SQLite database for Django data.
6. **External service layer:** SMTP email delivery and optional Google Maps resources.

**Figure 4.1: LaptopPilot system architecture**  
Insert an architecture diagram showing the browser, Django application, validation and prediction views, serialized models/encoders, SQLite database, SMTP service and optional map service.

## 4.3 Data Flow

The brand-prediction workflow is:

1. The authenticated user opens the brand-prediction page.
2. The user enters price, rating, screen size, storage, RAM, CPU, operating system and graphics.
3. The server parses numeric values and resolves categorical selections against the available choices.
4. The server checks basic value bounds and CPU/OS/graphics compatibility.
5. Categorical values are transformed using the brand-model encoders.
6. The classifier predicts a brand and derives the top class scores.
7. The application maps the predicted brand to the configured country information and renders the result.

The price-prediction workflow is:

1. The authenticated user opens the price-prediction page.
2. The user supplies brand, rating, screen size, storage, RAM, CPU, operating system, graphics, CPU speed and total sales.
3. The server parses and validates the values, then transforms categorical attributes with the price-model encoders.
4. The regressor predicts an estimated price.
5. The result is rendered on the price page with the submitted values and any supporting interface information.

**Figure 4.2: Prediction data flow**  
Insert a flowchart showing request submission, validation, encoding, model inference, result rendering and the validation-error path.

## 4.4 Model Design

### 4.4.1 Brand classifier

- Algorithm: `RandomForestClassifier`.
- Target: laptop brand.
- Input fields: price, rating, screen size, storage capacity, RAM, CPU, operating system and graphics.
- Categorical features are label-encoded.
- The training scripts use a fixed random seed and a held-out test partition.
- The pipeline implementation configures 200 trees and a maximum depth of 20.
- The model and encoders are saved as joblib artifacts.

### 4.4.2 Price regressor

- Algorithm: `RandomForestRegressor`.
- Target: price in Indian rupees.
- Input fields: brand, rating, screen size, storage capacity, RAM, CPU, operating system, graphics, CPU speed and total sales.
- The training script configures 500 trees, a maximum depth of 20, a minimum leaf size of 3 and square-root feature selection.
- The script evaluates a held-out test set using MAE, R-squared and MAPE.
- The model and categorical encoders are saved as joblib artifacts.

The report does not state numerical performance values because the checked-in training script calculates them at runtime and the corresponding output values are not included as verified results in the project documentation. Insert the final console metrics after running training against the finalized dataset.

## 4.5 Database Design

The current Django configuration uses SQLite as the application database. Django's built-in authentication and session framework manage user accounts and sessions. Laptop product records used to train the models are prepared from CSV files; the prediction artifacts are stored separately as serialized files rather than being represented as a live product-catalogue database.

## 4.6 Security and Error Handling Design

The application uses Django authentication for protected prediction views and includes Django security middleware and CSRF middleware. Email verification and password reset use Django's account/token utilities. Environment-based settings are available for deployment-specific values such as secret configuration, mail server configuration, the public base URL and optional map API configuration.

User-entered values are parsed and checked before prediction. Invalid or unsupported values should produce a user-visible error and should not be represented as a valid model prediction. Deployment secrets must be configured outside source control and rotated if they have ever been exposed.

---

# CHAPTER 5
# SYSTEM IMPLEMENTATION

## 5.1 Development Environment

The application is implemented in Python using Django. Machine-learning and data-processing functionality uses scikit-learn, pandas, NumPy and joblib. The user interface is implemented with Django templates, HTML, CSS and JavaScript. The production configuration includes Gunicorn for serving the Django WSGI application and WhiteNoise for static-file handling.

## 5.2 Data Cleaning and Preparation

The project includes a pipeline for handling more than one laptop dataset. Source-specific cleaner classes parse and normalize product fields, impute missing values and select or retain the fields required for later stages. A dataset adapter aligns compatible column names before records are combined.

The pipeline defines cleaning strategies for currency, storage, RAM and screen size. These strategies convert values represented as strings into numeric fields where possible. The training workflow then prepares categorical values and filters records according to the implemented minimum brand-sample threshold.

The final training data should be checked for duplicates, invalid ranges, inconsistent records and data leakage before a formal model evaluation. Any dataset-specific filtering choices should be documented alongside the final training run.

## 5.3 Brand Prediction Implementation

The brand-prediction page accepts product characteristics through an HTML form. The Django view reads the submitted values, converts numeric attributes to floating-point values and normalizes categorical inputs against known choices. It checks the entered price, RAM and storage against configured bounds and checks whether the selected CPU, operating system and graphics values are compatible with known brand rules.

When the values pass validation, the view constructs a one-row pandas DataFrame in the feature order expected by the brand classifier. The encoders transform CPU, operating system and graphics values, and the classifier returns a brand class. The application can also retrieve class probabilities, sort them and present the top results. Country labels and map coordinates are selected from local mappings; an external map preview requires the relevant configuration.

## 5.4 Price Prediction Implementation

The price-prediction page provides choices for brand, CPU, operating system and graphics and accepts numeric characteristics such as rating, screen size, storage, RAM, CPU speed and total sales. The Django view parses submitted values, applies input checks and transforms categorical values with the encoders used for the price model.

The prepared feature row is passed to the Random Forest regressor. The numerical output is rendered as an estimated price in Indian rupees. The model estimates a relationship learned from the training dataset and should not be treated as a guaranteed current market quote.

## 5.5 Authentication and Account Features

The project includes views and routes for user registration, email verification, resending verification messages, login, logout, forgotten-password requests and password resets. Django's authentication framework and token-generation utilities support these flows. Email delivery requires working SMTP settings in the deployment environment.

## 5.6 Design Patterns in the Data Pipeline

The project documents ten design patterns in the supporting pipeline:

### Creational patterns

1. **Singleton:** `ModelRepository` centralizes model and encoder artifact loading and saving.
2. **Factory Method:** `CleanerFactory` selects a cleaner implementation based on the dataset source.
3. **Builder:** `ModelBuilder` configures and constructs a Random Forest classifier.

### Structural patterns

4. **Adapter:** `DatasetAdapter` maps dataset-specific columns into a common schema.
5. **Facade:** `LaptopPredictor` provides a simplified prediction interface over model loading and encoding.
6. **Decorator:** `LoggingCleaner` adds timing and logging behavior around a cleaner.

### Behavioral patterns

7. **Strategy:** Cleaning strategies provide interchangeable parsing behavior for fields such as currency and storage.
8. **Observer:** `PipelineEventBus` notifies observers when a pipeline stage completes.
9. **Command:** Cleaning, training and saving operations are represented as command objects.
10. **Template Method:** Dataset-specific cleaners share a common cleaning sequence while implementing source-specific steps.

These patterns are demonstrated in the project pipeline. They should be understood as the design used in those modules; they do not imply that every model inference request runs through every pattern.

## 5.7 Deployment

The repository includes Render-oriented deployment configuration. The application can be served through Gunicorn, with WhiteNoise handling static files. A production deployment requires correct environment variables, dependency versions, allowed-host configuration, a strong secret key, email settings where account mail is enabled and optional map configuration where map functionality is enabled.

Before release, verify that all required model artifacts are present in the deployment build and are compatible with the installed scikit-learn version. Dataset files and model artifacts should be handled according to their size, licensing and deployment-storage requirements.

---

# CHAPTER 6
# SYSTEM TESTING

## 6.1 Testing Objectives

Testing checks that the application renders its main pages, accepts valid input, handles invalid or missing input and integrates the forms with the prediction logic. Testing also checks that optional integrations have a usable fallback when required external configuration is unavailable.

## 6.2 Testing Approach

- **Black-box testing:** Checks visible pages, forms, navigation, validation messages and rendered predictions.
- **White-box testing:** Checks internal validation branches, feature compatibility, choice normalization and fallback behavior.
- **Integration testing:** Checks that Django views, model artifacts and encoders work together for prediction requests.
- **Regression testing:** Re-runs the Django test suite after changes to views, templates or prediction logic.

## 6.3 Test Environment

The project uses Django's test framework and the application's configured Python dependencies. Tests issue requests through Django's test client and check response status, template content, context values and validation outcomes. Prediction tests depend on the model artifacts being available and loadable.

## 6.4 Representative Test Cases

| Test ID | Test case | Expected result |
|---|---|---|
| TC-01 | Request the home page | The page renders successfully for an appropriately authenticated user. |
| TC-02 | Request the price-prediction page | The page renders with the prediction form. |
| TC-03 | Request the design-pattern page | The page renders the design-pattern information. |
| TC-04 | Submit valid brand-prediction data | A prediction response is rendered with a brand result. |
| TC-05 | Submit valid brand-prediction data | The response includes country information and top-class output where available. |
| TC-06 | Submit nonnumeric brand-prediction data | The application renders an error state instead of treating the request as a valid prediction. |
| TC-07 | Omit a required brand-prediction field | The application reports the invalid request without an unhandled page failure. |
| TC-08 | Submit a configuration with incompatible features | The application reports that the selected configuration is not accepted. |
| TC-09 | Submit valid price-prediction data | The application returns a rendered price estimate. |
| TC-10 | Submit unrealistic numerical values | The application rejects the values or returns a validation error. |
| TC-11 | Load a page without map configuration | The application remains usable and shows its fallback behavior. |
| TC-12 | Exercise account routes | Registration and authentication routes return the expected response for the tested state. |

## 6.5 Test Results

The repository's QA report records **71 Django tests** covering routes, validation logic and frontend flows. It reports that an early run had one environment-specific assertion failure and that the final run passed after the assertion was adjusted in the validated environment. The QA report also records positive checks for form rendering, valid predictions, error handling and navigation.

For an academic submission, attach or reproduce the output from the final test run against the exact code revision being submitted. The repository's QA summary is documentation evidence; it is not a substitute for rerunning the tests in the final submission environment.

## 6.6 Model Evaluation

The price-model training script computes Mean Absolute Error (MAE), R-squared and Mean Absolute Percentage Error (MAPE) on a held-out test partition. The brand-training workflow computes classification accuracy and feature importance. Numerical results should be copied from a reproducible final training run and reported together with dataset size, split strategy and model configuration.

No numeric model score is asserted in this report because the training output values were not confirmed from a final, documented run. UI display values should not be used as experimental results unless they can be traced to the same model artifact and evaluation dataset.

## 6.7 Defect Summary

The existing IEEE 829-style defect report records four frontend defects: two marked closed and two marked open. The open items concern improving client-side validation feedback and making form-error styling clearer. It also records a map-preview dependency on an API key and backend-first validation messages as observed UX considerations.

The same QA document estimates a frontend defect density of 3.33 defects per KLOC and productivity of 100 LOC per hour, based on its stated frontend scope and effort assumptions. These are project estimates and should be presented as such, not as independently measured product-wide metrics.

## 6.8 Testing Limitations

- Model-quality tests depend on the availability and provenance of training data.
- A successful form test does not prove that a prediction is accurate for current products.
- External email and map integrations may not be fully testable without valid service configuration.
- A single held-out split may not reveal variation across brands, price bands or time periods.
- Test results should be rerun after model artifacts or dependencies are changed.

---

# CHAPTER 7
# CONCLUSION

LaptopPilot demonstrates how machine learning can be integrated into a web application for laptop brand classification and price estimation. The project brings together data cleaning, feature preparation, categorical encoding, Random Forest training, artifact persistence, Django request handling and browser-based forms. It also includes account-related functionality, validation, compatibility checks and a supporting design-pattern pipeline.

The project meets its primary implementation objective by providing two model-driven prediction workflows through a single web application. The brand classifier returns a predicted brand and class-score information where available, while the price regressor returns an estimated price based on the supplied attributes. Automated tests and QA documents provide evidence of the principal application flows and known defects.

The predictions should be interpreted as estimates learned from historical dataset examples. The system does not query a live retailer catalogue, and model reliability depends on data quality, feature availability and the match between training examples and the configuration being evaluated. Before the application is used for decisions beyond demonstration, the project should document the dataset's provenance, rerun model evaluation on a finalized dataset, review potential leakage and maintain the model as market data changes.

---

# CHAPTER 8
# APPLICATION SCREENSHOTS

Insert screenshots captured from the final running version of LaptopPilot. Use screenshots from the actual application rather than recreated or illustrative images.

## 8.1 Home Page and Brand Prediction Form

**Figure 8.1: LaptopPilot home page and brand-prediction form**  
Insert a screenshot showing the form fields and primary navigation.

## 8.2 Brand Prediction Result

**Figure 8.2: Brand prediction result with confidence scores**  
Insert a screenshot of a valid result. Ensure that any displayed sample values are clearly identified as demonstration data.

## 8.3 Price Prediction Page

**Figure 8.3: Laptop price-prediction form**  
Insert a screenshot showing the configuration fields for the price estimate.

## 8.4 Price Prediction Result

**Figure 8.4: Estimated price result**  
Insert a screenshot showing the rendered estimate and its currency.

## 8.5 Validation Error State

**Figure 8.5: Example validation feedback**  
Insert a screenshot showing how the application responds to an invalid or incompatible configuration.

## 8.6 Login and Account Pages

**Figure 8.6: Login or registration page**  
Insert a screenshot of the account interface. Do not include real email addresses, passwords, tokens or other personal information.

## 8.7 Design Patterns Page

**Figure 8.7: Design-pattern information page**  
Insert a screenshot of the page describing the implemented patterns.

---

# CHAPTER 9
# FUTURE ENHANCEMENTS

The following enhancements could improve the accuracy, maintainability and practical usefulness of LaptopPilot:

1. **Document data provenance:** Record the original source, collection date, licensing, geographic scope and limitations of each dataset.
2. **Refresh market data:** Add a controlled process for importing current product listings and retraining models as prices and product ranges change.
3. **Review feature leakage:** Evaluate whether total sales is appropriate and available at prediction time; compare models with and without it.
4. **Improve categorical representations:** Compare label encoding with one-hot encoding, target encoding or models designed to handle categorical variables.
5. **Use stronger evaluation protocols:** Apply cross-validation, temporal holdouts and per-brand/per-price-band metrics to test generalization.
6. **Report uncertainty:** Provide calibrated intervals or uncertainty estimates for price predictions rather than only a point estimate.
7. **Explain predictions:** Add feature-contribution explanations so users can understand which attributes most influenced an estimate.
8. **Improve validation UX:** Add client-side input assistance while retaining server-side validation as the source of truth.
9. **Internationalize price handling:** Support live or dated exchange-rate conversion, additional currencies, regional taxes and localization.
10. **Expand catalogue coverage:** Add additional brands, product generations and normalized component taxonomies.
11. **Strengthen model operations:** Version model artifacts, record training metadata and provide a safe model update and rollback workflow.
12. **Improve deployment observability:** Add structured logging, health checks, error monitoring and latency measurements.
13. **Review account security:** Use deployment-managed secrets, enforce secure transport, review email verification and password-reset behavior, and conduct a security assessment before public use.
14. **Add accessibility and responsive checks:** Verify keyboard operation, screen-reader labels, contrast and layouts across mobile and desktop browsers.
15. **Expand automated tests:** Add coverage for boundary values, authentication permissions, email flows, artifact loading, regression behavior and model-input schema compatibility.

---

# CHAPTER 10
# REFERENCES

1. L. Breiman, “Random Forests,” *Machine Learning*, vol. 45, pp. 5–32, 2001. DOI: [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324).
2. scikit-learn Developers, “RandomForestClassifier,” *scikit-learn API Documentation*. Available: [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).
3. scikit-learn Developers, “RandomForestRegressor,” *scikit-learn API Documentation*. Available: [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html).
4. scikit-learn Developers, “Model evaluation: quantifying the quality of predictions,” *scikit-learn User Guide*. Available: [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html).
5. Django Software Foundation, “Django documentation.” Available: [https://docs.djangoproject.com/](https://docs.djangoproject.com/).
6. The pandas Development Team, “pandas documentation.” Available: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/).
7. NumPy Developers, “NumPy documentation.” Available: [https://numpy.org/doc/](https://numpy.org/doc/).
8. Joblib Developers, “Persistence utilities.” Available: [https://joblib.readthedocs.io/en/latest/persistence.html](https://joblib.readthedocs.io/en/latest/persistence.html).
9. Django Software Foundation, “Testing in Django.” Available: [https://docs.djangoproject.com/en/stable/topics/testing/](https://docs.djangoproject.com/en/stable/topics/testing/).
10. LaptopPilot project source code and project documentation, including the data-cleaning and training scripts, Django application, QA test report and defect report. Repository: [https://github.com/Chandan1303/laptop-ML-model](https://github.com/Chandan1303/laptop-ML-model).

> Add the exact original dataset citations and access dates after verifying the dataset provider and its terms of use. Do not cite a dataset merely from its local filename.
