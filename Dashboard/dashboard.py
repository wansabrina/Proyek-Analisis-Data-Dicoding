import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import FuncFormatter
import streamlit as st

st.header('Brazil E-Commerce Dashboard 📈')

df = pd.read_csv('all_data.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month

st.sidebar.header('Filter Statistik')
years = ['Semua'] + sorted(df['year'].unique())
selected_year = st.sidebar.selectbox('Pilih Tahun', options=years)

months = ['Semua'] + list(range(1, 13))
month_names = ['Semua'] + \
    [pd.to_datetime(str(x), format='%m').strftime('%B') for x in range(1, 13)]
selected_month = st.sidebar.selectbox('Pilih Bulan', options=range(
    len(month_names)), format_func=lambda x: month_names[x])

states = ['Semua'] + sorted(df['customer_state'].unique().tolist())
selected_state = st.sidebar.selectbox('Pilih State', options=states)

if selected_year != 'Semua':
    filtered_df = df[df['year'] == selected_year]
else:
    filtered_df = df

if selected_month != 0:
    filtered_df = filtered_df[filtered_df['month'] == selected_month]

if selected_state != 'Semua':
    filtered_df = filtered_df[filtered_df['customer_state'] == selected_state]

total_orders_filtered = len(filtered_df)
total_sales_filtered = filtered_df['price'].sum()

if selected_month == 0:
    month_display = "Semua Bulan"
else:
    month_display = pd.to_datetime(
        str(selected_month), format='%m').strftime('%B')

st.write(
    f"#### Total Penjualan untuk {month_display} Tahun {selected_year} dan State {selected_state if selected_state != 'Semua' else 'Semua State'}")
col1, col2 = st.columns(2)
col1.metric("Total Pesanan", total_orders_filtered)
col2.metric("Total Penjualan", f"R$ {total_sales_filtered:.2f}")
st.markdown('<font color="gray">\* Pilih Tahun, Bulan dan State (Opsional) di sidebar untuk melihat statistik secara spesifik</font>', unsafe_allow_html=True)

customers_state_grouped = df.groupby(by="customer_state")[
    'customer_id'].nunique().sort_values(ascending=False).reset_index()

st.write('#### :star: Statistik Total Pesanan (Order) per tahun')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month

orders_per_month_year = df.groupby(
    ['year', 'month']).size().reset_index(name='total_orders')

orders_per_month_year['year_month'] = pd.to_datetime(
    orders_per_month_year[['year', 'month']].assign(DAY=1))

start_date = orders_per_month_year['year_month'].min()
end_date = orders_per_month_year['year_month'].max()

all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
all_months_df = pd.DataFrame(all_months, columns=['year_month'])
orders_per_month_year_complete = pd.merge(
    all_months_df, orders_per_month_year, on='year_month', how='left').fillna(0)

plt.figure(figsize=(14, 7))
sns.lineplot(x='year_month', y='total_orders',
             data=orders_per_month_year_complete, color='pink', marker="o")
plt.title('Total Pesanan (Order) per Bulan per Tahun')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Total Pesanan')
plt.xticks(rotation=45)
plt.grid(True)

plt.gca().set_xticks(orders_per_month_year_complete['year_month'])
plt.gca().set_xticklabels([date.strftime(
    '%Y-%m') for date in orders_per_month_year_complete['year_month']], rotation=45)

st.pyplot(plt)
st.write('\* Abaikan data 2 bulan terakhir karena data mungkin belum lengkap')

st.write('#### :star: Statistik Total Penjualan (Sum of Price) per tahun')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month

total_payment_per_month_year = df.groupby(
    ['year', 'month'])['payment_value'].sum().reset_index()

total_payment_per_month_year['year_month'] = pd.to_datetime(
    total_payment_per_month_year[['year', 'month']].assign(DAY=1))

start_date = total_payment_per_month_year['year_month'].min()
end_date = total_payment_per_month_year['year_month'].max()

all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
all_months_df = pd.DataFrame(all_months, columns=['year_month'])
total_payment_per_month_year_complete = pd.merge(
    all_months_df, total_payment_per_month_year, on='year_month', how='left').fillna(0)

plt.figure(figsize=(14, 7))
sns.lineplot(x='year_month', y='payment_value',
             data=total_payment_per_month_year_complete, color='pink', marker="o")
plt.title('Total Penjualan per Bulan per Tahun')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45)
plt.grid(True)
plt.gca().set_xticks(total_payment_per_month_year_complete['year_month'])
plt.gca().set_xticklabels([date.strftime(
    '%Y-%m') for date in total_payment_per_month_year_complete['year_month']], rotation=45)
plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))

st.pyplot(plt)
st.write('\* Abaikan data 2 bulan terakhir karena data mungkin belum lengkap')

st.write('#### :star: Jumlah Pelanggan Berdasarkan Negara Bagian (State) dan Kota')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['month'] = df['order_purchase_timestamp'].dt.month

customers_state_grouped = df.groupby(by="customer_state")[
    'customer_id'].nunique().sort_values(ascending=False).reset_index()
