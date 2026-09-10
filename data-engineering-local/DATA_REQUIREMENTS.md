# Automatic Block Planning System
## Data Engineering Requirements

This document defines the data required from the railway systems
for the Automatic Block Planning System.

---

## 1. TMS - Track Management System

Purpose:
Provides Engineering department maintenance and track defect information.

Required fields:

- task_id
- asset_id
- section_id
- defect_type
- severity
- reported_date
- due_date
- maintenance_duration
- status

---

## 2. SMMS - Signalling Maintenance & Management System

Purpose:
Provides Signal and Telecommunication maintenance information.

Required fields:

- task_id
- asset_id
- section_id
- fault_type
- severity
- reported_date
- due_date
- maintenance_duration
- status

---

## 3. TDMS - Traction Distribution Management System

Purpose:
Provides Traction Distribution/OHE maintenance information.

Required fields:

- task_id
- asset_id
- section_id
- equipment_type
- fault_type
- severity
- reported_date
- due_date
- maintenance_duration
- status

---

## 4. BDMS - Block Demand Management System

Purpose:
Provides maintenance block requests from different departments.

Required fields:

- block_request_id
- task_id
- department
- section_id
- requested_date
- requested_start
- requested_end
- duration
- reason

---

## 5. COA - Control Office Application

Purpose:
Provides train movement, timetable and corridor-related information.

Required fields:

- train_id
- train_type
- section_id
- arrival_time
- departure_time
- train_priority
- date

---

## Data Engineering Objective

The Data Engineering module will:

1. Collect data from TMS, SMMS, TDMS, BDMS and COA.
2. Clean the raw data.
3. Validate the data.
4. Standardize different formats.
5. Remove duplicate and invalid records.
6. Integrate data from multiple systems.
7. Create unified datasets.
8. Provide clean data to the AI/ML module.
9. Provide clean data to the Railway Optimization module.
10. Store processed data in the project database.