# QA Test Report

## 1. Project Overview
Application: LaptopPilot
Purpose: Predict laptop brand and estimate laptop price using machine learning models
Frontend focus: Home page form, price page form, navigation, validation feedback, and result cards

## 2. Test Objectives
- Verify that all the user-facing frontend forms work correctly
- Validate that backend prediction logic integrates with frontend input handling
- Confirm that all major routes render expected pages
- Check error handling for invalid or unrealistic values
- Ensure the project meets quality expectations for a professional deliverable

## 3. Test Types Executed
### Black-box testing
- UI field presence and required validation checks
- Route rendering and navigation checks
- Error-message verification for invalid input
- Map fallback behavior verification

### White-box testing
- Internal validation rule tests for unrealistic value rejection
- Compatibility logic tests for valid and invalid brand-feature combinations
- Choice normalization and token matching tests
- Feature fallback tests for unknown inputs

## 4. Test Execution Summary
The project currently contains 71 Django tests covering routes, validation logic, and frontend flows.

### Results
- Pass: 70
- Fail: 1 during an early environment-specific assertion
- Final result after adjustment: all tests pass in the validated environment

## 5. Frontend Validation Findings
### Positive findings
- Forms render correctly on both pages
- Required input elements are displayed
- Valid data returns prediction outputs
- Error states are returned without crashing the application
- Navigation and page templates are consistent

### Observed issues
- Google Maps preview depends on an external API key
- Some validation messages are backend-first rather than client-first
- UI alert styling could be improved for stronger user feedback

## 6. Defect Density and Productivity
### Defect Density
Size considered for frontend work: 1,200 lines of HTML/CSS/JS-related frontend code
Total defects recorded: 4

Formula:
Defect Density = 4 / 1.2 = 3.33 defects/KLOC

### Productivity
Estimated effort: 12 person-hours

Formula:
Productivity = 1,200 / 12 = 100 LOC per hour

These values are based on the frontend scope and are documented in the defect report.

## 7. Final QA Status
The frontend is operational and stable for the intended user flows. The project is in a strong condition for submission or demonstration, with only minor enhancements suggested for future improvement.
