import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Stakeholder Analysis", page_icon="👥", layout="wide")

st.title("👥 Stakeholder Analysis")
st.markdown("---")

st.markdown("""
Understanding stakeholders is crucial for successful healthcare analytics projects. 
Each stakeholder group has different interests, concerns, and requirements for the readmission prediction system.
""")

# Primary Stakeholders
st.header("🎯 Primary Stakeholders")

# Create stakeholder cards
stakeholder_data = {
    "Stakeholder": ["Hospital Administrators", "Physicians & Nurses", "Patients & Families", "Insurance Companies"],
    "Primary Interest": [
        "Cost reduction & efficiency",
        "Patient care & clinical outcomes", 
        "Quality care & safety",
        "Cost containment & risk assessment"
    ],
    "Impact Level": ["High", "High", "High", "High"],
    "Influence Level": ["High", "Medium", "Medium", "High"]
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏥 Hospital Administrators")
    st.markdown("""
    **Primary Concerns:**
    - Reducing 30-day readmission rates
    - Avoiding CMS penalties
    - Optimizing resource allocation
    - Improving hospital reputation
    
    **Key Metrics:**
    - Readmission rate percentage
    - Cost per readmission avoided
    - Length of stay optimization
    - Bed utilization efficiency
    
    **Success Indicators:**
    - Decreased readmission penalties
    - Improved quality scores
    - Enhanced operational efficiency
    """)
    
    st.subheader("👨‍⚕️ Physicians & Nurses")
    st.markdown("""
    **Primary Concerns:**
    - Patient safety and outcomes
    - Clinical decision support
    - Workload management
    - Evidence-based care
    
    **Key Metrics:**
    - Patient outcome improvements
    - Diagnostic accuracy
    - Treatment effectiveness
    - Care protocol adherence
    
    **Success Indicators:**
    - Better patient outcomes
    - Reduced clinical errors
    - Enhanced care quality
    """)

with col2:
    st.subheader("👨‍👩‍👧‍👦 Patients & Families")
    st.markdown("""
    **Primary Concerns:**
    - Quality of care received
    - Health outcome improvements
    - Cost of treatment
    - Communication & transparency
    
    **Key Metrics:**
    - Patient satisfaction scores
    - Health improvement rates
    - Treatment success rates
    - Care coordination quality
    
    **Success Indicators:**
    - Improved health outcomes
    - Reduced hospital visits
    - Better care experience
    """)
    
    st.subheader("💼 Insurance Companies")
    st.markdown("""
    **Primary Concerns:**
    - Cost control and management
    - Risk assessment accuracy
    - Fraud prevention
    - Member health outcomes
    
    **Key Metrics:**
    - Claims cost reduction
    - Risk prediction accuracy
    - Member health scores
    - Cost-effectiveness ratios
    
    **Success Indicators:**
    - Reduced claim costs
    - Better risk management
    - Improved member health
    """)

# Secondary Stakeholders
st.header("🎯 Secondary Stakeholders")

secondary_tabs = st.tabs(["🏛️ Regulatory Bodies", "💊 Pharmaceutical Companies", "🔬 Research Institutions", "🏢 Healthcare Technology"])

with secondary_tabs[0]:
    st.subheader("Healthcare Regulatory Bodies")
    st.markdown("""
    **Examples:** CMS, FDA, State Health Departments
    
    **Interests:**
    - Healthcare quality standards
    - Patient safety regulations
    - Cost-effectiveness monitoring
    - Population health outcomes
    
    **Requirements:**
    - Compliance with healthcare regulations
    - Transparent reporting mechanisms
    - Evidence-based recommendations
    - Patient privacy protection
    """)

with secondary_tabs[1]:
    st.subheader("Pharmaceutical Companies")
    st.markdown("""
    **Interests:**
    - Medication effectiveness tracking
    - Drug utilization patterns
    - Adverse event monitoring
    - Treatment outcome analysis
    
    **Value from Analysis:**
    - Better understanding of drug effectiveness
    - Identification of medication-related readmissions
    - Support for evidence-based prescribing
    """)

with secondary_tabs[2]:
    st.subheader("Research Institutions")
    st.markdown("""
    **Interests:**
    - Clinical research advancement
    - Healthcare outcomes research
    - Population health studies
    - Medical knowledge discovery
    
    **Value from Analysis:**
    - Research findings publication
    - Evidence for clinical guidelines
    - Healthcare policy recommendations
    """)

with secondary_tabs[3]:
    st.subheader("Healthcare Technology Vendors")
    st.markdown("""
    **Interests:**
    - Product development insights
    - Market opportunity identification
    - Customer success metrics
    - Technology adoption patterns
    
    **Value from Analysis:**
    - Better product features
    - Market-driven innovations
    - Customer satisfaction improvements
    """)

# Stakeholder Impact Matrix
st.header("📊 Stakeholder Impact & Influence Matrix")

# Create impact/influence matrix
stakeholders = [
    "Hospital Administrators", "Physicians", "Patients", "Insurance Companies",
    "Regulatory Bodies", "Pharma Companies", "Research Institutions", "Tech Vendors"
]

# Impact and influence scores (0-10 scale)
impact_scores = [9, 8, 9, 8, 7, 5, 6, 4]
influence_scores = [9, 7, 6, 9, 8, 4, 5, 3]

# Create scatter plot
fig = px.scatter(
    x=influence_scores,
    y=impact_scores,
    text=stakeholders,
    size=[20]*len(stakeholders),
    color=impact_scores,
    color_continuous_scale="viridis",
    title="Stakeholder Impact vs Influence Matrix"
)

fig.update_traces(textposition="middle center", textfont_size=10)
fig.update_layout(
    xaxis_title="Influence Level (0-10)",
    yaxis_title="Impact Level (0-10)",
    width=800,
    height=600
)

# Add quadrant lines
fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)

