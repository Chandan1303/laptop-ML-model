# Defect Life Cycle Table

## Defect States and Actions

| Stage | Name | Description | Responsible Role | Typical Action |
|---|---|---|---|---|
| 1 | New | Defect is reported after test execution or user observation | Tester / QA | Record in defect tracking log |
| 2 | Assigned | Defect is assigned to the responsible developer | Developer / Team Lead | Analyze and start fix |
| 3 | Open | Defect is being investigated | Developer | Confirm root cause and impact |
| 4 | In Progress | Fix is being implemented | Developer | Modify code, update tests |
| 5 | Fixed | Fix is implemented and made available in the branch | Developer | Verify with targeted tests |
| 6 | Retest | The fix is re-tested by QA | Tester | Validate actual behavior |
| 7 | Verified | The defect is confirmed resolved | QA Lead | Close the defect |
| 8 | Reopened | The defect reappears or fix is incomplete | QA / Developer | Reinvestigate and patch |
| 9 | Closed | No further action required | QA Lead | Mark final status |
| 10 | Deferred | Not fixed in current release due to priority or scope | Project Manager | Schedule for later sprint |

## Frontend Defect Life Cycle Example

| Defect ID | Initial State | Current State | Days in State | Notes |
|---|---|---|---:|---|
| DEF-001 | New | Closed | 3 | Invalid numeric input handling documented and verified |
| DEF-002 | New | Closed | 2 | Map fallback behavior confirmed under no API key |
| DEF-003 | New | Deferred | 5 | Client-side validation enhancement is planned for future UI improvement |
| DEF-004 | New | Open | 1 | Validation styling improvement is backlogged |

## Defect Lifecycle Notes
- The frontend defect life cycle follows a standard QA workflow from detection to closure.
- High-priority functional issues move through validation quickly.
- Cosmetic or low-priority UI defects may be deferred depending on release goals.
- Product quality is improved when each defect is tracked until closure or formal deferral.
