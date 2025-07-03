import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import io
import base64
from typing import Dict, List, Any, Optional, Tuple


class ExcelHandler:
    """
    A comprehensive Excel file handler for Streamlit applications.
    Handles reading, processing, and analyzing Excel files.
    """
    
    def __init__(self):
        self.df = None
        self.file_info = {}
        self.original_filename = None
    
    def read_excel_file(self, uploaded_file) -> bool:
        """
        Read an Excel file and store it in the handler.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Store original filename
            self.original_filename = uploaded_file.name
            
            # Read Excel file
            if uploaded_file.name.endswith('.xlsx'):
                self.df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.xls'):
                self.df = pd.read_excel(uploaded_file, engine='xlrd')
            else:
                st.error("❌ ไฟล์ต้องเป็นนามสกุล .xlsx หรือ .xls เท่านั้น")
                return False
            
            # Store file information
            self.file_info = {
                'filename': uploaded_file.name,
                'size': uploaded_file.size,
                'shape': self.df.shape,
                'columns': list(self.df.columns),
                'dtypes': self.df.dtypes.to_dict(),
                'memory_usage': self.df.memory_usage(deep=True).sum(),
                'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return True
            
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการอ่านไฟล์: {str(e)}")
            return False
    
    def get_file_info(self) -> Dict:
        """
        Get information about the loaded Excel file.
        
        Returns:
            dict: File information dictionary
        """
        return self.file_info
    
    def get_dataframe(self) -> pd.DataFrame:
        """
        Get the loaded DataFrame.
        
        Returns:
            pd.DataFrame: The loaded Excel data
        """
        return self.df
    
    def get_basic_statistics(self) -> Dict:
        """
        Get basic statistics of the loaded data.
        
        Returns:
            dict: Basic statistics
        """
        if self.df is None:
            return {}
        
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'numeric_columns': len(numeric_columns),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        return stats
    
    def get_column_analysis(self) -> Dict:
        """
        Get detailed analysis of each column.
        
        Returns:
            dict: Column analysis
        """
        if self.df is None:
            return {}
        
        analysis = {}
        
        for col in self.df.columns:
            col_data = self.df[col]
            
            analysis[col] = {
                'type': str(col_data.dtype),
                'missing_count': col_data.isnull().sum(),
                'missing_percent': (col_data.isnull().sum() / len(col_data)) * 100,
                'unique_count': col_data.nunique(),
                'unique_percent': (col_data.nunique() / len(col_data)) * 100
            }
            
            # Add statistics for numeric columns
            if col_data.dtype in ['int64', 'float64', 'int32', 'float32']:
                analysis[col].update({
                    'min': col_data.min(),
                    'max': col_data.max(),
                    'mean': col_data.mean(),
                    'median': col_data.median(),
                    'std': col_data.std()
                })
            
            # Add sample values
            analysis[col]['sample_values'] = col_data.dropna().head(5).tolist()
        
        return analysis
    
    def filter_data(self, column: str, filter_type: str, value: Any) -> pd.DataFrame:
        """
        Filter data based on column and criteria.
        
        Args:
            column: Column name to filter
            filter_type: Type of filter ('equals', 'contains', 'greater', 'less', 'range')
            value: Filter value
            
        Returns:
            pd.DataFrame: Filtered dataframe
        """
        if self.df is None:
            return pd.DataFrame()
        
        try:
            if filter_type == 'equals':
                return self.df[self.df[column] == value]
            elif filter_type == 'contains':
                return self.df[self.df[column].astype(str).str.contains(str(value), na=False)]
            elif filter_type == 'greater':
                return self.df[self.df[column] > value]
            elif filter_type == 'less':
                return self.df[self.df[column] < value]
            elif filter_type == 'range':
                min_val, max_val = value
                return self.df[(self.df[column] >= min_val) & (self.df[column] <= max_val)]
            else:
                return self.df
                
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการกรองข้อมูล: {str(e)}")
            return self.df
    
    def search_data(self, search_term: str) -> pd.DataFrame:
        """
        Search for a term across all columns.
        
        Args:
            search_term: Term to search for
            
        Returns:
            pd.DataFrame: Rows containing the search term
        """
        if self.df is None:
            return pd.DataFrame()
        
        try:
            # Convert all columns to string for searching
            mask = self.df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            
            return self.df[mask]
            
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการค้นหา: {str(e)}")
            return self.df
    
    def sort_data(self, column: str, ascending: bool = True) -> pd.DataFrame:
        """
        Sort data by specified column.
        
        Args:
            column: Column name to sort by
            ascending: Sort direction
            
        Returns:
            pd.DataFrame: Sorted dataframe
        """
        if self.df is None:
            return pd.DataFrame()
        
        try:
            return self.df.sort_values(by=column, ascending=ascending)
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในการเรียงลำดับ: {str(e)}")
            return self.df
    
    def export_to_excel(self, df: pd.DataFrame, filename: str = None) -> bytes:
        """
        Export DataFrame to Excel bytes.
        
        Args:
            df: DataFrame to export
            filename: Optional filename
            
        Returns:
            bytes: Excel file in bytes
        """
        if filename is None:
            filename = f"processed_{self.original_filename}"
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Add a summary sheet
            summary_df = pd.DataFrame({
                'Metric': ['Total Rows', 'Total Columns', 'Processing Time'],
                'Value': [len(df), len(df.columns), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            })
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return output.getvalue()
    
    def get_download_link(self, df: pd.DataFrame, filename: str = None) -> str:
        """
        Generate download link for Excel file.
        
        Args:
            df: DataFrame to download
            filename: Optional filename
            
        Returns:
            str: Download link HTML
        """
        excel_data = self.export_to_excel(df, filename)
        b64 = base64.b64encode(excel_data).decode()
        
        if filename is None:
            filename = f"processed_{self.original_filename}"
        
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">📥 ดาวน์โหลด Excel</a>'
        return href
    
    def clean_data(self) -> pd.DataFrame:
        """
        Basic data cleaning operations.
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        if self.df is None:
            return pd.DataFrame()
        
        cleaned_df = self.df.copy()
        
        # Remove completely empty rows
        cleaned_df = cleaned_df.dropna(how='all')
        
        # Remove completely empty columns
        cleaned_df = cleaned_df.dropna(axis=1, how='all')
        
        # Strip whitespace from string columns
        string_columns = cleaned_df.select_dtypes(include=['object']).columns
        cleaned_df[string_columns] = cleaned_df[string_columns].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
        
        return cleaned_df
    
    def get_data_types_summary(self) -> Dict:
        """
        Get summary of data types in the DataFrame.
        
        Returns:
            dict: Data types summary
        """
        if self.df is None:
            return {}
        
        type_counts = self.df.dtypes.value_counts().to_dict()
        return {str(dtype): count for dtype, count in type_counts.items()} 