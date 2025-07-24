# Healthcare Analytics Dashboard

## Overview

This is a comprehensive healthcare analytics dashboard built with Streamlit for hospital readmission risk prediction. The application provides a multi-page interface for healthcare stakeholders to understand problems, analyze data, visualize insights, and track key performance indicators related to patient readmissions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Pattern**: Multi-page application with navigation sidebar
- **Styling**: Custom CSS with healthcare-themed color schemes and responsive design
- **Layout**: Wide layout configuration for dashboard-style presentation

### Backend Architecture
- **Language**: Python
- **Session Management**: Streamlit session state for data persistence across pages
- **Data Processing**: Pandas for data manipulation and NumPy for numerical operations
- **No Traditional Backend**: Streamlit handles server-side processing directly

### Data Storage Solutions
- **Primary Storage**: In-memory storage using Streamlit session state
- **Data Format**: CSV file uploads processed into Pandas DataFrames
- **Persistence**: Session-based (data persists during user session only)

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Entry point and main dashboard
- **Features**: File upload, overview metrics, custom CSS styling
- **Navigation**: Hub for accessing different analysis pages

### 2. Problem Understanding Page
- **Purpose**: Define business problem and objectives
- **Content**: Hospital readmission context, challenges, and expected benefits
- **Stakeholder Focus**: Healthcare domain expertise presentation

### 3. Stakeholder Analysis Page
- **Purpose**: Identify and analyze key stakeholders
- **Content**: Hospital administrators, physicians, patients, insurance companies
- **Value**: Understanding different perspectives and requirements

### 4. KPI Definition Page
- **Purpose**: Define measurable success metrics
- **Categories**: Clinical, Financial, Operational, and Model Performance KPIs
- **Structure**: Organized tabs for different KPI types

### 5. Data Preprocessing Page
- **Purpose**: Data quality assessment and cleaning
- **Features**: Missing value analysis, data type validation, feature engineering
- **Dependencies**: Requires data upload from main page

### 6. Data Visualization Page
- **Purpose**: Comprehensive data exploration and insights
- **Features**: Interactive dashboards, trend analysis, pattern discovery
- **Dependencies**: Uses processed data from preprocessing page

## Data Flow

1. **Data Input**: User uploads CSV healthcare dataset through main page
2. **Storage**: Data stored in Streamlit session state as 'healthcare_data'
3. **Preprocessing**: Data cleaning and transformation on preprocessing page
4. **Enhanced Storage**: Processed data stored as 'healthcare_data_processed'
5. **Visualization**: Multiple pages access stored data for analysis and visualization
6. **Session Persistence**: Data persists throughout user session across all pages

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization (express and graph_objects)
- **seaborn**: Statistical data visualization
- **matplotlib**: Static plotting library

### Machine Learning Libraries
- **scikit-learn**: Data preprocessing utilities (StandardScaler, LabelEncoder, SimpleImputer)

### Utility Libraries
- **datetime**: Date and time handling
- **warnings**: Warning management

## Deployment Strategy

### Local Development
- **Command**: `streamlit run app.py`
- **Port**: Default Streamlit port (8501)
- **Environment**: Local Python environment with required dependencies

### process Deployment
- **Entry Point**: app.py
- **Run Command**: `streamlit run app.py --server.port 8080 --server.address 0.0.0.0`
- **Dependencies**: All libraries listed in external dependencies section
- **File Structure**: Multi-page application with pages/ directory structure

### Key Considerations
- **File Upload**: Application requires CSV file upload for functionality
- **Session State**: Data persistence relies on Streamlit session state (not permanent storage)
- **Resource Requirements**: Memory usage scales with dataset size
- **Browser Compatibility**: Modern browsers required for Plotly interactive features

### Configuration Requirements
- **Python Version**: 3.7+
- **Memory**: Sufficient RAM for dataset processing
- **File Access**: Read access for CSV file uploads
- **Network**: Internet access for external library CDNs (if any)

## Architecture Decisions

### Technology Stack Choice
- **Problem**: Need for rapid prototyping of healthcare analytics dashboard
- **Solution**: Streamlit for rapid web app development with Python
- **Rationale**: Streamlit provides excellent data science integration, minimal setup, and fast iteration cycles

### Multi-Page Architecture
- **Problem**: Complex healthcare analytics workflow with multiple analysis phases
- **Solution**: Streamlit multi-page application with organized navigation
- **Benefits**: Clear separation of concerns, logical user journey, maintainable code structure

### Session State Data Management
- **Problem**: Need to share data across multiple pages without external database
- **Solution**: Streamlit session state for temporary data persistence
- **Trade-offs**: Simple implementation but data lost on session end; suitable for demo/analysis purposes

### Visualization Strategy
- **Problem**: Need for both static and interactive visualizations
- **Solution**: Combination of Plotly (interactive) and Matplotlib/Seaborn (static)
- **Benefits**: Rich user experience with appropriate tool selection for different visualization needs