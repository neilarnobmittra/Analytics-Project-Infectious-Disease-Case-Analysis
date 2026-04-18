# COVID-19 Early Case Trend Analysis & Recovery Insights Dashboard

**A Professional Kivy-based GUI Dashboard for COVID-19 Patient Data Analysis & Recovery Prediction**

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Kivy](https://img.shields.io/badge/GUI-Kivy-2.3.1-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Project Overview

This project is a **complete interactive desktop dashboard** developed as part of my **Artificial Intelligence Minor Project**. It analyzes real COVID-19 patient data, generates insightful visualizations, and builds a **Linear Regression model** to predict recovery days.

The application provides a clean, modern, and professional user interface with five tabs, side-by-side graphs, key insights, and a fully scrollable regression summary.

**Submitted by:** Neilarnob Mittra  
**Date:** March 2026

---

## ✨ Key Features

- **Professional GUI** built with Kivy framework
- **Easy CSV Upload** with popup interface
- **Processing Popup** for smooth user experience during analysis
- **Five Interactive Tabs**:
  - Dashboard (Key Insights)
  - Demographics
  - Infection Spread
  - Recovery Trends
  - **Regression Model** (with side-by-side graphs + scrollable full OLS summary)
- **Dark Blue Theme** with Dark Orange text for premium look
- **Side-by-Side Graphs** in every tab (Matplotlib + Seaborn)
- **Linear Regression Model** using Statsmodels (predicts recovery days)
- **Fast Analysis** with optimized plot settings
- **Automatic Plot Saving** to `plots/` folder
- **Fully Scrollable Regression Summary**

---

## 🛠 Technology Stack

- **Language**: Python 3.11
- **GUI Framework**: Kivy 2.3.1
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Statistical Modeling**: Statsmodels (OLS Regression)
- **Others**: Kivy Clock, FileChooser, ScrollView, Popup

---

## 📊 Dataset

- **File**: `patient (1).csv`
- **Rows**: ~4000+ real COVID-19 patient records
- **Columns**: `id, sex, birth_year, country, region, infection_reason, infection_order, contact_number, confirmed_date, released_date, deceased_date, state`
- **Engineered Features**: `age`, `age_group`, `recovery_days`

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/covid-dashboard.git



   Install required packages:Bashpip install kivy pandas numpy matplotlib seaborn statsmodels
Run the application:Bashpython main.py
Click UPLOAD CSV FILE → select patient (1).csv
Click RUN FULL ANALYSIS
Explore all tabs (especially Regression Model tab)
   cd covid-dashboard

   Project Structure
   covid-dashboard/
├── main.py                    
├── patient (1).csv           
├── plots/                     
│   ├── gender.png
│   ├── age.png
│   ├── region.png
│   ├── residual_hist.png
│   ├── residual_scatter.png
│   └── ...
├── regression_summary.txt    
└── README.md

🔍 Regression Model Details
The Regression Model uses Ordinary Least Squares (OLS) to predict recovery_days based on:

age
contact_number
infection_order

Output includes:

R² Score
Two residual plots (side-by-side)
Full statistical summary (scrollable in the app)


🎯 Learning Outcomes

Data cleaning and feature engineering
Exploratory Data Analysis (EDA)
Data visualization best practices
Linear Regression modeling
Building professional GUI applications with Kivy
Creating scrollable and responsive layouts
Writing clean, maintainable Python code


🔮 Future Enhancements (Planned)

One-click PDF report generation
Date range filter
More ML models (Random Forest, XGBoost)
Patient search functionality
Dark/Light theme toggle
Deploy as standalone .exe file


📄 License
This project is open for educational purposes. Feel free to use it for learning or as a base for your own projects.

Made with ❤️ by Neilarnob Mittra
If you find this project useful, please give it a ⭐ on GitHub!
