# Data Engineering Module

## Purpose

The Data Engineering module collects, cleans, validates, integrates, and prepares railway maintenance data for AI/ML and optimization.

## Data Sources

The system uses data from:

- TMS - Track Management System
- SMMS - Signalling Maintenance & Management System
- TDMS - Traction Distribution Management System
- BDMS - Block request data
- COA - Train movement data
- Corridor data
- Available block-window data

## Data Pipeline

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
Matching Score Calculation
        ↓
Optimization Input
        ↓
Optimization Handoff

## Main Outputs

### 1. maintenance_tasks.csv

Unified maintenance records from TMS, SMMS, and TDMS.

### 2. block_requests.csv

Maintenance block requests received through BDMS.

### 3. integrated_maintenance.csv

Integrated maintenance, block, train, and corridor information.

### 4. priority_features.csv

Maintenance tasks enriched with urgency, severity, train activity, and priority scores.

### 5. ai_ready_dataset.csv

Dataset prepared for AI/ML processing.

### 6. optimization_dataset.csv

Dataset containing maintenance, block, train, corridor, and priority information for optimization.

### 7. available_block_windows.csv

Available maintenance windows after filtering block-window data.

### 8. task_window_matches.csv

Possible matches between maintenance tasks and available block windows.

### 9. optimization_candidates.csv

Candidate task-window combinations with matching scores.

### 10. optimization_input.csv

Clean optimization input containing feasible task-window candidates.

### 11. optimization_summary.csv

Best available window selected for each task based on matching score.

### 12. optimization_handoff.csv

Final validated dataset handed over to the Railway Optimization module.

## Current Result

The pipeline currently produces:

- 36 integrated maintenance records
- 18 available block windows
- 12 feasible task-window candidates
- 6 tasks with feasible windows
- 13 fields in the final optimization handoff dataset

## Role in the SIH Solution

The Data Engineering module acts as the bridge between railway source systems and the AI/optimization modules.

It ensures that the optimization engine receives:

- Clean data
- Valid data
- Standardized data
- Integrated railway information
- Maintenance priorities
- Feasible block windows
- Ranked scheduling candidates