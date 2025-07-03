import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="Tasky - Streamlit App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📊 Tasky Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🔧 Controls")
    
    # Page selection
    page = st.selectbox(
        "Select Page:",
        ["Dashboard", "Data Upload", "Data Visualization", "Interactive Tools"]
    )
    
    st.markdown("---")
    
    # Theme selector
    theme = st.select_slider(
        "Select Theme:",
        options=["Light", "Auto", "Dark"],
        value="Auto"
    )
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    st.info(f"Current time: {datetime.now().strftime('%H:%M:%S')}")

# Main content based on page selection
if page == "Dashboard":
    st.header("📊 Dashboard Overview")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Users",
            value="1,234",
            delta="12%"
        )
    
    with col2:
        st.metric(
            label="Revenue",
            value="$45,678",
            delta="8%"
        )
    
    with col3:
        st.metric(
            label="Active Sessions",
            value="456",
            delta="-3%"
        )
    
    with col4:
        st.metric(
            label="Conversion Rate",
            value="3.2%",
            delta="0.5%"
        )
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sample Line Chart")
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        values = np.cumsum(np.random.randn(len(dates))) + 100
        
        chart_data = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        
        fig = px.line(chart_data, x='Date', y='Value', title='Trend Over Time')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Sample Pie Chart")
        # Generate sample data
        categories = ['Category A', 'Category B', 'Category C', 'Category D']
        values = [30, 25, 20, 25]
        
        fig = px.pie(values=values, names=categories, title='Distribution by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Sample data table
    st.subheader("📋 Sample Data Table")
    sample_data = pd.DataFrame({
        'ID': range(1, 11),
        'Name': [f'User {i}' for i in range(1, 11)],
        'Score': np.random.randint(60, 100, 10),
        'Category': np.random.choice(['A', 'B', 'C'], 10),
        'Date': pd.date_range('2024-01-01', periods=10, freq='D')
    })
    
    st.dataframe(sample_data, use_container_width=True)

elif page == "Data Upload":
    st.header("📁 Data Upload & Processing")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file to analyze"
    )
    
    if uploaded_file is not None:
        # Read the file
        df = pd.read_csv(uploaded_file)
        
        st.success(f"✅ Successfully uploaded file with {len(df)} rows and {len(df.columns)} columns")
        
        # Display file info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Data Info")
            st.write(f"**Shape:** {df.shape}")
            st.write(f"**Columns:** {list(df.columns)}")
            st.write(f"**Memory Usage:** {df.memory_usage().sum() / 1024:.2f} KB")
        
        with col2:
            st.subheader("🔍 Data Types")
            st.write(df.dtypes)
        
        # Data preview
        st.subheader("👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Basic statistics
        if st.checkbox("Show Statistical Summary"):
            st.subheader("📈 Statistical Summary")
            st.write(df.describe())
        
        # Download processed data
        if st.button("📥 Download Processed Data"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name='processed_data.csv',
                mime='text/csv'
            )
    
    else:
        st.info("👆 Please upload a CSV file to get started")
        
        # Show sample data format
        st.subheader("📋 Expected Data Format")
        sample_format = pd.DataFrame({
            'Column1': ['Value1', 'Value2', 'Value3'],
            'Column2': [10, 20, 30],
            'Column3': ['A', 'B', 'C']
        })
        st.dataframe(sample_format)

elif page == "Data Visualization":
    st.header("📊 Data Visualization")
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type:",
        ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"]
    )
    
    # Generate sample data based on chart type
    if chart_type == "Line Chart":
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        values = np.cumsum(np.random.randn(100)) + 100
        
        data = pd.DataFrame({
            'Date': dates,
            'Value': values
        })
        
        fig = px.line(data, x='Date', y='Value', title='Time Series Data')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar Chart":
        categories = ['A', 'B', 'C', 'D', 'E']
        values = np.random.randint(10, 100, 5)
        
        data = pd.DataFrame({
            'Category': categories,
            'Value': values
        })
        
        fig = px.bar(data, x='Category', y='Value', title='Category Comparison')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        x_values = np.random.randn(100)
        y_values = x_values * 2 + np.random.randn(100) * 0.5
        
        data = pd.DataFrame({
            'X': x_values,
            'Y': y_values
        })
        
        fig = px.scatter(data, x='X', y='Y', title='Correlation Analysis')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        values = np.random.normal(100, 15, 1000)
        
        fig = px.histogram(x=values, nbins=30, title='Distribution Analysis')
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        categories = ['Group A', 'Group B', 'Group C']
        data = []
        
        for category in categories:
            values = np.random.normal(np.random.randint(80, 120), 10, 50)
            for value in values:
                data.append({'Category': category, 'Value': value})
        
        df = pd.DataFrame(data)
        fig = px.box(df, x='Category', y='Value', title='Statistical Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    # Customization options
    st.subheader("🎨 Customization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        color_theme = st.selectbox(
            "Color Theme:",
            ["plotly", "viridis", "plasma", "inferno", "magma"]
        )
    
    with col2:
        show_grid = st.checkbox("Show Grid", value=True)

elif page == "Interactive Tools":
    st.header("🛠️ Interactive Tools")
    
    # Calculator
    st.subheader("🔢 Simple Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num1 = st.number_input("First Number", value=0.0)
    
    with col2:
        operation = st.selectbox("Operation", ["+", "-", "*", "/"])
    
    with col3:
        num2 = st.number_input("Second Number", value=0.0)
    
    if st.button("Calculate"):
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/" and num2 != 0:
            result = num1 / num2
        else:
            result = "Error: Division by zero"
        
        st.success(f"Result: {result}")
    
    st.markdown("---")
    
    # Text analyzer
    st.subheader("📝 Text Analyzer")
    
    text_input = st.text_area("Enter text to analyze:", height=100)
    
    if text_input:
        words = text_input.split()
        chars = len(text_input)
        chars_no_spaces = len(text_input.replace(" ", ""))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Words", len(words))
        
        with col2:
            st.metric("Characters", chars)
        
        with col3:
            st.metric("Characters (no spaces)", chars_no_spaces)
    
    st.markdown("---")
    
    # Random data generator
    st.subheader("🎲 Random Data Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        rows = st.slider("Number of rows", 10, 1000, 100)
    
    with col2:
        columns = st.multiselect(
            "Select columns to generate",
            ["Name", "Age", "Score", "Category", "Date"],
            default=["Name", "Age", "Score"]
        )
    
    if st.button("Generate Random Data"):
        data = {}
        
        if "Name" in columns:
            data["Name"] = [f"Person {i}" for i in range(1, rows + 1)]
        
        if "Age" in columns:
            data["Age"] = np.random.randint(18, 80, rows)
        
        if "Score" in columns:
            data["Score"] = np.random.randint(0, 100, rows)
        
        if "Category" in columns:
            data["Category"] = np.random.choice(["A", "B", "C", "D"], rows)
        
        if "Date" in columns:
            start_date = datetime.now() - timedelta(days=365)
            data["Date"] = pd.date_range(start_date, periods=rows, freq='D')
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Generated Data",
            data=csv,
            file_name='random_data.csv',
            mime='text/csv'
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🚀 Built with Streamlit • Made with ❤️ in Python
    </div>
    """,
    unsafe_allow_html=True
) 