# Data Engineering Report
## Automatic Block Planning System

---

## 1. Overview

The Data Engineering module is responsible for collecting, cleaning, validating, transforming, integrating, and preparing railway maintenance data for AI/ML and optimization.

The module acts as the bridge between railway source systems and the AI/ML and Railway Optimization modules.

---

## 2. Data Sources

The system integrates data from the following railway systems:

### TMS - Track Management System
Provides track maintenance information such as:

- Track defects
- Asset information
- Section information
- Severity
- Due dates
- Maintenance duration
- Maintenance status

### SMMS - Signalling Maintenance & Management System
Provides signalling maintenance information such as:

- Signal faults
- Point machine faults
- Track circuit failures
- Severity
- Due dates
- Maintenance duration
- Maintenance status

### TDMS - Traction Distribution Management System
Provides traction maintenance information such as:

- OHE faults
- Insulator damage
- Transformer issues
- Contact wire wear
- Severity
- Due dates
- Maintenance duration
- Maintenance status

### BDMS - Block Demand Management System

Provides maintenance block requests including:

- Block request ID
- Maintenance task ID
- Department
- Section
- Requested date
- Requested start time
- Requested end time
- Block duration
- Maintenance reason

### COA - Control Office Application

Provides train movement information including:

- Train ID
- Train type
- Section
- Arrival time
- Departure time
- Train priority
- Date

### Corridor Data

Provides railway corridor information including:

- Section
- Start location
- End location
- Distance

### Block Window Data

Provides available maintenance windows including:

- Section
- Date
- Window start
- Window end
- Window duration
- Availability status

---

## 3. Data Engineering Pipeline

The complete pipeline follows this process:

Raw Railway Data
        ↓
Data Transformation
        ↓
Data Cleaning
        ↓
Data Validation
        ↓
Data Integration
        ↓
Train Activity Summary
        ↓
Priority Feature Engineering
        ↓
AI/ML Dataset
        ↓
Optimization Dataset
        ↓
Available Block Windows
        ↓
Task-Window Matching
        ↓
Train Conflict Checking
        ↓
Matching Score Calculation
        ↓
Optimization Input
        ↓
Optimization Handoff

---

## 4. Data Transformation

The transformation stage converts data from TMS, SMMS, TDMS, COA, and BDMS into standardized CSV datasets.

Maintenance records from TMS, SMMS, and TDMS are converted into a common maintenance structure.

This allows data from different railway departments to be processed together.

Current transformation result:

- TMS records: 12
- SMMS records: 12
- TDMS records: 12
- Total maintenance records: 36
- COA train records: 24
- BDMS block requests: 20

---

## 5. Data Cleaning

The cleaning stage removes invalid or inconsistent records and standardizes the data.

The cleaning process checks:

- Missing values
- Invalid values
- Data types
- Severity values
- Maintenance duration
- Department information

Current result:

- Records before cleaning: 36
- Records after cleaning: 36

---

## 6. Data Validation

Multiple validation scripts are used throughout the pipeline.

Validation checks include:

- Required columns
- Missing values
- Duplicate IDs
- Valid departments
- Valid severity levels
- Valid maintenance durations
- Valid block durations
- Valid section IDs
- Valid train activity information
- Valid corridor information

All current validation stages pass successfully.

---

## 7. Data Integration

Maintenance data, BDMS block requests, train activity summaries, and corridor information are integrated into a common dataset.

The integrated dataset provides a combined view of:

- Maintenance requirements
- Department
- Railway section
- Block requests
- Train activity
- Train priority
- Corridor information

Current result:

- Integrated maintenance records: 36
- BDMS requests: 20
- Train summary records: 9
- Corridor records: 6

---

## 8. Train Activity Summary

Train movement data is summarized by railway section and date.

The summary includes:

- Total train count
- High-priority train count
- First train arrival
- Last train departure

This information helps identify sections with high train activity.

The optimization process can use this information when selecting maintenance windows.

---

## 9. Maintenance Priority Features

Priority features are generated using maintenance and railway operational information.

The priority calculation considers:

- Maintenance severity
- Due date
- Overdue status
- Train activity
- High-priority train activity

Severity scores:

- Low = 1
- Medium = 2
- High = 3
- Critical = 4

