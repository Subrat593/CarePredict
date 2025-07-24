import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="KPI Definition", page_icon="📊", layout="wide")

st.title("📊 Key Performance Indicators (KPI) Definition")
st.markdown("---")

st.markdown("""
Defining clear, measurable KPIs is essential for tracking the success of our healthcare analytics project. 
These indicators will help us measure progress toward reducing hospital readmissions and improving patient outcomes.
""")

# KPI Categories
st.header("🎯 KPI Categories")

kpi_tabs = st.tabs(["🏥 Clinical KPIs", "💰 Financial KPIs", "⚡ Operational KPIs", "🤖 Model Performance KPIs"])

with kpi_tabs[0]:
    st.subheader("Clinical Performance Indicators")
    
    clinical_kpis = {
        "KPI Name": [
            "30-Day Readmission Rate",
            "Patient Mortality Rate", 
            "Length of Stay (LOS)",
            "Test Result Accuracy",
            "Treatment Success Rate"
        ],
        "Definition": [
            "Percentage of patients readmitted within 30 days",
            "Percentage of patients who die during or after treatment",
            "Average number of days patients stay in hospital",
            "Percentage of correctly classified test results",
            "Percentage of patients with improved health outcomes"
        ],
        "Target Value": [
            "<10%",
            "<2%",
            "5-7 days",
            ">90%",
            ">85%"
        ],
        "Current Baseline": [
            "15%",
            "3%",
            "8 days",
            "Unknown",
            "Unknown"
        ]
    }
    
    clinical_df = pd.DataFrame(clinical_kpis)
    st.dataframe(clinical_df, use_container_width=True)
    
    # Clinical KPI Visualization
    fig = go.Figure()
    
    kpi_names = clinical_kpis["KPI Name"]
    current_values = [15, 3, 8, 70, 70]  # Sample current values
    target_values = [10, 2, 6, 90, 85]   # Target values
    
    fig.add_trace(go.Bar(
        name='Current Performance',
        x=kpi_names,
        y=current_values,
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='Target Performance',
        x=kpi_names,
        y=target_values,
        marker_color='lightgreen'
    ))
    
    fig.update_layout(
        title='Clinical KPIs: Current vs Target Performance',
        xaxis_title='KPI',
        yaxis_title='Value (%)',
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with kpi_tabs[1]:
    st.subheader("Financial Performance Indicators")
    
    financial_kpis = {
        "KPI Name": [
            "Cost per Readmission",
            "Average Billing Amount",
            "Insurance Claim Approval Rate",
            "Cost Savings from Prevention",
            "Revenue per Patient"
        ],
        "Definition": [
            "Average cost incurred per readmitted patient",
            "Mean billing amount per patient admission",
            "Percentage of insurance claims approved",
            "Money saved by preventing readmissions",
            "Average revenue generated per patient"
        ],
        "Target Value": [
            "<$15,000",
            "$20,000-$30,000",
            ">95%",
            ">$500,000/year",
            ">$25,000"
        ],
        "Impact": [
            "High",
            "Medium",
            "High",
            "Very High",
            "High"
        ]
    }
    
    financial_df = pd.DataFrame(financial_kpis)
    st.dataframe(financial_df, use_container_width=True)
    
    # Financial Impact Visualization
    categories = financial_kpis["KPI Name"]
    impact_values = [4, 3, 4, 5, 4]  # Impact scores
    
    fig = px.bar(
        x=categories,
        y=impact_values,
        title="Financial KPIs - Impact Assessment",
        color=impact_values,
        color_continuous_scale="RdYlGn",
        labels={'y': 'Impact Score (1-5)', 'x': 'Financial KPI'}
    )
    
    st.plotly_chart(fig, use_container_width=True)

with kpi_tabs[2]:
    st.subheader("Operational Performance Indicators")
    
    operational_kpis = {
        "KPI Name": [
            "Bed Utilization Rate",
            "Emergency Department Visits",
            "Staff Efficiency Score",
            "Patient Satisfaction Score",
            "System Response Time"
        ],
        "Definition": [
            "Percentage of available beds occupied",
            "Number of emergency visits per month",
            "Measure of staff productivity and effectiveness",
            "Patient-reported satisfaction rating",
            "Time for system to provide risk predictions"
        ],
        "Target Value": [
            "80-90%",
            "Reduce by 20%",
            ">4.0/5.0",
            ">4.5/5.0",
            "<2 seconds"
        ],
        "Measurement Frequency": [
            "Daily",
            "Monthly",
            "Quarterly",
            "Monthly",
            "Real-time"
        ]
    }
    
    operational_df = pd.DataFrame(operational_kpis)
    st.dataframe(operational_df, use_container_width=True)

with kpi_tabs[3]:
    st.subheader("Model Performance Indicators")
    
    model_kpis = {
        "KPI Name": [
            "Model Accuracy",
            "Precision (Positive Predictive Value)",
            "Recall (Sensitivity)",
            "F1-Score",
            "AUC-ROC Score",
            "False Positive Rate",
            "Model Reliability Score"
        ],
        "Definition": [
            "Percentage of correct predictions",
            "True positives / (True positives + False positives)",
            "True positives / (True positives + False negatives)",
            "Harmonic mean of precision and recall",
            "Area under ROC curve",
            "False positives / (False positives + True negatives)",
            "Consistency of model predictions over time"
        ],
        "Target Value": [
            ">85%",
            ">80%",
            ">80%",
            ">80%",
            ">0.85",
            "<10%",
            ">90%"
        ],
        "Critical Level": [
            "<70%",
            "<60%",
            "<60%",
            "<60%",
            "<0.70",
            ">20%",
            "<70%"
        ]
    }
    
    model_df = pd.DataFrame(model_kpis)
    st.dataframe(model_df, use_container_width=True)
    
    # Model Performance Radar Chart
    categories = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    target_values = [85, 80, 80, 80, 85]
    current_values = [75, 70, 78, 74, 82]  # Sample current performance
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=target_values,
        theta=categories,
        fill='toself',
        name='Target Performance',
        line_color='green'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=current_values,
        theta=categories,
        fill='toself',
        name='Current Performance',
        line_color='orange'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Model Performance KPIs: Current vs Target"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# KPI Dashboard Design
st.header("📈 KPI Dashboard Design")

st.subheader("🎛️ Real-time KPI Monitoring")

# Create sample dashboard layout
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="30-Day Readmission Rate",
        value="12.3%",
        delta="-2.7%",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="Model Accuracy",
        value="87.2%",
        delta="+4.1%"
    )

