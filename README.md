# INFS4205 Taxi Trajectory Analysis Project (2025)

**Author:** Xiaoyu Zhuang  
**Course:** INFS4205/7205 Advanced Techniques in High Dimensional Data, Semester 1, 2025

---

## 📌 Project Overview

This project benchmarks and analyses **spatio-temporal queries, skyline queries, and trajectory similarity analysis** on **large-scale Porto Taxi Trajectory data** using **PostgreSQL with PostGIS**, fulfilling the **INFS4205/7205 Type I Individual Project** requirements.

### 🎯 Key Components

- **Spatio-Temporal Query:** Retrieve taxi trips within defined **spatial regions** during **specific time windows**, using functions like `ST_CoveredBy`, `ST_Contains`, `ST_StartPoint`, and `ST_EndPoint`.
- **Skyline Query:** Find **non-dominated trajectories** that balance travel time and distance using SQL CTEs and self-joins.
- **Trajectory Similarity Analysis:** Identify **top-5 similar trajectories** using the **Fast Dynamic Time Warping (FastDTW)** algorithm with a **PostgreSQL UDF**.
- **Indexing Strategy Exploration:** Evaluate and compare **B-tree, GiST, and SP-GiST** indexing to measure their impact on **query performance**.

---

## 📂 Dataset

- **Porto Taxi Trajectory Dataset:** [Taxi Trajectory Data](https://www.kaggle.com/datasets/crailtap/taxi-trajectory)
- Contains over **1.7 million GPS trajectories (2013-2014)** with timestamps for **high-dimensional spatio-temporal analysis**.
- Data preprocessed to extract:
  - Valid `LINESTRING` geometries
  - Timestamps in UTC and local Lisbon time
  - Derived attributes including `hour_of_day`, `point_count`, and `total_travel_time`.

---

## 🛠️ Environment Requirements

- **Python 3.x**
- PostgreSQL with PostGIS and `plpython3u` enabled.
- Required Python packages:
  ```bash
  pip install pytz numpy scipy fastdtw
  ```

---

## 🚀 Setup & Execution

### 1️⃣ Data Preprocessing

Run the provided script to convert raw CSV into a **cleaned CSV** compatible with PostGIS:
```bash
python data_preprocessing.py
```

### 2️⃣ Database Setup

1. **Create the database:**
    ```sql
    CREATE DATABASE porto_taxi_trajectory;
    ```
2. **Connect to the database:**
    ```bash
    \c porto_taxi_trajectory
    ```
3. **Enable necessary extensions:**
    ```sql
    CREATE EXTENSION postgis;
    CREATE EXTENSION plpython3u;
    ```
4. **Create the table:**
    ```sql
    DROP TABLE IF EXISTS taxi_trajectory;
    CREATE TABLE taxi_trajectory (
        trip_id BIGINT,
        call_type CHAR(1),
        origin_call INTEGER,
        origin_stand INTEGER,
        taxi_id INTEGER,
        day_type CHAR(1),
        missing_data BOOLEAN,
        polyline GEOMETRY(LINESTRING, 4326),
        timestamps TIMESTAMP WITH TIME ZONE[],
        total_travel_time INTEGER,
        start_local_time TIMESTAMP WITHOUT TIME ZONE,
        end_local_time TIMESTAMP WITHOUT TIME ZONE,
        hour_of_day INTEGER,
        point_count INTEGER
    );
    ```
5. **Insert the data:**
    ```sql
    COPY taxi_trajectory
    FROM '<PATH TO YOUR train_preprocessed.csv>'
    WITH (
        FORMAT csv,
        HEADER,
        DELIMITER ',',
        NULL ''
    );
    ```

The `queries.sql` file includes:
- Table creation
- Index creation (B-tree, GiST, SP-GiST)
- Data insertion
- Spatio-temporal, skyline, and trajectory similarity queries
- `EXPLAIN (ANALYZE, BUFFERS)` outputs for benchmarking

---

## 📈 Results & Reflection

- Achieved efficient **query filtering using combined temporal and spatial indexing**.
- Demonstrated **FastDTW feasibility on large trajectory data** within PostgreSQL.
- Identified that **GiST indexing benefits range queries**, while **SP-GiST can accelerate start/end point searches** in uniform distributions.
- Full analysis and experimental results are documented in `INFS4205_Report_Xiaoyu_Zhuang.pdf`.

---

## 📎 File Structure

```
.
├── data_preprocessing.py                 # Python script for data cleaning and preparation
├── queries.sql                           # PostgreSQL setup, indexing, and queries with EXPLAIN outputs
└── INFS4205_Report_Xiaoyu_Zhuang.pdf     # Full report for result analysis
```

---

## 📬 Reproduction & Sharing

If you wish to replicate or extend, please:
- Use the same environment settings and dataset.
- Follow the step-by-step commands above.
- This report is **ONLY** shared for peer learning only. **It must NOT be submitted, in whole or in part, for any assignments in any course or academic setting.**

All rights to the contents of this project are reserved by the author unless explicitly stated otherwise. The SQL structure template were provided by the INFS4205/7205 teaching team for assessment purposes.

---