# Add quadrant labels
fig.add_annotation(x=2.5, y=8.5, text="High Impact<br>Low Influence", showarrow=False, font=dict(size=12, color="gray"))
fig.add_annotation(x=7.5, y=8.5, text="High Impact<br>High Influence", showarrow=False, font=dict(size=12, color="gray"))
fig.add_annotation(x=2.5, y=2.5, text="Low Impact<br>Low Influence", showarrow=False, font=dict(size=12, color="gray"))
fig.add_annotation(x=7.5, y=2.5, text="Low Impact<br>High Influence", showarrow=False, font=dict(size=12, color="gray"))

st.plotly_chart(fig, use_container_width=True)

# Stakeholder Requirements Analysis
st.header("📋 Stakeholder Requirements Analysis")

requirements_col1, requirements_col2 = st.columns(2)

with requirements_col1:
    st.subheader("🔍 Data Requirements")
    st.markdown("""
    **Hospital Administrators:**
    - Cost analysis per patient
    - Readmission rate trends
    - Resource utilization metrics
    - Quality improvement indicators
    
    **Clinical Staff:**
    - Patient risk scores
    - Clinical decision support
    - Treatment effectiveness data
    - Care pathway recommendations
    
    **Patients:**
    - Personal risk assessment
    - Care plan information
    - Health improvement tracking
    - Treatment options explanation
    """)

with requirements_col2:
    st.subheader("🎯 Functional Requirements")
    st.markdown("""
    **Real-time Processing:**
    - Immediate risk assessment
    - Alert systems for high-risk patients
    - Dashboard updates
    
    **Accuracy & Reliability:**
    - High prediction accuracy
    - Consistent performance
    - Validated medical insights
    
    **Usability:**
    - Intuitive interface design
    - Mobile accessibility
    - Integration with existing systems
    """)

# Stakeholder Communication Plan
st.header("📢 Stakeholder Communication Plan")

communication_data = {
    "Stakeholder Group": [
        "Hospital Administrators",
        "Clinical Staff", 
        "Patients",
        "Insurance Companies",
        "Regulatory Bodies"
    ],
    "Communication Frequency": [
        "Monthly reports",
        "Real-time alerts",
        "As needed",
        "Quarterly reports",
        "Annual compliance"
    ],
    "Preferred Format": [
        "Executive dashboards",
        "Clinical alerts",
        "Patient portals",
        "Statistical reports",
        "Compliance documents"
    ],
    "Key Messages": [
        "Cost savings & efficiency gains",
        "Patient safety improvements",
        "Better health outcomes",
        "Risk reduction & cost control",
        "Quality & compliance metrics"
    ]
}

comm_df = pd.DataFrame(communication_data)
st.dataframe(comm_df, use_container_width=True)

# Risk Assessment by Stakeholder
st.header("⚠️ Stakeholder Risk Assessment")

risk_tabs = st.tabs(["🔴 High Risk", "🟡 Medium Risk", "🟢 Low Risk"])

