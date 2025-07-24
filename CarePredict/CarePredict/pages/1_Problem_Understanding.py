import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Problem Understanding", page_icon="🎯", layout="wide")

st.title("🎯 Problem Understanding")
st.markdown("---")

# Problem Statement Section
st.header("📋 Problem Statement")
st.markdown("""
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
<h3>🏥 Hospital Readmission Risk Prediction</h3>
<p><strong>Background:</strong> Hospital readmissions, especially among patients with chronic illnesses (like diabetes, heart disease, or hypertension), are a major challenge for the healthcare system. Early identification of patients at high risk of readmission allows providers to intervene and improve outcomes.</p>

<h4>Primary Objectives:</h4>
<ol>
<li>🔍 <strong>Explore key risk factors</strong> and trends that affect readmission</li>
<li>💡 <strong>Provide actionable recommendations</strong> for reducing unnecessary readmissions</li>
<li>🎯 <strong>Develop a predictive model</strong> to classify test results and identify high-risk patients</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Healthcare Domain Context
st.header("🏥 Healthcare Domain Context")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Current Challenges")
    st.markdown("""
    - **High Readmission Rates**: 30-day readmission rates can reach 15-20% for certain conditions
    - **Financial Impact**: Hospitals face penalties for excessive readmissions
    - **Patient Outcomes**: Readmissions often indicate inadequate initial care
    - **Resource Strain**: Emergency readmissions strain hospital resources
    - **Quality Metrics**: Readmission rates are key quality indicators
    """)

with col2:
    st.subheader("✅ Expected Benefits")
    st.markdown("""
    - **Cost Reduction**: Lower readmission rates reduce healthcare costs
    - **Improved Care**: Better patient outcomes and satisfaction
    - **Resource Optimization**: More efficient use of hospital resources
    - **Preventive Care**: Focus on preventive measures for high-risk patients
    - **Quality Improvement**: Enhanced overall healthcare quality metrics
    """)

# Dataset Overview
st.header("📊 Dataset Overview")

# Display dataset information
st.subheader("📋 Healthcare Dataset Information")
dataset_info = {
    "Dataset Name": "Healthcare Dataset",
    "Source": "Kaggle - prasad22",
    "Records": "10,000 synthetic patient records",
    "Purpose": "Multi-category classification problem",
    "Target Variable": "Test Results (Normal/Abnormal/Inconclusive)",
    "Data Type": "Synthetic healthcare data"
}

info_df = pd.DataFrame(list(dataset_info.items()), columns=['Attribute', 'Value'])
st.table(info_df)

# Data Schema
st.subheader("🗂️ Data Schema")
schema_data = {
    "Column Name": [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition",
        "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
        "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
        "Medication", "Test Results"
    ],
    "Data Type": [
        "Text", "Integer", "Categorical", "Categorical", "Categorical",
        "Date", "Text", "Categorical", "Categorical",
        "Float", "Integer", "Categorical", "Date",
        "Categorical", "Categorical"
    ],
    "Description": [
        "Patient name identifier",
        "Patient age in years",
        "Patient gender (Male/Female)",
        "Blood type (A+, B-, O+, etc.)",
        "Primary medical condition",
        "Hospital admission date",
        "Attending physician name",
        "Healthcare facility name",
        "Insurance provider name",
        "Total billing amount",
        "Assigned room number",
        "Type of admission (Emergency/Elective/Urgent)",
        "Hospital discharge date",
        "Prescribed medication",
        "Medical test results (Target variable)"
    ]
}

schema_df = pd.DataFrame(schema_data)
st.dataframe(schema_df, use_container_width=True)

# Problem Complexity Analysis
st.header("🧩 Problem Complexity Analysis")

complexity_tabs = st.tabs(["🎯 Classification Challenge", "📊 Data Challenges", "🏥 Domain Complexity"])

with complexity_tabs[0]:
    st.subheader("Multi-Class Classification Problem")
    st.markdown("""
    **Target Variable: Test Results**
    - **Normal**: Indicates healthy test results
    - **Abnormal**: Suggests potential health issues requiring attention
    - **Inconclusive**: Results that need further investigation
    
    **Classification Metrics to Consider:**
    - Accuracy across all three classes
    - Precision and Recall for each class
    - F1-Score for balanced performance
    - Confusion Matrix for detailed analysis
    """)
    
    # Visualization of classification challenge
    classes = ['Normal', 'Abnormal', 'Inconclusive']
    challenges = ['Clear Diagnosis', 'Requires Immediate Action', 'Needs Further Testing']
    colors = ['#2ecc71', '#e74c3c', '#f39c12']
    
    fig = go.Figure(go.Bar(
        x=classes,
        y=[1, 1, 1],
        marker_color=colors,
        text=challenges,
        textposition='inside'
    ))
    fig.update_layout(
        title="Test Result Classification Categories",
        xaxis_title="Test Result Categories",
        yaxis_title="Classification Complexity",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with complexity_tabs[1]:
    st.subheader("Data-Related Challenges")
    st.markdown("""
    **Potential Data Issues:**
    - **Missing Values**: Incomplete patient records
    - **Outliers**: Unusual billing amounts or ages
    - **Imbalanced Classes**: Uneven distribution of test results
    - **Temporal Patterns**: Seasonal variations in admissions
    - **Categorical Variables**: Proper encoding needed
    
    **Data Quality Considerations:**
    - Synthetic data may not reflect real-world complexity
    - Need to validate patterns against medical knowledge
    - Ensure representativeness across demographic groups
    """)

with complexity_tabs[2]:
    st.subheader("Healthcare Domain Complexity")
    st.markdown("""
    **Medical Considerations:**
    - **Chronic Conditions**: Diabetes, hypertension, heart disease patterns
    - **Age Factors**: Different risk profiles by age group
    - **Comorbidities**: Multiple conditions affecting outcomes
    - **Treatment Protocols**: Varying approaches by hospital/doctor
    
    **Regulatory & Ethical Factors:**
    - Patient privacy and data protection
    - Medical ethics in prediction algorithms
    - Healthcare regulations and compliance
    - Bias prevention in model decisions
    """)

# Success Metrics
st.header("📈 Success Metrics Definition")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Model Performance**
    - Accuracy > 85%
    - Balanced precision/recall
    - Low false negative rate
    - Robust cross-validation
    """)