customers_city_grouped = df.groupby(by="customer_city")[
    'customer_id'].nunique().sort_values(ascending=False).reset_index()
customers_city_grouped_top10 = customers_city_grouped.head(10)

sum_of_price_per_state = df.groupby('customer_state')[
    'price'].sum().sort_values(ascending=False).reset_index()
sales_heatmap_data = df.groupby(['customer_state', 'month'])[
    'price'].sum().unstack()

fig1, ax1 = plt.subplots(figsize=(10, 8))
sns.barplot(ax=ax1, x='customer_id', y='customer_state',
            data=customers_state_grouped, palette='RdPu_r')
ax1.set_xlabel('Jumlah Pelanggan')
ax1.set_ylabel('Negara Bagian')
ax1.set_title('Jumlah Pelanggan per Negara Bagian (State)')

fig2, ax2 = plt.subplots(figsize=(10, 8))
sns.barplot(ax=ax2, x='customer_id', y='customer_city',
            data=customers_city_grouped_top10, palette='RdPu_r')
ax2.set_xlabel('Jumlah Pelanggan')
ax2.set_ylabel('Kota')
ax2.set_title('Jumlah Pelanggan per Kota')

fig3, ax3 = plt.subplots(figsize=(10, 8))
sns.barplot(ax=ax3, x='price', y='customer_state',
            data=sum_of_price_per_state, palette='Reds_r')
ax3.set_xlabel('Total Penjualan')
ax3.set_ylabel('Negara Bagian')
ax3.set_title('Total Penjualan per Negara Bagian')
ax3.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

fig4, ax4 = plt.subplots(figsize=(10, 8))
sns.heatmap(sales_heatmap_data, cmap='Reds', ax=ax4)
ax4.set_title('Heatmap Total Penjualan per Negara Bagian per Bulan')
ax4.set_xlabel('Bulan')
ax4.set_ylabel('Negara Bagian')

col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)

st.write('#### :star: Total Penjualan per Negara Bagian')
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig3)
with col2:
    st.pyplot(fig4)

st.write('#### :star: Rata-rata Pengeluaran Belanja Per Negara Bagian')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

state_spending = df.groupby('customer_state')['payment_value'].mean(
).reset_index().sort_values('payment_value', ascending=False)

plt.figure(figsize=(15, 7))
sns.barplot(x='customer_state', y='payment_value',
            data=state_spending, palette='viridis')
plt.title('Average Customer Spend per State')
plt.xlabel('State')
plt.ylabel('Average Spend ($)')
plt.xticks(rotation=90)
plt.tight_layout()

st.pyplot(plt)

st.write('#### :star: Rata-rata Nilai Pengiriman (Freight) per Tahun')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month
df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

avg_freight_per_month_year = df.groupby(
    ['year_month'])['freight_value'].mean().reset_index()

plt.figure(figsize=(14, 7))
sns.lineplot(x='year_month', y='freight_value',
             data=avg_freight_per_month_year, color='pink', marker="o")

plt.title('Rata-Rata Nilai Pengiriman (Freight) per Bulan per Tahun')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Rata-Rata Nilai Pengiriman')
plt.xticks(rotation=45)
plt.grid(True)

plt.gca().set_xticklabels(
    avg_freight_per_month_year['year_month'], rotation=45)

st.pyplot(plt)


st.write('#### :star: Rata-rata Skor Ulasan per Tahun')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['year'] = df['order_purchase_timestamp'].dt.year
df['month'] = df['order_purchase_timestamp'].dt.month

avg_review_score_per_month_year = df.groupby(
    ['year', 'month'])['review_score'].mean().reset_index()

avg_review_score_per_month_year['year_month'] = pd.to_datetime(
    avg_review_score_per_month_year[['year', 'month']].assign(DAY=1))

start_date = '2017-01-01'
end_date = avg_review_score_per_month_year['year_month'].max()

all_months = pd.date_range(start=start_date, end=end_date, freq='MS')
all_months_df = pd.DataFrame(all_months, columns=['year_month'])
avg_review_score_per_month_year_complete = pd.merge(
    all_months_df, avg_review_score_per_month_year, on='year_month', how='left').fillna(0)

plt.figure(figsize=(14, 7))
sns.lineplot(x='year_month', y='review_score',
             data=avg_review_score_per_month_year_complete, color='pink', marker="o")
plt.title('Rata-Rata Skor Ulasan per Bulan per Tahun')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Rata-Rata Skor Ulasan')
plt.xticks(rotation=45)
plt.grid(True)

plt.gca().set_xticks(avg_review_score_per_month_year_complete['year_month'])
plt.gca().set_xticklabels([date.strftime(
    '%Y-%m') for date in avg_review_score_per_month_year_complete['year_month']], rotation=45)

plt.gca().yaxis.set_major_formatter(
    FuncFormatter(lambda x, _: '{:.2f}'.format(x)))

st.pyplot(plt)

st.caption('Copyright (c) Wan Sabrina Mayzura')