with col3:
    st.metric(
        label="Cost Savings (Monthly)",
        value="$425K",
        delta="+$75K"
    )

with col4:
    st.metric(
        label="Patient Satisfaction",
        value="4.6/5.0",
        delta="+0.3"
    )

# KPI Trend Analysis
st.subheader("📊 KPI Trend Analysis")

# Sample trend data
dates = pd.date_range('2024-01-01', periods=12, freq='M')
readmission_rates = [15.2, 14.8, 14.1, 13.7, 13.2, 12.9, 12.5, 12.1, 11.8, 11.4, 11.1, 10.8]
model_accuracy = [82.1, 83.5, 84.2, 85.1, 85.8, 86.3, 86.9, 87.2, 87.6, 87.9, 88.1, 88.4]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates,
    y=readmission_rates,
    mode='lines+markers',
    name='Readmission Rate (%)',
    line=dict(color='red'),
    yaxis='y'
))

fig.add_trace(go.Scatter(
    x=dates,
    y=model_accuracy,
    mode='lines+markers',
    name='Model Accuracy (%)',
    line=dict(color='blue'),
    yaxis='y2'
))

fig.update_layout(
    title='KPI Trends Over Time',
    xaxis_title='Month',
    yaxis=dict(
        title='Readmission Rate (%)',
        side='left',
        range=[10, 16]
    ),
    yaxis2=dict(
        title='Model Accuracy (%)',
        side='right',
        overlaying='y',
        range=[80, 90]
    ),
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# KPI Prioritization Matrix
st.header("🎯 KPI Prioritization Matrix")

st.markdown("""
We prioritize KPIs based on their impact on patient outcomes and business value, 
as well as the feasibility of measurement and improvement.
""")

# KPI Priority Data
kpi_priority_data = {
    "KPI": [
        "30-Day Readmission Rate", "Model Accuracy", "Patient Satisfaction",
        "Cost per Readmission", "Treatment Success Rate", "Length of Stay",
        "System Response Time", "Staff Efficiency"
    ],
    "Impact": [9, 8, 8, 7, 9, 6, 5, 6],
    "Feasibility": [8, 9, 7, 8, 6, 8, 9, 7],
    "Priority Score": [17, 17, 15, 15, 15, 14, 14, 13]
}

# Create priority matrix
fig = px.scatter(
    x=kpi_priority_data["Feasibility"],
    y=kpi_priority_data["Impact"],
    text=kpi_priority_data["KPI"],
    size=kpi_priority_data["Priority Score"],
    color=kpi_priority_data["Priority Score"],
    color_continuous_scale="viridis",
    title="KPI Prioritization Matrix: Impact vs Feasibility"
)

fig.update_traces(textposition="middle center", textfont_size=10)
fig.update_layout(
    xaxis_title="Feasibility Score (1-10)",
    yaxis_title="Impact Score (1-10)",
    width=800,
    height=600
)

# Add quadrant lines
fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)