with col2:
    st.markdown("""
    **🏥 Healthcare Impact**
    - Risk factor identification
    - Actionable insights
    - Cost reduction potential
    - Improved patient outcomes
    """)

with col3:
    st.markdown("""
    **📊 Business Value**
    - Reduced readmission rates
    - Resource optimization
    - Enhanced quality metrics
    - Stakeholder satisfaction
    """)

# Research Questions
st.header("❓ Key Research Questions")

research_questions = [
    "What are the primary risk factors for abnormal test results?",
    "How do different medical conditions correlate with readmission risk?",
    "What role does age and gender play in test result outcomes?",
    "Which admission types are most associated with adverse outcomes?",
    "How can billing patterns indicate potential readmission risk?",
    "What combinations of factors create the highest risk profiles?",
    "How can we balance model accuracy with interpretability?",
    "What interventions could be recommended based on predictions?"
]

for i, question in enumerate(research_questions, 1):
    st.markdown(f"**{i}.** {question}")

# Methodology Overview
st.header("🔬 Methodology Overview")

method_col1, method_col2 = st.columns(2)

with method_col1:
    st.markdown("""
    ### 📊 Data Analysis Approach
    - **Exploratory Data Analysis**: Understanding data patterns
    - **Statistical Analysis**: Correlation and significance testing
    - **Visualization**: Interactive charts and dashboards
    - **Feature Engineering**: Creating meaningful predictors
    """)

with method_col2:
    st.markdown("""
    ### 🤖 Machine Learning Strategy
    - **Multiple Algorithms**: Compare different models
    - **Cross-Validation**: Ensure robust performance
    - **Hyperparameter Tuning**: Optimize model parameters
    - **Ensemble Methods**: Combine models for better accuracy
    """)

# Expected Challenges
st.header("⚠️ Expected Challenges & Mitigation")

challenges_data = {
    "Challenge": [
        "Class Imbalance",
        "Feature Selection",
        "Model Interpretability",
        "Overfitting",
        "Data Quality"
    ],
    "Description": [
        "Uneven distribution of test results",
        "Identifying most predictive features",
        "Making models explainable to clinicians",
        "Model performs well on training but not test data",
        "Missing values and inconsistent data"
    ],
    "Mitigation Strategy": [
        "Use SMOTE, class weights, or stratified sampling",
        "Use feature importance scores and domain knowledge",
        "Use SHAP values and feature importance plots",
        "Use cross-validation and regularization",
        "Implement comprehensive data cleaning pipeline"
    ]
}

challenges_df = pd.DataFrame(challenges_data)
st.dataframe(challenges_df, use_container_width=True)

# Next Steps
st.header("🚀 Next Steps")
st.markdown("""
**Problem Understanding Complete! ✅**

You now have a comprehensive understanding of:
- The healthcare readmission prediction challenge
- Dataset structure and characteristics
- Success metrics and evaluation criteria
- Expected challenges and mitigation strategies

**Workflow Progression:**
1. ✅ **Problem Understanding** (Current)
2. 👥 **Stakeholder Analysis** - Identify key players and their interests
3. 📊 **KPI Definition** - Define measurable success indicators
4. 🔧 **Data Preprocessing** - Clean and prepare the dataset
5. 📈 **Data Visualization** - Explore patterns and insights
6. 🤖 **Predictive Modeling** - Build and evaluate models

**Ready to proceed?** Navigate to the **Stakeholder Analysis** page to continue the learnathon workflow.
""")
