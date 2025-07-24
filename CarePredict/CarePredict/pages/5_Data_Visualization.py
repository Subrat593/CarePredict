import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Data Visualization", page_icon="📈", layout="wide")

st.title("📈 Data Visualization & Insights")
st.markdown("---")

st.markdown("""
Explore the healthcare dataset through comprehensive visualizations to uncover patterns, trends, 
and insights that will inform our predictive modeling and clinical recommendations.
""")

# Check if processed data is available
if 'healthcare_data_processed' in st.session_state:
    data = st.session_state['healthcare_data_processed'].copy()
elif 'healthcare_data' in st.session_state:
    data = st.session_state['healthcare_data'].copy()
else:
    st.warning("⚠️ Please upload and process the healthcare dataset first.")
    st.markdown("Navigate to the main page to upload data and the Data Preprocessing page to clean it.")
    st.stop()

# Overview Dashboard
st.header("📊 Healthcare Analytics Dashboard")

# Key Metrics
cols = st.columns(5)

with cols[0]:
    st.metric("Total Patients", f"{len(data):,}")

with cols[1]:
    if 'age' in data.columns:
        avg_age = data['age'].mean()
        st.metric("Average Age", f"{avg_age:.1f} years")
    else:
        st.metric("Average Age", "N/A")

with cols[2]:
    condition_col = None
    for col in ['medical_condition', 'Medical_Condition', 'Medical Condition']:
        if col in data.columns:
            condition_col = col
            break
    
    if condition_col:
        unique_conditions = data[condition_col].nunique()
        st.metric("Medical Conditions", unique_conditions)
    else:
        st.metric("Medical Conditions", "N/A")

with cols[3]:
    billing_col = None
    for col in ['billing_amount', 'Billing_Amount', 'Billing Amount']:
        if col in data.columns:
            billing_col = col
            break
    
    if billing_col:
        avg_billing = data[billing_col].mean()
        st.metric("Avg Billing", f"${avg_billing:,.0f}")
    else:
        st.metric("Avg Billing", "N/A")

with cols[4]:
    target_col = None
    for col in ['test_results', 'Test_Results', 'Test Results']:
        if col in data.columns:
            target_col = col
            break
    
    if target_col:
        abnormal_pct = (data[target_col] == 'Abnormal').mean() * 100
        st.metric("Abnormal Tests", f"{abnormal_pct:.1f}%")
    else:
        st.metric("Abnormal Tests", "N/A")

# Visualization Categories
st.header("🎯 Visualization Categories")

viz_tabs = st.tabs([
    "👥 Demographics", 
    "🏥 Medical Conditions", 
    "💰 Financial Analysis", 
    "📅 Temporal Patterns", 
    "🎯 Target Analysis",
    "🔗 Correlations"
])

with viz_tabs[0]:
    st.subheader("👥 Patient Demographics Analysis")
    
    demo_col1, demo_col2 = st.columns(2)
    
    with demo_col1:
        # Gender Distribution
        if 'gender' in data.columns:
            st.markdown("#### Gender Distribution")
            gender_counts = data['gender'].value_counts()
            
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Patient Gender Distribution",
                color_discrete_sequence=['#FF6B6B', '#4ECDC4']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Blood Type Distribution
        blood_col = None
        for col in ['blood_type', 'Blood_Type', 'Blood Type']:
            if col in data.columns:
                blood_col = col
                break
        
        if blood_col:
            st.markdown("#### Blood Type Distribution")
            
            blood_counts = data[blood_col].value_counts()
            fig = px.bar(
                x=blood_counts.index,
                y=blood_counts.values,
                title="Blood Type Distribution",
                color=blood_counts.values,
                color_continuous_scale='viridis'
            )
            fig.update_xaxis(title="Blood Type")
            fig.update_yaxis(title="Count")
            st.plotly_chart(fig, use_container_width=True)
    
    with demo_col2:
        # Age Distribution
        if 'age' in data.columns:
            st.markdown("#### Age Distribution")
            
            fig = px.histogram(
                data,
                x='age',
                nbins=20,
                title="Patient Age Distribution",
                color_discrete_sequence=['#45B7D1']
            )
            fig.update_xaxis(title="Age (years)")
            fig.update_yaxis(title="Count")
            st.plotly_chart(fig, use_container_width=True)
            
            # Age vs Gender
            if 'gender' in data.columns:
                st.markdown("#### Age Distribution by Gender")
                
                fig = px.box(
                    data,
                    x='gender',
                    y='age',
                    title="Age Distribution by Gender",
                    color='gender',
                    color_discrete_sequence=['#FF6B6B', '#4ECDC4']
                )
                st.plotly_chart(fig, use_container_width=True)