st.plotly_chart(fig, use_container_width=True)

# KPI Targets and Thresholds
st.header("🎯 KPI Targets and Thresholds")

threshold_data = {
    "KPI": [
        "30-Day Readmission Rate",
        "Model Accuracy", 
        "Patient Satisfaction",
        "Cost per Readmission"
    ],
    "Excellent (Green)": [
        "< 8%",
        "> 90%",
        "> 4.8/5.0",
        "< $12,000"
    ],
    "Good (Yellow)": [
        "8-12%",
        "85-90%",
        "4.0-4.8/5.0",
        "$12,000-$18,000"
    ],
    "Needs Improvement (Red)": [
        "> 12%",
        "< 85%",
        "< 4.0/5.0",
        "> $18,000"
    ],
    "Current Status": [
        "12.3% (Yellow)",
        "87.2% (Yellow)",
        "4.6/5.0 (Green)",
        "$15,500 (Yellow)"
    ]
}

threshold_df = pd.DataFrame(threshold_data)
st.dataframe(threshold_df, use_container_width=True)

# KPI Reporting Schedule
st.header("📅 KPI Reporting Schedule")

reporting_schedule = {
    "KPI Category": [
        "Clinical KPIs",
        "Financial KPIs",
        "Operational KPIs",
        "Model Performance KPIs"
    ],
    "Reporting Frequency": [
        "Weekly",
        "Monthly",
        "Daily",
        "Real-time"
    ],
    "Audience": [
        "Clinical Teams, Hospital Admin",
        "Finance Team, Executives",
        "Operations Team, Department Heads",
        "Data Science Team, IT"
    ],
    "Report Format": [
        "Clinical Dashboard",
        "Financial Summary Report",
        "Operations Dashboard",
        "Technical Performance Report"
    ]
}

schedule_df = pd.DataFrame(reporting_schedule)
st.dataframe(schedule_df, use_container_width=True)

# KPI Action Plans
st.header("🚀 KPI Improvement Action Plans")

action_tabs = st.tabs(["🏥 Clinical Improvements", "💰 Financial Optimizations", "⚡ Operational Enhancements"])

with action_tabs[0]:
    st.subheader("Clinical KPI Improvement Actions")
    st.markdown("""
    **For 30-Day Readmission Rate Reduction:**
    - Implement post-discharge follow-up protocols
    - Enhanced patient education programs
    - Medication reconciliation improvements
    - Chronic disease management programs
    
    **For Treatment Success Rate Improvement:**
    - Evidence-based treatment protocols
    - Personalized care plans
    - Multidisciplinary team approaches
    - Continuous clinical training
    """)

