import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def load_csv(file_path):
    return pd.read_csv(file_path)


revenue = load_csv('./dashboard/revenue.csv')
product_review = load_csv('./dashboard/order_product_review.csv')
payment_report = load_csv('./dashboard/payment_report.csv')
orders = load_csv('./dashboard/orders.csv')


MIN_DATE = parse_date('2016-01-01')
MAX_DATE = parse_date('2018-12-01')


def get_revenue(min_date, max_date):
    df = revenue.copy()
    df["date"] = pd.to_datetime(df["purchase_year"].astype(str) + "-" +
                                     df["purchase_month"].astype(str) + "-01").dt.date
    return df[(df["date"] >= min_date) & (df["date"] <= max_date)]


def get_payment_report(min_date, max_date):
    payment_report['date'] = pd.to_datetime(payment_report['order_purchase_timestamp']).dt.date
    return payment_report[
        (payment_report['date']  >= min_date) & 
        (payment_report['date']  <= max_date)
    ]

def get_order_product_review(min_date, max_date):
    product_review['order_purchase_timestamp'] = pd.to_datetime(product_review['order_purchase_timestamp']).dt.date
    return product_review[
        (product_review['order_purchase_timestamp'] >= min_date) & 
        (product_review['order_purchase_timestamp'] <= max_date)
        ].groupby(by="product_category_name").agg({
                    "review_score": "sum"
                 }).reset_index()

def get_total_revenue(min_date, max_date):
    df = revenue.copy()
    df["date"] = pd.to_datetime(df["purchase_year"].astype(str) + "-" +
                                     df["purchase_month"].astype(str) + "-01").dt.date
    df = df[(df["date"] >= min_date) & (df["date"] <= max_date)]
    return '${:,.2f}'.format(round(df['price'].sum(), 2))


def visualize_revenue(df):
    revenue_data_by_year_month = df.groupby(by=['purchase_year', 'purchase_month']).agg({
      'price': 'sum'
    }).reset_index()

    revenue_data_by_year_month['purchase_month'] = revenue_data_by_year_month['purchase_month'].astype(int)
    revenue_data_by_year_month = revenue_data_by_year_month.sort_values(by=['purchase_year', 'purchase_month'])
    revenue_data_by_year_month['purchase_month'] = revenue_data_by_year_month['purchase_month'].astype('str')

    fig = px.line(
        revenue_data_by_year_month,
        x="purchase_month",
        y="price",
        title='Revenue over years',
        color='purchase_year',
        markers=True,
        labels={
            "price": "Price (USD)",
            "purchase_year": "Year",
            "purchase_month": "Month"
        }
        )
    return fig


def get_total_revenue(min_date, max_date):
    df = revenue.copy()
    df["date"] = pd.to_datetime(df["purchase_year"].astype(str) + "-" +
                                     df["purchase_month"].astype(str) + "-01").dt.date
    total_revenue = df[(df["date"] >= min_date) & (df["date"] <= max_date)].price.sum()
    return '${:,.2f}'.format(total_revenue)

def get_total_order(min_date, max_date):
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp']).dt.date
    return orders[
        (orders['order_purchase_timestamp'] >= min_date) & 
        (orders['order_purchase_timestamp'] <= max_date)
        ].order_id.count()

def get_delivery_status(min_date, max_date):
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp']).dt.date
    df = orders[
        (orders['order_purchase_timestamp'] >= min_date) & 
        (orders['order_purchase_timestamp'] <= max_date)
        ]
    return df.groupby(by='delivery_status').agg({
    "order_id": "nunique"
    }).sort_values(ascending=False, by="delivery_status").reset_index()

def get_payment_status(min_date, max_date):
    df = get_payment_report(min_date, max_date)
    complete_count = df[df['outstanding_payment'] < 1].shape[0]
    total_count = df.shape[0]
    incomplete_count = total_count - complete_count

    data = {
    'name' : ['belum lunas', 'lunas'],
    'count' : [incomplete_count, complete_count]
    }

    return pd.DataFrame.from_dict(data)



def visualize_delivery(df):
    fig = px.pie(
    df,
    values="order_id",
    names="delivery_status",
    title="Delivery status",
    width=600,
    height=600
    )
    fig.update_traces(hole=.55)
    return fig

def visualize_payment(df):
    fig = px.pie(
    df,
    values="count",
    names="name",
    title="Payment status",
    width=600,
    height=600
    )
    fig.update_traces(textinfo='percent+label', texttemplate='%{percent:.1%}', hole=.55)
    return fig


def visualize_product_by_review(df):
    highest_review_scores = df.sort_values(ascending=True, by="review_score").tail(10)
    lowest_review_scores = df.sort_values(ascending=True, by="review_score").head(10)
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Highest", "Lowest"],
        shared_yaxes=False  # Allow independent y-axes
    )
    fig.add_trace(
        go.Bar(
            y=highest_review_scores["product_category_name"],
            x=highest_review_scores["review_score"],
            text=highest_review_scores["review_score"],
            textposition="auto",
            orientation="h",
            marker_color="blue"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            y=lowest_review_scores["product_category_name"],
            x=lowest_review_scores["review_score"],
            text=lowest_review_scores["review_score"],
            textposition="auto",
            orientation="h",
            marker_color="red"
        ),
        row=1, col=2
    )
    fig.update_layout(
        height=600,
        width=1200,
        showlegend=False,
        xaxis_title="Review Score",
        xaxis2_title="Review Score",
        yaxis=dict(title="Product Category", automargin=True),
        yaxis2=dict(title="Product Category", automargin=True, side="right"),
        title='10 Products with highest and lowest review score'
    )

    return fig

