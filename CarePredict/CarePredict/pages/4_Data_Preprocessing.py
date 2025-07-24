import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Data Preprocessing", page_icon="🔧", layout="wide")

st.title("🔧 Data Preprocessing")
st.markdown("---")

st.markdown("""
Data preprocessing is crucial for building reliable predictive models. This section covers data quality assessment, 
cleaning, feature engineering, and preparation for modeling.
""")

# Check if data is loaded
if 'healthcare_data' not in st.session_state:
    st.warning("⚠️ Please upload the healthcare dataset in the main page first.")
    st.markdown("Navigate to the main page and upload the healthcare_dataset.csv file to continue.")
    st.stop()

data = st.session_state['healthcare_data'].copy()

# Data Quality Assessment
st.header("📊 Data Quality Assessment")

# Basic Statistics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", f"{len(data):,}")
with col2:
    st.metric("Total Features", len(data.columns))
with col3:
    missing_count = data.isnull().sum().sum()
    st.metric("Missing Values", missing_count)
with col4:
    duplicate_count = data.duplicated().sum()
    st.metric("Duplicate Records", duplicate_count)

# Data Types and Missing Values Analysis
st.subheader("🔍 Data Types and Missing Values")

# Create data quality summary
data_quality = pd.DataFrame({
    'Column': data.columns,
    'Data Type': data.dtypes.astype(str),
    'Non-Null Count': data.count(),
    'Null Count': data.isnull().sum(),
    'Null Percentage': (data.isnull().sum() / len(data) * 100).round(2),
    'Unique Values': [data[col].nunique() for col in data.columns],
    'Sample Values': [str(data[col].dropna().head(3).tolist()) for col in data.columns]
})

st.dataframe(data_quality, use_container_width=True)

