# RTRP_AgroSense_Tomato_Forecaster
AgroSense: An end-to-end MLOps pipeline for real-time tomato price scraping and 30-day forecasting using Selenium, ARIMA, and GRU models.

# AgroSense: Intelligent Price Prediction & Market Analytics

## Abstract
AgroSense is an end-to-end MLOps pipeline designed to stabilize agricultural market awareness through data-driven price forecasting. [cite_start]The system utilizes Selenium-based web scraping to ingest real-time commodity data, augmented by historical datasets to train ARIMA and GRU models for 30-day price projections[cite: 7, 9].

## Architecture
[cite_start]The system follows a three-stage MLOps lifecycle[cite: 16]:
1. [cite_start]**Data Ingestion**: Selenium WebDriver extracts real-time attributes (Price, Market, Date)[cite: 19, 20].
2. [cite_start]**Backend**: Data cleaning via Pandas and normalization using MinMaxScaler[cite: 17, 21].
3. [cite_start]**Forecasting**: Baseline ARIMA model for linear trends and RNN (GRU) for non-linear price forecasting[cite: 25, 26].

## Societal Impact
[cite_start]AgroSense supports **SDG 12: Responsible Consumption and Production** by minimizing agricultural food waste through demand forecasting and ensuring market price transparency[cite: 29, 30].

## Tech Stack
- **Language**: Python
- **Automation**: Selenium WebDriver
- **ML Models**: ARIMA, GRU (TensorFlow/Keras)
- **Data Tools**: Pandas, NumPy, Scikit-learn
- **Visualization**: Matplotlib, Plotly