with viz_tabs[1]:
    st.subheader("🏥 Medical Conditions Analysis")
    
    if condition_col:
        med_col1, med_col2 = st.columns(2)
        
        with med_col1:
            # Medical Conditions Distribution
            st.markdown("#### Medical Conditions Frequency")
            
            condition_counts = data[condition_col].value_counts()
            fig = px.bar(
                y=condition_counts.index,
                x=condition_counts.values,
                orientation='h',
                title="Medical Conditions Distribution",
                color=condition_counts.values,
                color_continuous_scale='plasma'
            )
            fig.update_xaxis(title="Number of Patients")
            fig.update_yaxis(title="Medical Condition")
            st.plotly_chart(fig, use_container_width=True)
        
        with med_col2:
            # Medical Conditions by Age Group
            if 'age' in data.columns:
                st.markdown("#### Medical Conditions by Age Group")
                
                # Create age groups
                data_viz = data.copy()
                data_viz['Age_Group'] = pd.cut(
                    data_viz['age'], 
                    bins=[0, 18, 35, 55, 75, 100], 
                    labels=['<18', '18-34', '35-54', '55-74', '75+']
                )
                
                condition_age = data_viz.groupby([condition_col, 'Age_Group']).size().reset_index(name='Count')
                
                fig = px.bar(
                    condition_age,
                    x=condition_col,
                    y='Count',
                    color='Age_Group',
                    title="Medical Conditions by Age Group",
                    barmode='stack'
                )
                fig.update_xaxis(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Medical Conditions by Gender
        if 'gender' in data.columns:
            st.markdown("#### Medical Conditions by Gender")
            
            condition_gender = pd.crosstab(data[condition_col], data['gender'])
            
            fig = px.bar(
                x=condition_gender.index,
                y=[condition_gender.iloc[:, 0], condition_gender.iloc[:, 1]],
                title="Medical Conditions by Gender",
                barmode='group',
                labels={'x': 'Medical Condition', 'y': 'Count'}
            )
            if len(condition_gender.columns) >= 2:
                fig.data[0].name = condition_gender.columns[0]
                fig.data[1].name = condition_gender.columns[1]
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

with viz_tabs[2]:
    st.subheader("💰 Financial Analysis")
    
    if billing_col:
        fin_col1, fin_col2 = st.columns(2)
        
        with fin_col1:
            # Billing Amount Distribution
            st.markdown("#### Billing Amount Distribution")
            
            fig = px.histogram(
                data,
                x=billing_col,
                nbins=30,
                title="Billing Amount Distribution",
                color_discrete_sequence=['#2E8B57']
            )
            fig.update_xaxis(title="Billing Amount ($)")
            fig.update_yaxis(title="Frequency")
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary Statistics
            st.markdown("#### Billing Statistics")
            billing_stats = data[billing_col].describe()
            
            stats_df = pd.DataFrame({
                'Statistic': ['Mean', 'Median', 'Std Dev', 'Min', 'Max'],
                'Value': [
                    f"${billing_stats['mean']:,.2f}",
                    f"${billing_stats['50%']:,.2f}",
                    f"${billing_stats['std']:,.2f}",
                    f"${billing_stats['min']:,.2f}",
                    f"${billing_stats['max']:,.2f}"
                ]
            })
            st.dataframe(stats_df, use_container_width=True)
        
        with fin_col2:
            # Billing by Medical Condition
            if condition_col:
                st.markdown("#### Average Billing by Medical Condition")
                
                billing_by_condition = data.groupby(condition_col)[billing_col].mean().sort_values(ascending=True)
                
                fig = px.bar(
                    y=billing_by_condition.index,
                    x=billing_by_condition.values,
                    orientation='h',
                    title="Average Billing by Medical Condition",
                    color=billing_by_condition.values,
                    color_continuous_scale='viridis'
                )
                fig.update_xaxis(title="Average Billing Amount ($)")
                fig.update_yaxis(title="Medical Condition")
                st.plotly_chart(fig, use_container_width=True)
        
        # Insurance Provider Analysis
        insurance_col = None
        for col in ['insurance_provider', 'Insurance_Provider', 'Insurance Provider']:
            if col in data.columns:
                insurance_col = col
                break
        
        if insurance_col:
            st.markdown("#### Billing Analysis by Insurance Provider")
            
            ins_col1, ins_col2 = st.columns(2)
            
            with ins_col1:
                # Average billing by insurance
                avg_billing_insurance = data.groupby(insurance_col)[billing_col].mean().sort_values(ascending=False)
                
                fig = px.bar(
                    x=avg_billing_insurance.index,
                    y=avg_billing_insurance.values,
                    title="Average Billing by Insurance Provider",
                    color=avg_billing_insurance.values,
                    color_continuous_scale='blues'
                )
                fig.update_xaxis(title="Insurance Provider", tickangle=45)
                fig.update_yaxis(title="Average Billing ($)")
                st.plotly_chart(fig, use_container_width=True)
            
            with ins_col2:
                # Patient count by insurance
                insurance_counts = data[insurance_col].value_counts()
                
                fig = px.pie(
                    values=insurance_counts.values,
                    names=insurance_counts.index,
                    title="Patient Distribution by Insurance Provider"
                )
                st.plotly_chart(fig, use_container_width=True)

with viz_tabs[3]:
    st.subheader("📅 Temporal Patterns Analysis")
    
    # Find date columns
    date_columns = []
    for col in data.columns:
        if 'date' in col.lower() or data[col].dtype == 'datetime64[ns]':
            date_columns.append(col)
    
    if date_columns:
        selected_date_col = st.selectbox("Select date column for temporal analysis:", date_columns)
        
        if selected_date_col:
            # Ensure datetime format
            try:
                data[selected_date_col] = pd.to_datetime(data[selected_date_col])
                
                temp_col1, temp_col2 = st.columns(2)
                
                with temp_col1:
                    # Admissions by month
                    st.markdown("#### Admissions by Month")
                    
                    data['Month'] = data[selected_date_col].dt.month
                    data['Year'] = data[selected_date_col].dt.year
                    
                    monthly_admissions = data.groupby('Month').size()
                    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    fig = px.line(
                        x=month_names,
                        y=monthly_admissions.values,
                        title="Monthly Admission Patterns",
                        markers=True
                    )
                    fig.update_xaxis(title="Month")
                    fig.update_yaxis(title="Number of Admissions")
                    st.plotly_chart(fig, use_container_width=True)
                
                with temp_col2:
                    # Admissions by day of week
                    st.markdown("#### Admissions by Day of Week")
                    
                    data['Weekday'] = data[selected_date_col].dt.day_name()
                    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    weekday_admissions = data['Weekday'].value_counts().reindex(weekday_order, fill_value=0)
                    
                    fig = px.bar(
                        x=weekday_admissions.index,
                        y=weekday_admissions.values,
                        title="Admissions by Day of Week",
                        color=weekday_admissions.values,
                        color_continuous_scale='plasma'
                    )
                    fig.update_xaxis(title="Day of Week")
                    fig.update_yaxis(title="Number of Admissions")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Yearly trends if multiple years
                if data['Year'].nunique() > 1:
                    st.markdown("#### Yearly Admission Trends")
                    
                    yearly_admissions = data.groupby('Year').size()
                    
                    fig = px.line(
                        x=yearly_admissions.index,
                        y=yearly_admissions.values,
                        title="Yearly Admission Trends",
                        markers=True
                    )
                    fig.update_xaxis(title="Year")
                    fig.update_yaxis(title="Number of Admissions")
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error processing date column: {str(e)}")
    else:
        st.info("No date columns found for temporal analysis")

with viz_tabs[4]:
    st.subheader("🎯 Target Variable Analysis")
    
    if target_col:
        target_col1, target_col2 = st.columns(2)
        
        with target_col1:
            # Target distribution
            st.markdown("#### Test Results Distribution")
            
            target_counts = data[target_col].value_counts()
            
            fig = px.pie(
                values=target_counts.values,
                names=target_counts.index,
                title="Test Results Distribution",
                color_discrete_sequence=['#2ECC71', '#E74C3C', '#F39C12']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Target statistics
            st.markdown("#### Target Statistics")
            target_stats = pd.DataFrame({
                'Test Result': target_counts.index,
                'Count': target_counts.values,
                'Percentage': (target_counts.values / len(data) * 100).round(2)
            })
            st.dataframe(target_stats, use_container_width=True)
        
        with target_col2:
            # Target by medical condition
            if condition_col:
                st.markdown("#### Test Results by Medical Condition")
                
                condition_target = pd.crosstab(data[condition_col], data[target_col], normalize='index') * 100
                
                fig = px.bar(
                    condition_target,
                    title="Test Results Distribution by Medical Condition (%)",
                    barmode='stack'
                )
                fig.update_xaxis(title="Medical Condition", tickangle=45)
                fig.update_yaxis(title="Percentage")
                st.plotly_chart(fig, use_container_width=True)
        
        # Target by demographics
        if 'age' in data.columns:
            st.markdown("#### Test Results by Age Group")
            
            data_viz = data.copy()
            data_viz['Age_Group'] = pd.cut(
                data_viz['age'], 
                bins=[0, 18, 35, 55, 75, 100], 
                labels=['<18', '18-34', '35-54', '55-74', '75+']
            )
            
            age_target = pd.crosstab(data_viz['Age_Group'], data_viz[target_col], normalize='index') * 100
            
            fig = px.bar(
                age_target,
                title="Test Results Distribution by Age Group (%)",
                barmode='stack',
                color_discrete_sequence=['#2ECC71', '#E74C3C', '#F39C12']
            )
            fig.update_xaxis(title="Age Group")
            fig.update_yaxis(title="Percentage")
            st.plotly_chart(fig, use_container_width=True)

with viz_tabs[5]:
    st.subheader("🔗 Correlation Analysis")
    
    # Select numerical columns for correlation
    numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numerical_cols) > 1:
        corr_col1, corr_col2 = st.columns(2)
        
        with corr_col1:
            # Correlation heatmap
            st.markdown("#### Correlation Heatmap")
            
            # Calculate correlation matrix
            corr_matrix = data[numerical_cols].corr()
            
            fig = px.imshow(
                corr_matrix,
                title="Feature Correlation Heatmap",
                color_continuous_scale='RdBu',
                aspect='auto'
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with corr_col2:
            # Top correlations
            st.markdown("#### Strongest Correlations")
            
            # Get correlation pairs
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_pairs.append({
                        'Feature 1': corr_matrix.columns[i],
                        'Feature 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
            
            corr_df = pd.DataFrame(corr_pairs)
            corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
            
            # Display top 10 correlations
            st.dataframe(corr_df.head(10), use_container_width=True)
        
        # Scatter plots for high correlations
        if len(corr_df) > 0:
            st.markdown("#### Scatter Plot Analysis")
            
            # Select top correlation pair
            top_corr = corr_df.iloc[0]
            
            fig = px.scatter(
                data,
                x=top_corr['Feature 1'],
                y=top_corr['Feature 2'],
                title=f"Relationship: {top_corr['Feature 1']} vs {top_corr['Feature 2']} (r={top_corr['Correlation']:.3f})",
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)

# Advanced Analytics
st.header("🔬 Advanced Analytics")

advanced_tabs = st.tabs(["📊 Statistical Summary", "🎯 Risk Factors", "💡 Key Insights"])

with advanced_tabs[0]:
    st.subheader("📊 Comprehensive Statistical Summary")
    
    # Numerical summary
    if numerical_cols:
        st.markdown("#### Numerical Variables Summary")
        st.dataframe(data[numerical_cols].describe(), use_container_width=True)
    
    # Categorical summary
    categorical_cols = data.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        st.markdown("#### Categorical Variables Summary")
        
        cat_summary = []
        for col in categorical_cols:
            cat_summary.append({
                'Column': col,
                'Unique Values': data[col].nunique(),
                'Most Frequent': data[col].mode().iloc[0] if len(data[col].mode()) > 0 else 'N/A',
                'Frequency of Most Common': data[col].value_counts().iloc[0] if len(data[col]) > 0 else 0
            })
        
        cat_summary_df = pd.DataFrame(cat_summary)
        st.dataframe(cat_summary_df, use_container_width=True)

with advanced_tabs[1]:
    st.subheader("🎯 Risk Factor Analysis")
    
    if target_col and condition_col:
        # Risk analysis by medical condition
        st.markdown("#### Risk Assessment by Medical Condition")
        
        risk_analysis = data.groupby(condition_col)[target_col].apply(
            lambda x: (x == 'Abnormal').mean() * 100
        ).sort_values(ascending=False)
        
        fig = px.bar(
            y=risk_analysis.index,
            x=risk_analysis.values,
            orientation='h',
            title="Abnormal Test Result Rate by Medical Condition",
            color=risk_analysis.values,
            color_continuous_scale='Reds'
        )
        fig.update_xaxis(title="Abnormal Test Rate (%)")
        fig.update_yaxis(title="Medical Condition")
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk by age group
        if 'age' in data.columns:
            st.markdown("#### Risk Assessment by Age Group")
            
            data_risk = data.copy()
            data_risk['Age_Group'] = pd.cut(
                data_risk['age'], 
                bins=[0, 18, 35, 55, 75, 100], 
                labels=['<18', '18-34', '35-54', '55-74', '75+']
            )
            
            age_risk = data_risk.groupby('Age_Group')[target_col].apply(
                lambda x: (x == 'Abnormal').mean() * 100
            )
            
            fig = px.bar(
                x=age_risk.index,
                y=age_risk.values,
                title="Abnormal Test Result Rate by Age Group",
                color=age_risk.values,
                color_continuous_scale='Oranges'
            )
            fig.update_xaxis(title="Age Group")
            fig.update_yaxis(title="Abnormal Test Rate (%)")
            st.plotly_chart(fig, use_container_width=True)

with advanced_tabs[2]:
    st.subheader("💡 Key Insights & Recommendations")
    
    # Generate insights based on the analysis
    insights = []
    
    # Demographic insights
    if 'age' in data.columns:
        avg_age = data['age'].mean()
        insights.append(f"📊 **Demographics**: Average patient age is {avg_age:.1f} years")
    
    # Medical condition insights
    if condition_col:
        top_condition = data[condition_col].value_counts().index[0]
        top_condition_pct = data[condition_col].value_counts(normalize=True).iloc[0] * 100
        insights.append(f"🏥 **Most Common Condition**: {top_condition} ({top_condition_pct:.1f}% of patients)")
    
    # Financial insights
    if billing_col:
        avg_billing = data[billing_col].mean()
        high_billing_threshold = data[billing_col].quantile(0.9)
        high_billing_pct = (data[billing_col] > high_billing_threshold).mean() * 100
        insights.append(f"💰 **Financial**: Average billing is ${avg_billing:,.0f}, with {high_billing_pct:.1f}% of cases being high-cost")
    
    # Target variable insights
    if target_col:
        abnormal_pct = (data[target_col] == 'Abnormal').mean() * 100
        insights.append(f"🎯 **Test Results**: {abnormal_pct:.1f}% of patients have abnormal test results")
    
    # Display insights
    for insight in insights:
        st.markdown(insight)
    
    st.markdown("### 🎯 Clinical Recommendations")
    st.markdown("""
    Based on the data analysis, here are key recommendations:
    
    1. **High-Risk Monitoring**: Focus on patients with conditions showing highest abnormal test rates
    2. **Age-Based Protocols**: Implement age-specific screening and monitoring protocols
    3. **Cost Management**: Investigate high-billing cases for cost optimization opportunities
    4. **Preventive Care**: Develop targeted prevention programs for most common conditions
    5. **Resource Allocation**: Plan staffing and resources based on admission patterns
    """)

# Export Visualizations
st.header("💾 Export Analysis")

if st.button("Generate Analysis Report"):
    st.success("✅ Analysis complete! Key findings:")
    
    # Generate summary statistics
    total_patients = len(data)
    avg_age = data['age'].mean() if 'age' in data.columns else 0
    top_condition = data[condition_col].value_counts().index[0] if condition_col else 'N/A'
    abnormal_rate = (data[target_col] == 'Abnormal').mean() * 100 if target_col else 0
    
    # Find date range
    date_range = "N/A"
    if date_columns:
        try:
            min_date = data[date_columns[0]].min().strftime('%Y-%m-%d')
            max_date = data[date_columns[0]].max().strftime('%Y-%m-%d')
            date_range = f"{min_date} to {max_date}"
        except:
            date_range = "Date format error"
    
    report_summary = f"""
    **Healthcare Analytics Report Summary**
    
    📊 **Dataset Overview**:
    - Total Patients: {total_patients:,}
    - Features Analyzed: {len(data.columns)}
    - Time Period: {date_range}
    
    🎯 **Key Findings**:
    - Most common condition: {top_condition}
    - Average patient age: {avg_age:.1f} years
    - Abnormal test rate: {abnormal_rate:.1f}%
    
    💡 **Recommendations**: Focus on high-risk conditions and age groups for targeted interventions.
    """
    
    st.markdown(report_summary)

# Next Steps
st.header("🚀 Next Steps")
st.markdown("""
**Data Visualization Complete! ✅**

You've successfully explored the healthcare dataset and uncovered key insights. The visualization analysis has revealed:
- ✅ Patient demographic patterns and distributions
- ✅ Medical condition prevalence and relationships
- ✅ Financial trends and billing patterns
- ✅ Temporal admission patterns and seasonality
- ✅ Risk factors for abnormal test results
- ✅ Statistical correlations between variables

**Key Insights Generated:**
- Identified high-risk patient populations
- Discovered cost patterns and optimization opportunities
- Revealed temporal trends for resource planning
- Established baseline metrics for KPI tracking

**Next Steps:**
1. 🤖 **Predictive Modeling** - Build machine learning models
2. 📊 **Model Evaluation** - Assess model performance and accuracy
3. 💡 **Generate Recommendations** - Create actionable clinical insights
4. 📋 **Report Generation** - Summarize findings and recommendations

Navigate to the **Predictive Modeling** page to build classification models for test result prediction.
""")
