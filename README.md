# MIG Cement Operational Planner & Demand Forecasting

An enterprise-grade operational analytics and inventory planning system built for **MIG Cement**, designed to transition site operations from reactive ordering to data-driven, automated demand forecasting and inventory simulation.

---

## 🚀 Project Overview
Managing bulk cement inventory across multiple regional sites requires balancing two costly extremes: running out of stock (causing site shutdowns) or holding too much inventory (tying up working capital and risking product degradation). 

This project implements an end-to-end machine learning pipeline and an interactive stakeholder dashboard that predicts daily cement consumption across **30 operational sites** and simulates silo inventory levels, delivery lead times, and weather-adjusted safety buffers.

---

## 🏆 Key Architecture & Model Comparison
We evaluated **CatBoost** as our primary predictive engine against **Random Forest** as our benchmarking model across a chronological holdout of **6,540 site-days** (28 May – 31 December 2024).

| Evaluation Metric | CatBoost (Primary) | Random Forest (Benchmark) | Performance Gain |
| :--- | :---: | :---: | :---: |
| **MAE** (Average Daily Miss) | **0.73 tonnes** | 0.87 tonnes | **16.0% lower error** |
| **RMSE** (Large-Error Penalty) | **1.75 tonnes** | 1.99 tonnes | **12.3% better stability** |
| **MAPE** (Percentage Error on Active Days) | **2.70%** | 3.72% | **27.4% lower error** |

* **Why CatBoost?** CatBoost outperformed Random Forest by handling complex site-level features natively, adapting smoothly to sharp demand spikes (such as large slab pours), and minimizing extreme prediction errors.

---

## 📊 Interactive Stakeholder Dashboard
The project features a live, glass-morphism web application built using **Dash**, **Plotly**, and **Bootstrap**:
* **Site Selector:** Switch instantly between all 30 operational sites.
* **KPI Summary Cards:** Monitor total forecasted consumption, planned reorders, average inventory levels, and capacity utilisation.
* **Inventory & Demand Timeline:** Visualises simulated silo stock levels, daily demand bars, silo capacity thresholds, and exact reorder trigger points.
* **Delivery Schedule:** Reviews recommended delivery dates, quantities, and wet-weather buffer flags.
