# Defect Report (IEEE 829 Format)

## 1. Test Plan Identification
Project: LaptopPilot Web Application
Project Type: Frontend + Django ML Prediction UI
Report Date: 2026-09-23
Prepared By: QA and Software Testing Team

## 2. Test Item(s)
The following frontend and UI flows were evaluated:
- Home page brand prediction form
- Price prediction page
- Navigation and route rendering
- Form validation and error handling
- Map fallback behavior when no Google Maps API key is configured
- Output rendering of prediction results and confidence scores

## 3. Features to be Tested
- Brand prediction form interaction
- Price prediction form interaction
- Real-world validation checks
- Error response handling in the UI
- Template rendering and route health
- Frontend responsiveness and user feedback

## 4. Test Approach
The project was validated using:
- Black-box testing to check user-visible behavior
- White-box testing to confirm internal validation logic and branch handling
- Django test suite execution for functional verification

## 5. Item Pass/Fail Criteria
A test item passes if:
- The page loads with expected UI sections
- Required inputs are present and correctly validated
- Valid inputs produce result cards and model outputs
- Invalid inputs trigger a meaningful user-facing error message
- The app does not crash or render broken UI

## 6. Defect Log

| Defect ID | Severity | Priority | Module/Screen | Description | Root Cause | Status | Resolution |
|---|---|---:|---|---|---|---|---|
| DEF-001 | Medium | High | Home page | No explicit frontend validation for invalid numeric input beyond backend error response | Input validation handled on server side without stronger UI messaging | Closed | Added QA tests and documented validation behavior |
| DEF-002 | Low | Medium | Price prediction page | Google Maps preview depends on API key availability | Map feature is environment-dependent | Closed | Fallback text added and environment-aware test implemented |
| DEF-003 | Medium | Medium | Form logic | Brand and price prediction forms rely on backend-driven validation messages | User experience can be improved with client-side validation | Open | Recommended enhancement for future sprint |
| DEF-004 | Low | Low | Templates | Form error states need clearer visual distinction | CSS styling is minimal for validation alert states | Open | UI improvement backlog item |

## 7. Summary of Defect Metrics

- Total defects found: 4
- Defects resolved: 2
- Defects open: 2
- Severity distribution:
  - Critical: 0
  - High: 0
  - Medium: 2
  - Low: 2

## 8. Defect Density Calculation
For the frontend scope, the app includes approximately 1,200 lines of UI-related code across templates and CSS.

Formula:
Defect Density = Total Defects / Size in KLOC

Calculation:
Defect Density = 4 / 1.2 = 3.33 defects per KLOC

This reflects the frontend experience and forms used in the brand and price prediction pages.

## 9. Productivity Calculation
Front-end QA effort for this project was estimated at 12 person-hours across the testing cycle.

Formula:
Productivity = Size / Effort

Calculation:
Productivity = 1,200 LOC / 12 hours = 100 LOC per hour

This estimate reflects the frontend work completed across the interactive pages, forms, and output components.

## 10. Defect Reporting Notes
- Defects were logged against actual user-facing frontend flows.
- The report is structured in conformance with IEEE 829 expectations for test reporting.
- The defect log includes severity, priority, description, root cause, status, and closure details.

## 11. Overall QA Status
The frontend is functionally stable for the tested user journeys, with minor enhancement opportunities for richer validation UX and stronger client-side feedback.