with action_tabs[1]:
    st.subheader("Financial KPI Optimization Actions")
    st.markdown("""
    **For Cost per Readmission Reduction:**
    - Preventive care investments
    - Efficient resource allocation
    - Value-based care contracts
    - Technology automation
    
    **For Revenue per Patient Optimization:**
    - Service line expansion
    - Quality-based reimbursements
    - Insurance negotiation improvements
    - Billing process optimization
    """)

with action_tabs[2]:
    st.subheader("Operational KPI Enhancement Actions")
    st.markdown("""
    **For Bed Utilization Optimization:**
    - Predictive admission planning
    - Discharge planning improvements
    - Transfer coordination
    - Capacity management systems
    
    **For Patient Satisfaction Improvement:**
    - Communication training
    - Service quality programs
    - Wait time reductions
    - Patient feedback systems
    """)

# KPI Success Stories
st.header("🏆 Expected Success Stories")

success_col1, success_col2 = st.columns(2)

with success_col1:
    st.markdown("""
    ### 📈 6-Month Targets
    - Reduced 30-day readmission rate from 15% to 11%
    - Improved model accuracy from 82% to 88%
    - Achieved $2M in annual cost savings
    - Increased patient satisfaction to 4.6/5.0
    - Reduced average length of stay by 1 day
    """)

with success_col2:
    st.markdown("""
    ### 🎯 12-Month Vision
    - Industry-leading readmission rate of <8%
    - Model accuracy consistently >90%
    - $5M+ in annual cost savings
    - Patient satisfaction >4.8/5.0
    - Top quartile performance in all clinical metrics
    """)

# KPI Implementation Roadmap
st.header("🗺️ KPI Implementation Roadmap")

roadmap_data = {
    "Phase": [
        "Phase 1: Foundation",
        "Phase 2: Implementation", 
        "Phase 3: Optimization",
        "Phase 4: Excellence"
    ],
    "Duration": [
        "Months 1-2",
        "Months 3-6",
        "Months 7-9", 
        "Months 10-12"
    ],
    "Key Activities": [
        "Baseline measurement, Dashboard setup, Data collection",
        "Model deployment, Staff training, Process integration",
        "Performance tuning, Feedback incorporation, Scaling",
        "Advanced analytics, Benchmarking, Continuous improvement"
    ],
    "Success Metrics": [
        "All KPIs baseline established",
        "80% of targets met",
        "90% of targets met",
        "Industry-leading performance"
    ]
}

roadmap_df = pd.DataFrame(roadmap_data)
st.dataframe(roadmap_df, use_container_width=True)

# Next Steps
st.header("🚀 Next Steps")
st.markdown("""
**KPI Definition Complete! ✅**

You have successfully:
- Defined comprehensive KPIs across all critical dimensions
- Established clear targets and thresholds for success
- Created prioritization framework for improvement efforts
- Developed implementation roadmap and action plans

**Key Achievements:**
- **25 KPIs defined** across clinical, financial, operational, and model performance
- **Clear success criteria** aligned with stakeholder needs
- **Actionable improvement plans** for each KPI category
- **Implementation roadmap** with 12-month timeline

**KPI Summary:**
- 🏥 Clinical KPIs: Focus on patient outcomes and care quality
- 💰 Financial KPIs: Target cost reduction and revenue optimization
- ⚡ Operational KPIs: Improve efficiency and patient satisfaction
- 🤖 Model Performance KPIs: Ensure accurate and reliable predictions

**KPI Implementation Roadmap:**
1. ✅ **KPI Definition** (Completed)
2. 📊 **Baseline Measurement** - Establish current performance levels
3. 🎯 **Target Setting** - Set realistic improvement targets
4. 📈 **Dashboard Development** - Create monitoring systems
5. 🔄 **Regular Review** - Weekly/monthly performance reviews

**Ready to proceed?** Navigate to the **Data Preprocessing** page to prepare the dataset for analysis and modeling.
""")
