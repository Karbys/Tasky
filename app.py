import streamlit as st
import pandas as pd
from utils.excel_handler import ExcelHandler

# Page configuration
st.set_page_config(
    page_title="Excel Data Processor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .upload-section {
        background: #f0f8ff;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 5px solid #2E8B57;
    }
    .info-box {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #32CD32 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #32CD32 0%, #2E8B57 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Excel handler
if 'excel_handler' not in st.session_state:
    st.session_state.excel_handler = ExcelHandler()

# Main header
st.markdown('<h1 class="main-header">📊 Excel Data Processor</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🔧 เครื่องมือจัดการ")
    
    # File upload section
    st.markdown("### 📂 อัปโหลดไฟล์ Excel")
    uploaded_file = st.file_uploader(
        "เลือกไฟล์ Excel",
        type=['xlsx', 'xls'],
        help="รองรับไฟล์ .xlsx และ .xls",
        key="excel_uploader"
    )
    
    if uploaded_file is not None:
        # Process the uploaded file
        if st.button("🚀 ประมวลผลไฟล์", key="process_file"):
            with st.spinner("กำลังประมวลผลไฟล์..."):
                success = st.session_state.excel_handler.read_excel_file(uploaded_file)
                if success:
                    st.success("✅ ประมวลผลไฟล์เสร็จเรียบร้อย!")
                    st.rerun()
    
    # Display file info if available
    if st.session_state.excel_handler.get_file_info():
        st.markdown("---")
        st.markdown("### 📋 ข้อมูลไฟล์")
        file_info = st.session_state.excel_handler.get_file_info()
        
        st.info(f"📄 **ชื่อไฟล์:** {file_info['filename']}")
        st.info(f"💾 **ขนาด:** {file_info['size'] / 1024:.2f} KB")
        st.info(f"📊 **มิติ:** {file_info['shape'][0]} แถว × {file_info['shape'][1]} คอลัมน์")
        st.info(f"⏰ **อัปโหลดเมื่อ:** {file_info['upload_time']}")

# Main content area
if st.session_state.excel_handler.get_dataframe() is not None:
    df = st.session_state.excel_handler.get_dataframe()
    
    # Display basic statistics
    st.markdown("## 📈 สถิติเบื้องต้น")
    
    stats = st.session_state.excel_handler.get_basic_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 จำนวนแถว",
            value=f"{stats['total_rows']:,}"
        )
    
    with col2:
        st.metric(
            label="📋 จำนวนคอลัมน์",
            value=f"{stats['total_columns']:,}"
        )
    
    with col3:
        st.metric(
            label="🔢 คอลัมน์ตัวเลข",
            value=f"{stats['numeric_columns']:,}"
        )
    
    with col4:
        st.metric(
            label="❌ ข้อมูลขาดหาย",
            value=f"{stats['missing_values']:,}",
            delta=f"{(stats['missing_values'] / (stats['total_rows'] * stats['total_columns']) * 100):.1f}%"
        )
    
    # Data manipulation tools
    st.markdown("## 🛠️ เครื่องมือจัดการข้อมูล")
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        # Search functionality
        st.markdown("### 🔍 ค้นหาข้อมูล")
        search_term = st.text_input("ค้นหาในทุกคอลัมน์:", key="search_input")
        
        if search_term:
            if st.button("🔍 ค้นหา", key="search_button"):
                search_results = st.session_state.excel_handler.search_data(search_term)
                if not search_results.empty:
                    st.success(f"✅ พบข้อมูล {len(search_results)} แถว")
                    st.session_state.current_view = search_results
                else:
                    st.warning("⚠️ ไม่พบข้อมูลที่ตรงกัน")
    
    with tool_col2:
        # Sort functionality
        st.markdown("### 📊 เรียงลำดับข้อมูล")
        sort_column = st.selectbox("เลือกคอลัมน์:", df.columns, key="sort_column")
        sort_order = st.radio("ลำดับ:", ["จากน้อยไปมาก", "จากมากไปน้อย"], key="sort_order")
        
        if st.button("📊 เรียงลำดับ", key="sort_button"):
            ascending = sort_order == "จากน้อยไปมาก"
            sorted_df = st.session_state.excel_handler.sort_data(sort_column, ascending)
            st.success(f"✅ เรียงลำดับตาม {sort_column} เรียบร้อย")
            st.session_state.current_view = sorted_df
    
    # Filter functionality
    st.markdown("### 🎯 กรองข้อมูล")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        filter_column = st.selectbox("เลือกคอลัมน์:", df.columns, key="filter_column")
    
    with filter_col2:
        filter_type = st.selectbox(
            "ประเภทการกรอง:",
            ["เท่ากับ", "มีคำว่า", "มากกว่า", "น้อยกว่า"],
            key="filter_type"
        )
    
    with filter_col3:
        filter_value = st.text_input("ค่าที่ต้องการกรอง:", key="filter_value")
    
    if st.button("🎯 กรองข้อมูล", key="filter_button") and filter_value:
        filter_mapping = {
            "เท่ากับ": "equals",
            "มีคำว่า": "contains",
            "มากกว่า": "greater",
            "น้อยกว่า": "less"
        }
        
        try:
            # Convert value if needed for numeric operations
            if filter_type in ["มากกว่า", "น้อยกว่า"]:
                filter_value = float(filter_value)
        except:
            st.error("❌ กรุณาใส่ตัวเลขสำหรับการเปรียบเทียบ")
        else:
            filtered_df = st.session_state.excel_handler.filter_data(
                filter_column, 
                filter_mapping[filter_type], 
                filter_value
            )
            if not filtered_df.empty:
                st.success(f"✅ พบข้อมูล {len(filtered_df)} แถว")
                st.session_state.current_view = filtered_df
            else:
                st.warning("⚠️ ไม่พบข้อมูลที่ตรงกับเงื่อนไข")
    
    # Display data
    st.markdown("## 📋 ตารางข้อมูล")
    
    # Display options
    display_col1, display_col2, display_col3 = st.columns(3)
    
    with display_col1:
        if st.button("📊 แสดงทั้งหมด", key="show_all"):
            st.session_state.current_view = df
    
    with display_col2:
        if st.button("🧹 ทำความสะอาด", key="clean_data"):
            cleaned_df = st.session_state.excel_handler.clean_data()
            st.session_state.current_view = cleaned_df
            st.success("✅ ทำความสะอาดข้อมูลเรียบร้อย")
    
    with display_col3:
        # Download current view
        current_df = st.session_state.get('current_view', df)
        excel_data = st.session_state.excel_handler.export_to_excel(current_df)
        st.download_button(
            label="📥 ดาวน์โหลด Excel",
            data=excel_data,
            file_name="processed_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )
    
    # Display current view
    current_df = st.session_state.get('current_view', df)
    
    # Pagination
    rows_per_page = st.selectbox("แสดงจำนวนแถวต่อหน้า:", [10, 25, 50, 100], index=1, key="rows_per_page")
    
    if len(current_df) > rows_per_page:
        page_number = st.number_input(
            f"หน้าที่ (1-{(len(current_df) - 1) // rows_per_page + 1}):",
            min_value=1,
            max_value=(len(current_df) - 1) // rows_per_page + 1,
            value=1,
            key="page_number"
        )
        
        start_idx = (page_number - 1) * rows_per_page
        end_idx = start_idx + rows_per_page
        display_df = current_df.iloc[start_idx:end_idx]
        
        st.info(f"แสดงแถว {start_idx + 1}-{min(end_idx, len(current_df))} จากทั้งหมด {len(current_df)} แถว")
    else:
        display_df = current_df
    
    # Display the dataframe
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.Column(
                width="medium",
                help=f"คอลัมน์ {col}"
            ) for col in display_df.columns
        }
    )
    
    # Column analysis
    if st.checkbox("📊 แสดงการวิเคราะห์คอลัมน์", key="show_analysis"):
        st.markdown("## 📊 การวิเคราะห์คอลัมน์")
        
        analysis = st.session_state.excel_handler.get_column_analysis()
        
        for col, info in analysis.items():
            with st.expander(f"📋 {col} ({info['type']})"):
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.write(f"**ข้อมูลขาดหาย:** {info['missing_count']} ({info['missing_percent']:.1f}%)")
                    st.write(f"**ค่าไม่ซ้ำ:** {info['unique_count']} ({info['unique_percent']:.1f}%)")
                
                with col_info2:
                    if 'mean' in info:
                        st.write(f"**ค่าเฉลี่ย:** {info['mean']:.2f}")
                        st.write(f"**ค่ากลาง:** {info['median']:.2f}")
                        st.write(f"**ค่าต่ำสุด:** {info['min']:.2f}")
                        st.write(f"**ค่าสูงสุด:** {info['max']:.2f}")
                
                st.write(f"**ตัวอย่างข้อมูล:** {', '.join(map(str, info['sample_values']))}")

