import streamlit as st

st.set_page_config(page_title="YMCA Dashboard", layout="wide")

st.title("🏊‍♂️ YMCA Member Insights Dashboard")

st.write("""
Welcome to the YMCA Membership Insights Dashboard.

This dashboard was developed as part of the **CMPT 3830 Machine Learning Work-Integrated Project** 
to help YMCA better understand membership behaviour and identify meaningful patterns using data-driven insights.

---
### 📌 What You Can Do Here

Use the sidebar to navigate through:

1. **📄 Data Overview**  
   Preview the cleaned dataset used in analysis.

2. **📊 Insights Summary**  
   Key metrics such as member counts, cluster distribution, and membership patterns.

3. **📈 Visualizations**  
   Interactive charts showing age groups, cluster breakdowns, durations, and more.

4. **🎯 Recommendations**  
   Actionable interpretations based on derived clusters and trends.

---

### 🧠 Project Objective

The goal of this project is to:

- Understand how members behave based on usage patterns  
- Group similar users into behaviour clusters  
- Provide insights YMCA can use to improve programs, retention, and engagement  

---

### 📂 Dataset Version

✔ The dataset used is: **ymca_clusters.csv**

---

If you are ready, use the menu on the left to begin! 🚀
""")
