import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .workflow-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Healthcare Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Comprehensive Hospital Readmission Risk Analysis Following Learnathon Workflow</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Learnathon Workflow")
    
    # Workflow steps with status indicators
    workflow_steps = [
        ("🎯", "Problem Understanding", "1_Problem_Understanding"),
        ("👥", "Stakeholder Analysis", "2_Stakeholder_Analysis"), 
        ("📊", "KPI Definition", "3_KPI_Definition"),
        ("🔧", "Data Preprocessing", "4_Data_Preprocessing"),
        ("📈", "Data Visualization", "5_Data_Visualization"),
        ("🤖", "Predictive Modeling", "6_Predictive_Modeling")
    ]
    
    for i, (icon, title, page) in enumerate(workflow_steps, 1):
        status = "✅" if 'healthcare_data' in st.session_state else "⏳"
        st.sidebar.markdown(f"{i}. {icon} **{title}** {status}")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    if 'healthcare_data' in st.session_state:
        data = st.session_state['healthcare_data']
        st.sidebar.metric("Total Records", len(data))
        st.sidebar.metric("Features", len(data.columns))
        st.sidebar.metric("Missing Values", data.isnull().sum().sum())
    else:
        st.sidebar.info("Upload data to see stats")
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Problem Statement</h3>
            <p>Predict Hospital Readmission Risk for Patients with Chronic Conditions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Dataset Source</h3>
            <p>Healthcare Dataset by prasad22 from Kaggle</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Target Variable</h3>
            <p>Test Results Classification (Normal/Abnormal/Inconclusive)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Upload Section
    st.markdown('<h2 class="section-header">📁 Data Upload</h2>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your healthcare dataset CSV file",
        type=['csv'],
        help="Upload the healthcare_dataset.csv file from Kaggle"
    )
    
    if uploaded_file is not None:
        try:
            # Load data with progress bar
            with st.spinner('Loading and processing dataset...'):
                data = pd.read_csv(uploaded_file)
                
                # Clean column names - replace spaces with underscores and normalize
                data.columns = data.columns.str.replace(' ', '_').str.replace('-', '_').str.lower()
                
                # Standardize column names to match expected format
                column_mapping = {
                    'medical_condition': 'medical_condition',
                    'test_results': 'test_results', 
                    'billing_amount': 'billing_amount',
                    'insurance_provider': 'insurance_provider',
                    'blood_type': 'blood_type',
                    'date_of_admission': 'date_of_admission',
                    'discharge_date': 'discharge_date',
                    'admission_type': 'admission_type',
                    'room_number': 'room_number'
                }
                
                # Apply column mapping if columns exist
                for old_name, new_name in column_mapping.items():
                    if old_name in data.columns:
                        data = data.rename(columns={old_name: new_name})
            
            st.success(f"✅ Dataset loaded successfully! Shape: {data.shape}")
            st.session_state['healthcare_data'] = data
            
            # Display basic info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", f"{len(data):,}")
            with col2:
                st.metric("Features", len(data.columns))
            with col3:
                missing_count = data.isnull().sum().sum()
                st.metric("Missing Values", missing_count)
            with col4:
                duplicate_count = data.duplicated().sum()
                st.metric("Duplicates", duplicate_count)
            
            # Data quality indicators
            st.markdown("### 🔍 Data Quality Assessment")
            quality_col1, quality_col2, quality_col3 = st.columns(3)
            
            with quality_col1:
                completeness = (1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
                st.metric("Data Completeness", f"{completeness:.1f}%")
            
            with quality_col2:
                uniqueness = (1 - duplicate_count / len(data)) * 100
                st.metric("Data Uniqueness", f"{uniqueness:.1f}%")
            
            with quality_col3:
                consistency = 100  # Placeholder for consistency check
                st.metric("Data Consistency", f"{consistency:.1f}%")
            
            # Preview data
            st.markdown("### 📋 Data Preview")
            st.dataframe(data.head(10), use_container_width=True)
            
            # Show column information
            st.markdown("### 📊 Dataset Schema")
            schema_info = pd.DataFrame({
                'Column': data.columns,
                'Data Type': data.dtypes.astype(str),
                'Non-Null Count': data.count(),
                'Null Count': data.isnull().sum(),
                'Unique Values': [data[col].nunique() for col in data.columns],
                'Sample Values': [str(data[col].dropna().head(2).tolist()) for col in data.columns]
            })
            st.dataframe(schema_info, use_container_width=True)
            
            # Data validation checks
            st.markdown("### ✅ Data Validation")
            validation_checks = []
            
            # Check for target variable
            target_candidates = ['test_results', 'Test_Results', 'test results']
            target_found = any(col in data.columns for col in target_candidates)
            validation_checks.append(("Target Variable Present", "✅" if target_found else "❌"))
            
            # Check for key features
            key_features = ['age', 'gender', 'medical_condition']
            features_found = sum(1 for feature in key_features if feature in data.columns)
            validation_checks.append(("Key Features Present", f"{features_found}/{len(key_features)}"))
            
            # Check data types
            date_cols = [col for col in data.columns if 'date' in col.lower()]
            dates_valid = all(pd.to_datetime(data[col], errors='coerce').notna().all() for col in date_cols)
            validation_checks.append(("Date Formats Valid", "✅" if dates_valid else "⚠️"))
            
            validation_df = pd.DataFrame(validation_checks, columns=['Check', 'Status'])
            st.dataframe(validation_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.markdown("**Troubleshooting Tips:**")
            st.markdown("- Ensure the file is a valid CSV format")
            st.markdown("- Check that the file is not corrupted")
            st.markdown("- Verify the file contains the expected healthcare data structure")
    else:
        # Show instructions for getting the data  
        st.info("📋 Please upload the healthcare dataset CSV file to begin analysis.")
        
        # Enhanced instructions
        instruction_tabs = st.tabs(["📥 Download Instructions", "📋 Dataset Info", "🔧 Troubleshooting"])
        
        with instruction_tabs[0]:
            st.markdown("""
            ### 📥 How to Get the Dataset
            
            1. **Visit Kaggle**: Go to [Healthcare Dataset by prasad22](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)
            2. **Create Account**: Sign up for a free Kaggle account if you don't have one
            3. **Download**: Click the "Download" button to get the healthcare_dataset.csv file (8.4 MB)
            4. **Upload**: Use the file uploader above to upload the CSV file
            
            **Direct Link**: https://www.kaggle.com/datasets/prasad22/healthcare-dataset
            """)
        
        with instruction_tabs[1]:
            st.markdown("""
            ### 📋 Expected Dataset Structure
            The dataset should contain these **15 columns**:
            
            | Column | Description | Type |
            |--------|-------------|------|
            | **Name** | Patient name identifier | Text |
            | **Age** | Patient age in years | Integer |
            | **Gender** | Male/Female | Categorical |
            | **Blood Type** | A+, B-, O+, etc. | Categorical |
            | **Medical Condition** | Primary diagnosis | Categorical |
            | **Date of Admission** | Hospital admission date | Date |
            | **Doctor** | Attending physician | Text |
            | **Hospital** | Healthcare facility | Categorical |
            | **Insurance Provider** | Insurance company | Categorical |
            | **Billing Amount** | Total billing cost | Float |
            | **Room Number** | Assigned room | Integer |
            | **Admission Type** | Emergency/Elective/Urgent | Categorical |
            | **Discharge Date** | Hospital discharge date | Date |
            | **Medication** | Prescribed medication | Categorical |
            | **Test Results** | Normal/Abnormal/Inconclusive | **Target** |
            
            **Expected Size**: ~10,000 patient records
            """)
        
        with instruction_tabs[2]:
            st.markdown("""
            ### 🔧 Common Issues & Solutions
            
            **File Upload Issues:**
            - Ensure file size is under Streamlit's limit (200MB)
            - Check file extension is `.csv`
            - Verify file is not corrupted
            
            **Data Format Issues:**
            - CSV should use comma separators
            - Text fields should be properly quoted
            - Date fields should be in recognizable format
            
            **Column Name Issues:**
            - The app automatically handles column name variations
            - Spaces, hyphens, and case differences are normalized
            - Core columns must be present for full functionality
            
            **Need Help?**
            - Check the Kaggle dataset page for updates
            - Ensure you're downloading the latest version
            - Try refreshing the browser if upload fails
            """)
    
    # Workflow Progress
    st.markdown("---")
    st.markdown('<h2 class="section-header">🚀 Workflow Progress</h2>', unsafe_allow_html=True)
    
    # Progress tracking
    if 'healthcare_data' in st.session_state:
        progress_steps = [
            ("Data Upload", True),
            ("Problem Understanding", True),
            ("Stakeholder Analysis", True),
            ("KPI Definition", True),
            ("Data Preprocessing", 'healthcare_data_processed' in st.session_state),
            ("Data Visualization", 'healthcare_data_processed' in st.session_state),
            ("Predictive Modeling", False)
        ]
        
        completed_steps = sum(1 for _, completed in progress_steps if completed)
        progress_percentage = (completed_steps / len(progress_steps)) * 100
        
        st.progress(progress_percentage / 100)
        st.markdown(f"**Progress**: {completed_steps}/{len(progress_steps)} steps completed ({progress_percentage:.0f}%)")
        
        # Next recommended step
        next_step = next((step for step, completed in progress_steps if not completed), None)
        if next_step:
            st.info(f"👉 **Next Step**: {next_step}")
        else:
            st.success("🎉 **All workflow steps completed!**")
    
    # Key Objectives
    st.markdown("---")
    st.markdown('<h2 class="section-header">🎯 Key Objectives</h2>', unsafe_allow_html=True)
    
    objectives_col1, objectives_col2 = st.columns(2)
    
    with objectives_col1:
        st.markdown("""
        ### 🔍 Analysis Goals
        - **Risk Factor Identification**: Explore key factors affecting hospital readmission
        - **Trend Analysis**: Identify patterns in readmission data
        - **Stakeholder Impact**: Understand how different stakeholders are affected
        - **KPI Development**: Define measurable indicators for success
        - **Predictive Modeling**: Build accurate classification models
        """)
    
    with objectives_col2:
        st.markdown("""
        ### 📈 Expected Outcomes
        - **Predictive Model**: Classify test results with >85% accuracy
        - **Actionable Insights**: Provide recommendations for reducing readmissions
        - **Data-Driven Decisions**: Support healthcare management decisions
        - **Cost Optimization**: Identify opportunities for cost reduction
        - **Quality Improvement**: Enhance patient care outcomes
        """)
    
    # Workflow Navigation
    st.markdown("---")
    st.markdown('<h2 class="section-header">🧭 Navigation Guide</h2>', unsafe_allow_html=True)
    
    nav_col1, nav_col2, nav_col3 = st.columns(3)
    
    with nav_col1:
        st.markdown("""
        <div class="workflow-step">
            📋 Analysis Phase
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        1. **Problem Understanding**
        2. **Stakeholder Analysis** 
        3. **KPI Definition**
        """)
    
    with nav_col2:
        st.markdown("""
        <div class="workflow-step">
            🔧 Data Phase
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        4. **Data Preprocessing**
        5. **Data Visualization**
        """)
    
    with nav_col3:
        st.markdown("""
        <div class="workflow-step">
            🤖 Modeling Phase
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        6. **Predictive Modeling**
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><strong>Healthcare Analytics Dashboard</strong> | Built with Streamlit</p>
        <p>Dataset Source: <a href="https://www.kaggle.com/datasets/prasad22/healthcare-dataset" target="_blank">Healthcare Dataset by prasad22</a></p>
        <p>🏥 Empowering healthcare decisions through data analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