with risk_tabs[0]:
    st.subheader("High Risk Stakeholders")
    st.markdown("""
    **Hospital Administrators:**
    - Risk: Financial penalties from high readmission rates
    - Mitigation: Implement predictive interventions
    - Success Metric: Reduced penalty costs
    
    **Patients:**
    - Risk: Poor health outcomes from missed high-risk indicators
    - Mitigation: Accurate risk prediction and early intervention
    - Success Metric: Improved health outcomes
    """)

with risk_tabs[1]:
    st.subheader("Medium Risk Stakeholders")
    st.markdown("""
    **Clinical Staff:**
    - Risk: Alert fatigue from false positives
    - Mitigation: Optimize prediction thresholds
    - Success Metric: Balanced sensitivity/specificity
    
    **Insurance Companies:**
    - Risk: Increased claims from unidentified high-risk patients
    - Mitigation: Better risk stratification
    - Success Metric: Reduced unexpected claims
    """)

with risk_tabs[2]:
    st.subheader("Low Risk Stakeholders")
    st.markdown("""
    **Research Institutions:**
    - Risk: Limited access to anonymized data
    - Mitigation: Establish data sharing agreements
    - Success Metric: Research collaboration success
    
    **Technology Vendors:**
    - Risk: Product misalignment with user needs
    - Mitigation: Regular stakeholder feedback
    - Success Metric: User adoption rates
    """)

# Success Criteria by Stakeholder
st.header("✅ Success Criteria by Stakeholder")

success_metrics = {
    "Stakeholder": [
        "Hospital Administrators", "Clinical Staff", "Patients", 
        "Insurance Companies", "Regulatory Bodies"
    ],
    "Primary Success Metric": [
        "15% reduction in readmission rates",
        "20% improvement in patient outcomes",
        "90% patient satisfaction with care",
        "10% reduction in readmission claims",
        "100% compliance with quality standards"
    ],
    "Secondary Metrics": [
        "Cost savings, operational efficiency",
        "Reduced workload, better decisions",
        "Health improvements, care quality",
        "Risk prediction accuracy, cost control",
        "Quality indicators, patient safety"
    ],
    "Timeline": [
        "6-12 months",
        "3-6 months", 
        "Ongoing",
        "6-12 months",
        "Annual assessment"
    ]
}

success_df = pd.DataFrame(success_metrics)
st.dataframe(success_df, use_container_width=True)

# Stakeholder Engagement Strategy
st.header("🤝 Stakeholder Engagement Strategy")

engagement_col1, engagement_col2 = st.columns(2)

with engagement_col1:
    st.markdown("""
    ### 📋 Engagement Phases
    **Phase 1: Discovery (Weeks 1-2)**
    - Stakeholder interviews
    - Requirements gathering
    - Pain point identification
    
    **Phase 2: Design (Weeks 3-4)**
    - Solution co-creation
    - Prototype feedback
    - User acceptance criteria
    
    **Phase 3: Implementation (Weeks 5-8)**
    - Pilot program launch
    - Training and support
    - Performance monitoring
    """)

with engagement_col2:
    st.markdown("""
    ### 📊 Engagement Metrics
    **Participation Rates:**
    - Meeting attendance: >80%
    - Feedback response: >75%
    - Training completion: >90%
    
    **Satisfaction Scores:**
    - Process satisfaction: >4.0/5.0
    - Solution relevance: >4.2/5.0
    - Support quality: >4.0/5.0
    """)

# Next Steps
st.header("🚀 Next Steps")
st.markdown("""
**Stakeholder Analysis Complete! ✅**

You have successfully:
- Identified all key stakeholders and their interests
- Mapped stakeholder influence and impact levels
- Defined requirements and success criteria
- Developed communication and engagement strategies

**Key Insights:**
- Hospital administrators and insurance companies have the highest influence
- Clinical staff and patients have the highest impact on outcomes
- Success requires balancing competing interests and priorities
- Regular communication is essential for project success

**Stakeholder Engagement Strategy:**
1. ✅ **Stakeholder Identification** (Completed)
2. 📋 **Requirements Gathering** - Detailed requirement collection
3. 🤝 **Stakeholder Buy-in** - Secure commitment and support
4. 📊 **KPI Alignment** - Align metrics with stakeholder needs
5. 🔄 **Continuous Communication** - Regular updates and feedback

**Ready to proceed?** Navigate to the **KPI Definition** page to define measurable success indicators aligned with stakeholder needs.
""")