Priority levels are generated as:

- Critical
- High
- Medium
- Low

Current priority distribution:

- Critical: 6
- High: 12
- Medium: 6
- Low: 12

---

## 10. AI/ML Ready Dataset

The AI-ready dataset contains standardized features that can be used by the AI/ML module.

The dataset contains:

- Task information
- Department
- Asset
- Section
- Maintenance type
- Severity
- Maintenance duration
- Status
- Days to due date
- Overdue indicator
- Severity score
- Urgency score
- Train activity score
- High-priority train score
- Priority score
- Priority level

Current result:

- Records: 36
- Features: 17

---

## 11. Optimization Dataset

The optimization dataset combines maintenance, block, train, corridor, and priority information.

It provides the Railway Optimization module with the information required for scheduling.

Current result:

- Records: 36
- Features: 31

---

## 12. Available Block Windows

Available block windows are filtered from the block-window dataset.

Only windows marked as available are retained.

Current result:

- Available windows: 18
- Total available time: 2550 minutes

---

## 13. Task-to-Window Matching

Each maintenance task is compared with available block windows.

A task can match a window when:

1. The railway section is the same.
2. The date is the same.
3. The available window is long enough for the maintenance.
4. The proposed maintenance period does not overlap with a train movement.

The system also calculates:

- Maintenance start time
- Maintenance end time
- Unused window time

Current result:

- Feasible task-window matches: 12
- Tasks with feasible windows: 6
- Train-conflict rejections: 0

---

## 14. Matching Score

Each feasible task-window combination receives a matching score.

The score considers:

- Maintenance priority
- Priority level
- Window efficiency
- Maintenance duration
- Available window duration

Higher scores indicate more suitable task-window combinations.

Current result:

- Candidates: 12
- Highest matching score: 103.00
- Lowest matching score: 61.50

---

## 15. Optimization Input

The optimization input dataset contains feasible task-window candidates prepared for the Railway Optimization module.

It contains:

- Task ID
- Department
- Section
- Priority score
- Priority level
- Maintenance duration
- Window date
- Window start
- Window end
- Window duration
- Unused window time
- Window efficiency
- Priority bonus
- Matching score

Current result:

- Candidates: 12
- Features: 14

---

## 16. Optimization Handoff

The final optimization handoff dataset is the output of the Data Engineering module.

It provides the Railway Optimization module with ranked scheduling candidates.

Current result:

- Tasks: 6
- Features: 13

Final output:

`processed/optimization_handoff.csv`

---

## 17. Validation Architecture

Validation is performed at multiple stages rather than only at the end.

This helps prevent incorrect data from moving into later modules.

Validation stages include:

1. Maintenance data validation
2. BDMS validation
3. Integrated data validation
4. Priority feature validation
5. AI dataset validation
6. Optimization dataset validation
7. Available window validation
8. Task-window match validation
9. Optimization candidate validation
10. Optimization input validation
11. Optimization summary validation
12. Optimization handoff validation

All current validation stages pass successfully.

---

## 18. Role of Data Engineering in the SIH Solution

The Data Engineering module provides the foundation for the Automatic Block Planning System.

It converts decentralized railway data into structured information that can be used by AI/ML and optimization algorithms.

The module performs:

**Collect → Clean → Transform → Integrate → Validate → Prepare → Handoff**

This enables the system to move from manual and decentralized planning toward data-driven automatic block planning.

---

## 19. Current Pipeline Statistics

| Dataset / Stage | Records |
|---|---:|
| TMS | 12 |
| SMMS | 12 |
| TDMS | 12 |
| Total Maintenance | 36 |
| COA | 24 |
| BDMS | 20 |
| Integrated Maintenance | 36 |
| Available Windows | 18 |
| Task-Window Matches | 12 |
| Optimization Candidates | 12 |
| Tasks with Feasible Windows | 6 |
| Final Handoff Tasks | 6 |

---

## 20. Final Status

The Data Engineering pipeline is fully executable through the master pipeline script:

`python scripts\run_pipeline.py`

The complete pipeline currently executes successfully without errors.

Final output:

`processed/optimization_handoff.csv`

The Data Engineering module is ready to provide structured scheduling candidates to the Railway Optimization module.