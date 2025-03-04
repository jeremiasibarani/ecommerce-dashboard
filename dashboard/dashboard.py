import streamlit as st
from util import *



with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=MIN_DATE,
        max_value=MAX_DATE,
        value=[MIN_DATE, MAX_DATE]
    )

st.header('E-commerce revenue report')

col1, col2 = st.columns(2)
with col1:
    total_revenue = get_total_revenue(start_date, end_date)
    st.metric("Total Revenue", value=total_revenue)

with col2:
    total_order = get_total_order(start_date, end_date)
    st.metric("Total Order", value=total_order)



plot = visualize_revenue(get_revenue(start_date, end_date))
st.plotly_chart(plot)

plotcol1, plotcol2 = st.columns(2)

with plotcol1:
    plot = visualize_delivery(get_delivery_status(start_date, end_date))
    st.plotly_chart(plot)

with plotcol2:
    plot = visualize_payment(get_payment_status(start_date, end_date))
    st.plotly_chart(plot)

plot2 = visualize_product_by_review(get_order_product_review(start_date, end_date))
st.plotly_chart(plot2)

plot3 = visualize_rfm(get_rfm_customer(start_date, end_date))
st.plotly_chart(plot3)