else:
    # Welcome screen
    st.markdown("""
    <div class="upload-section">
        <h2 style="color: #2E8B57; margin-bottom: 1rem;">🎯 ยินดีต้อนรับสู่ Excel Data Processor</h2>
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">
            เครื่องมือประมวลผลไฟล์ Excel ที่ทรงพลังและใช้งานง่าย
        </p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 2rem;">
            <div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #2E8B57;">📂 อัปโหลดไฟล์</h3>
                <p>อัปโหลดไฟล์ Excel (.xlsx, .xls) เพื่อเริ่มต้นการวิเคราะห์</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #2E8B57;">🔍 ค้นหาและกรอง</h3>
                <p>ค้นหาข้อมูลหรือกรองข้อมูลตามเงื่อนไขที่ต้องการ</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #2E8B57;">📊 เรียงลำดับ</h3>
                <p>เรียงลำดับข้อมูลตามคอลัมน์ที่ต้องการ</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #2E8B57;">📥 ดาวน์โหลด</h3>
                <p>ดาวน์โหลดผลลัพธ์ที่ประมวลผลแล้วเป็นไฟล์ Excel</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 วิธีการใช้งาน")
    st.markdown("""
    1. **อัปโหลดไฟล์:** คลิกที่ปุ่ม "เลือกไฟล์ Excel" ในแถบด้านซ้าย
    2. **ประมวลผล:** คลิกปุ่ม "ประมวลผลไฟล์" เพื่อเริ่มการวิเคราะห์
    3. **จัดการข้อมูล:** ใช้เครื่องมือต่างๆ เพื่อค้นหา กรอง หรือเรียงลำดับข้อมูล
    4. **ดาวน์โหลด:** บันทึกผลลัพธ์ที่ได้เป็นไฟล์ Excel ใหม่
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🚀 Excel Data Processor • Made with ❤️ using Streamlit
    </div>
    """,
    unsafe_allow_html=True
) 