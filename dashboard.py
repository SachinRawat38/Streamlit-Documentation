import streamlit as st
import pandas as pd

st.title("Simple Analytics Dashboard")

# Create some sample data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [10, 25, 40, 15]
})

# Add a sidebar filter
st.sidebar.header("Dashboard Controls")
show_chart = st.sidebar.checkbox("Show Chart", value=True)
show_table = st.sidebar.checkbox("Show Data Table", value=True)

# Display selected elements
if show_chart:
    st.subheader("Data Visualization")
    st.bar_chart(data.set_index('Category'))

if show_table:
    st.subheader("Raw Data")
    st.dataframe(data)