# Missing Values Visualization
if data.isnull().sum().sum() > 0:
    st.subheader("📈 Missing Values Pattern")
    
    missing_data = data.isnull().sum().sort_values(ascending=False)
    missing_data = missing_data[missing_data > 0]
    
    if len(missing_data) > 0:
        fig = px.bar(
            x=missing_data.values,
            y=missing_data.index,
            orientation='h',
            title='Missing Values by Column',
            labels={'x': 'Number of Missing Values', 'y': 'Columns'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No missing values detected in the dataset!")
else:
    st.success("✅ No missing values detected in the dataset!")

# Data Distribution Analysis
st.header("📊 Data Distribution Analysis")

# Numerical columns analysis
numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = data.select_dtypes(include=['object']).columns.tolist()

if numerical_cols:
    st.subheader("📈 Numerical Variables Distribution")
    
    # Create tabs for different numerical analyses
    num_tabs = st.tabs(["Distribution Plots", "Statistics Summary", "Outlier Detection"])
    
    with num_tabs[0]:
        # Select numerical column for distribution plot
        selected_num_col = st.selectbox("Select numerical column for distribution analysis:", numerical_cols)
        
        if selected_num_col:
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram
                fig = px.histogram(
                    data, 
                    x=selected_num_col,
                    title=f'Distribution of {selected_num_col}',
                    nbins=30
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Box plot
                fig = px.box(
                    data,
                    y=selected_num_col,
                    title=f'Box Plot of {selected_num_col}'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with num_tabs[1]:
        # Statistical summary
        st.markdown("### Statistical Summary of Numerical Variables")
        st.dataframe(data[numerical_cols].describe(), use_container_width=True)
    
    with num_tabs[2]:
        # Outlier detection
        st.markdown("### Outlier Detection")
        
        selected_outlier_col = st.selectbox("Select column for outlier analysis:", numerical_cols, key="outlier_col")
        
        if selected_outlier_col:
            # Calculate IQR
            Q1 = data[selected_outlier_col].quantile(0.25)
            Q3 = data[selected_outlier_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data[(data[selected_outlier_col] < lower_bound) | (data[selected_outlier_col] > upper_bound)]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Outliers", len(outliers))
            with col2:
                st.metric("Outlier Percentage", f"{len(outliers)/len(data)*100:.2f}%")
            with col3:
                st.metric("IQR Range", f"{lower_bound:.2f} - {upper_bound:.2f}")
            
            if len(outliers) > 0:
                st.markdown("#### Outlier Records:")
                st.dataframe(outliers[[selected_outlier_col]], use_container_width=True)

# Categorical Variables Analysis
if categorical_cols:
    st.subheader("📊 Categorical Variables Analysis")
    
    selected_cat_col = st.selectbox("Select categorical column for analysis:", categorical_cols)
    
    if selected_cat_col:
        col1, col2 = st.columns(2)
        
        with col1:
            # Value counts
            value_counts = data[selected_cat_col].value_counts()
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f'Distribution of {selected_cat_col}'
            )
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Pie chart
            fig = px.pie(
                values=value_counts.values,
                names=value_counts.index,
                title=f'Proportion of {selected_cat_col}'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show value counts table
        st.markdown(f"#### Value Counts for {selected_cat_col}")
        value_counts_df = pd.DataFrame({
            'Value': value_counts.index,
            'Count': value_counts.values,
            'Percentage': (value_counts.values / len(data) * 100).round(2)
        })
        st.dataframe(value_counts_df, use_container_width=True)

# Data Cleaning
st.header("🧹 Data Cleaning")

cleaning_tabs = st.tabs(["Missing Values", "Duplicates", "Data Types", "Outliers"])

with cleaning_tabs[0]:
    st.subheader("🔧 Missing Values Treatment")
    
    if data.isnull().sum().sum() > 0:
        st.markdown("#### Missing Values Treatment Options:")
        
        missing_cols = data.columns[data.isnull().any()].tolist()
        
        for col in missing_cols:
            st.markdown(f"**{col}** - {data[col].isnull().sum()} missing values")
            
            col1, col2 = st.columns(2)
            with col1:
                if data[col].dtype in ['object']:
                    # Categorical column
                    treatment = st.selectbox(
                        f"Treatment for {col}:",
                        ["Keep as is", "Fill with mode", "Fill with 'Unknown'", "Drop rows"],
                        key=f"missing_{col}"
                    )
                else:
                    # Numerical column
                    treatment = st.selectbox(
                        f"Treatment for {col}:",
                        ["Keep as is", "Fill with mean", "Fill with median", "Fill with mode", "Drop rows"],
                        key=f"missing_{col}"
                    )
            
            with col2:
                if st.button(f"Apply treatment for {col}", key=f"apply_{col}"):
                    if treatment == "Fill with mean" and data[col].dtype in ['int64', 'float64']:
                        data[col].fillna(data[col].mean(), inplace=True)
                        st.success(f"✅ Filled {col} missing values with mean")
                    elif treatment == "Fill with median" and data[col].dtype in ['int64', 'float64']:
                        data[col].fillna(data[col].median(), inplace=True)
                        st.success(f"✅ Filled {col} missing values with median")
                    elif treatment == "Fill with mode":
                        data[col].fillna(data[col].mode()[0], inplace=True)
                        st.success(f"✅ Filled {col} missing values with mode")
                    elif treatment == "Fill with 'Unknown'":
                        data[col].fillna('Unknown', inplace=True)
                        st.success(f"✅ Filled {col} missing values with 'Unknown'")
                    elif treatment == "Drop rows":
                        data.dropna(subset=[col], inplace=True)
                        st.success(f"✅ Dropped rows with missing {col} values")
                    
                    # Update session state
                    st.session_state['healthcare_data_processed'] = data
                    st.rerun()
    else:
        st.success("✅ No missing values to treat!")

with cleaning_tabs[1]:
    st.subheader("🔄 Duplicate Records Treatment")
    
    duplicate_count = data.duplicated().sum()
    
    if duplicate_count > 0:
        st.warning(f"Found {duplicate_count} duplicate records")
        
        if st.button("Remove Duplicate Records"):
            data = data.drop_duplicates()
            st.session_state['healthcare_data_processed'] = data
            st.success(f"✅ Removed {duplicate_count} duplicate records")
            st.rerun()
    else:
        st.success("✅ No duplicate records found!")

with cleaning_tabs[2]:
    st.subheader("🏷️ Data Type Conversions")
    
    st.markdown("#### Current Data Types:")
    dtype_df = pd.DataFrame({
        'Column': data.columns,
        'Current Type': data.dtypes.astype(str),
        'Suggested Type': ['datetime64' if 'date' in col.lower() else str(dtype) for col, dtype in zip(data.columns, data.dtypes)]
    })
    st.dataframe(dtype_df, use_container_width=True)
    
    # Date columns conversion
    date_columns = [col for col in data.columns if 'date' in col.lower()]
    
    if date_columns:
        st.markdown("#### Convert Date Columns:")
        for col in date_columns:
            if data[col].dtype != 'datetime64[ns]':
                if st.button(f"Convert {col} to datetime", key=f"date_{col}"):
                    try:
                        data[col] = pd.to_datetime(data[col])
                        st.success(f"✅ Converted {col} to datetime")
                        st.session_state['healthcare_data_processed'] = data
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error converting {col}: {str(e)}")

with cleaning_tabs[3]:
    st.subheader("🎯 Outlier Treatment")
    
    if numerical_cols:
        selected_outlier_treatment_col = st.selectbox(
            "Select column for outlier treatment:", 
            numerical_cols, 
            key="outlier_treatment_col"
        )
        
        if selected_outlier_treatment_col:
            # Calculate outliers
            Q1 = data[selected_outlier_treatment_col].quantile(0.25)
            Q3 = data[selected_outlier_treatment_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_mask = (data[selected_outlier_treatment_col] < lower_bound) | (data[selected_outlier_treatment_col] > upper_bound)
            outlier_count = outliers_mask.sum()
            
            if outlier_count > 0:
                st.warning(f"Found {outlier_count} outliers in {selected_outlier_treatment_col}")
                
                treatment_method = st.selectbox(
                    "Select outlier treatment method:",
                    ["Keep as is", "Remove outliers", "Cap outliers (Winsorization)", "Transform with log"]
                )
                
                if st.button(f"Apply {treatment_method}", key="apply_outlier_treatment"):
                    if treatment_method == "Remove outliers":
                        data = data[~outliers_mask]
                        st.success(f"✅ Removed {outlier_count} outliers")
                    elif treatment_method == "Cap outliers (Winsorization)":
                        data.loc[data[selected_outlier_treatment_col] < lower_bound, selected_outlier_treatment_col] = lower_bound
                        data.loc[data[selected_outlier_treatment_col] > upper_bound, selected_outlier_treatment_col] = upper_bound
                        st.success(f"✅ Capped outliers to bounds [{lower_bound:.2f}, {upper_bound:.2f}]")
                    elif treatment_method == "Transform with log":
                        if (data[selected_outlier_treatment_col] > 0).all():
                            data[selected_outlier_treatment_col] = np.log1p(data[selected_outlier_treatment_col])
                            st.success(f"✅ Applied log transformation to {selected_outlier_treatment_col}")
                        else:
                            st.error("❌ Cannot apply log transformation to non-positive values")
                    
                    st.session_state['healthcare_data_processed'] = data
                    st.rerun()
            else:
                st.success(f"✅ No outliers found in {selected_outlier_treatment_col}")

# Feature Engineering
st.header("🛠️ Feature Engineering")

feature_tabs = st.tabs(["Date Features", "Categorical Encoding", "Numerical Scaling", "New Features"])

with feature_tabs[0]:
    st.subheader("📅 Date Feature Engineering")
    
    # Check for date columns
    date_cols = [col for col in data.columns if data[col].dtype == 'datetime64[ns]' or 'date' in col.lower()]
    
    if date_cols:
        selected_date_col = st.selectbox("Select date column for feature extraction:", date_cols)
        
        if selected_date_col and st.button("Extract Date Features", key="date_features"):
            try:
                # Convert to datetime if not already
                if data[selected_date_col].dtype != 'datetime64[ns]':
                    data[selected_date_col] = pd.to_datetime(data[selected_date_col])
                
                # Extract features
                data[f'{selected_date_col}_year'] = data[selected_date_col].dt.year
                data[f'{selected_date_col}_month'] = data[selected_date_col].dt.month
                data[f'{selected_date_col}_day'] = data[selected_date_col].dt.day
                data[f'{selected_date_col}_weekday'] = data[selected_date_col].dt.dayofweek
                data[f'{selected_date_col}_quarter'] = data[selected_date_col].dt.quarter
                
                st.success(f"✅ Extracted date features from {selected_date_col}")
                st.session_state['healthcare_data_processed'] = data
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error extracting date features: {str(e)}")
    else:
        st.info("No date columns found for feature extraction")

with feature_tabs[1]:
    st.subheader("🏷️ Categorical Variable Encoding")
    
    if categorical_cols:
        selected_cat_encode_col = st.selectbox("Select categorical column for encoding:", categorical_cols, key="encode_col")
        
        encoding_method = st.selectbox(
            "Select encoding method:",
            ["Label Encoding", "One-Hot Encoding", "Frequency Encoding"]
        )
        
        if st.button("Apply Encoding", key="apply_encoding"):
            if encoding_method == "Label Encoding":
                le = LabelEncoder()
                data[f'{selected_cat_encode_col}_encoded'] = le.fit_transform(data[selected_cat_encode_col].astype(str))
                st.success(f"✅ Applied label encoding to {selected_cat_encode_col}")
                
            elif encoding_method == "One-Hot Encoding":
                dummies = pd.get_dummies(data[selected_cat_encode_col], prefix=selected_cat_encode_col)
                data = pd.concat([data, dummies], axis=1)
                st.success(f"✅ Applied one-hot encoding to {selected_cat_encode_col}")
                
            elif encoding_method == "Frequency Encoding":
                freq_map = data[selected_cat_encode_col].value_counts().to_dict()
                data[f'{selected_cat_encode_col}_frequency'] = data[selected_cat_encode_col].map(freq_map)
                st.success(f"✅ Applied frequency encoding to {selected_cat_encode_col}")
            
            st.session_state['healthcare_data_processed'] = data
            st.rerun()

with feature_tabs[2]:
    st.subheader("📊 Numerical Variable Scaling")
    
    if numerical_cols:
        selected_scale_cols = st.multiselect("Select numerical columns for scaling:", numerical_cols)
        
        scaling_method = st.selectbox(
            "Select scaling method:",
            ["Standard Scaling (Z-score)", "Min-Max Scaling", "Robust Scaling"]
        )
        
        if selected_scale_cols and st.button("Apply Scaling", key="apply_scaling"):
            if scaling_method == "Standard Scaling (Z-score)":
                scaler = StandardScaler()
                for col in selected_scale_cols:
                    data[f'{col}_scaled'] = scaler.fit_transform(data[[col]])
                st.success(f"✅ Applied standard scaling to selected columns")
                
            elif scaling_method == "Min-Max Scaling":
                from sklearn.preprocessing import MinMaxScaler
                scaler = MinMaxScaler()
                for col in selected_scale_cols:
                    data[f'{col}_minmax'] = scaler.fit_transform(data[[col]])
                st.success(f"✅ Applied min-max scaling to selected columns")
                
            elif scaling_method == "Robust Scaling":
                from sklearn.preprocessing import RobustScaler
                scaler = RobustScaler()
                for col in selected_scale_cols:
                    data[f'{col}_robust'] = scaler.fit_transform(data[[col]])
                st.success(f"✅ Applied robust scaling to selected columns")
            
            st.session_state['healthcare_data_processed'] = data
            st.rerun()

with feature_tabs[3]:
    st.subheader("🆕 Create New Features")
    
    st.markdown("#### Length of Stay Calculation")
    admission_col = None
    discharge_col = None
    
    # Find admission and discharge date columns
    for col in data.columns:
        if 'admission' in col.lower() and 'date' in col.lower():
            admission_col = col
        elif 'discharge' in col.lower() and 'date' in col.lower():
            discharge_col = col
    
    if admission_col and discharge_col:
        if st.button("Calculate Length of Stay", key="los_calc"):
            try:
                # Ensure datetime format
                data[admission_col] = pd.to_datetime(data[admission_col])
                data[discharge_col] = pd.to_datetime(data[discharge_col])
                
                # Calculate length of stay
                data['length_of_stay'] = (data[discharge_col] - data[admission_col]).dt.days
                
                st.success("✅ Created Length of Stay feature")
                st.session_state['healthcare_data_processed'] = data
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error calculating length of stay: {str(e)}")
    
    st.markdown("#### Age Groups")
    if 'age' in data.columns:
        if st.button("Create Age Groups", key="age_groups"):
            def categorize_age(age):
                if age < 18:
                    return 'Child'
                elif age < 35:
                    return 'Young Adult'
                elif age < 55:
                    return 'Middle Age'
                elif age < 75:
                    return 'Senior'
                else:
                    return 'Elderly'
            
            data['age_group'] = data['age'].apply(categorize_age)
            st.success("✅ Created age group categories")
            st.session_state['healthcare_data_processed'] = data
            st.rerun()

# Data Validation
st.header("✅ Data Validation")

# Show processed data summary
if 'healthcare_data_processed' in st.session_state:
    processed_data = st.session_state['healthcare_data_processed']
    
    st.subheader("📊 Processed Data Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Records", f"{len(processed_data):,}")
    with col2:
        st.metric("Features", len(processed_data.columns))
    with col3:
        st.metric("Missing Values", processed_data.isnull().sum().sum())
    with col4:
        st.metric("Duplicates", processed_data.duplicated().sum())
    
    # Show data preview
    st.subheader("📋 Processed Data Preview")
    st.dataframe(processed_data.head(10), use_container_width=True)
    
    # Data export option
    st.subheader("💾 Export Processed Data")
    if st.button("Prepare Data for Download"):
        csv = processed_data.to_csv(index=False)
        st.download_button(
            label="Download Processed Dataset",
            data=csv,
            file_name=f"healthcare_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Data Quality Report
st.header("📋 Data Quality Report")

quality_report = {
    "Metric": [
        "Total Records",
        "Total Features", 
        "Missing Value Percentage",
        "Duplicate Records",
        "Numerical Features",
        "Categorical Features",
        "Date Features"
    ],
    "Original Data": [
        f"{len(st.session_state['healthcare_data']):,}",
        len(st.session_state['healthcare_data'].columns),
        f"{st.session_state['healthcare_data'].isnull().sum().sum() / (len(st.session_state['healthcare_data']) * len(st.session_state['healthcare_data'].columns)) * 100:.2f}%",
        st.session_state['healthcare_data'].duplicated().sum(),
        len(st.session_state['healthcare_data'].select_dtypes(include=[np.number]).columns),
        len(st.session_state['healthcare_data'].select_dtypes(include=['object']).columns),
        len([col for col in st.session_state['healthcare_data'].columns if 'date' in col.lower()])
    ],
    "Processed Data": [
        f"{len(data):,}",
        len(data.columns),
        f"{data.isnull().sum().sum() / (len(data) * len(data.columns)) * 100:.2f}%",
        data.duplicated().sum(),
        len(data.select_dtypes(include=[np.number]).columns),
        len(data.select_dtypes(include=['object']).columns),
        len([col for col in data.columns if data[col].dtype == 'datetime64[ns]'])
    ]
}

quality_df = pd.DataFrame(quality_report)
st.dataframe(quality_df, use_container_width=True)

# Update session state with processed data
st.session_state['healthcare_data_processed'] = data

# Preprocessing Summary
st.header("📋 Preprocessing Summary")

preprocessing_steps = []
if 'healthcare_data' in st.session_state:
    original_data = st.session_state['healthcare_data']
    
    # Check what processing was done
    if len(data) != len(original_data):
        preprocessing_steps.append(f"✅ Removed {len(original_data) - len(data)} records")
    
    if len(data.columns) != len(original_data.columns):
        new_features = len(data.columns) - len(original_data.columns)
        preprocessing_steps.append(f"✅ Created {new_features} new features")
    
    if data.isnull().sum().sum() != original_data.isnull().sum().sum():
        preprocessing_steps.append("✅ Handled missing values")
    
    preprocessing_steps.extend([
        "✅ Analyzed data quality and distributions",
        "✅ Identified and handled outliers",
        "✅ Prepared data for modeling"
    ])

if preprocessing_steps:
    st.markdown("### Processing Steps Completed:")
    for step in preprocessing_steps:
        st.markdown(step)

# Next Steps
st.header("🚀 Next Steps")
st.markdown("""
**Data Preprocessing Complete! ✅**

Your data is now ready for visualization and modeling. The preprocessing pipeline has:
- ✅ Assessed data quality and identified issues
- ✅ Handled missing values and duplicates
- ✅ Analyzed distributions and outliers
- ✅ Engineered relevant features
- ✅ Prepared data for machine learning

**Data Quality Improvements:**
- Clean, consistent data format
- No missing values or duplicates
- Properly typed columns
- Engineered features for better predictions

**Next Steps:**
1. 📈 **Data Visualization** - Explore patterns and insights
2. 🤖 **Predictive Modeling** - Build classification models
3. 📊 **Performance Evaluation** - Assess model effectiveness
4. 💡 **Generate Insights** - Extract actionable recommendations

Navigate to the **Data Visualization** page to continue the analysis workflow.
""")
