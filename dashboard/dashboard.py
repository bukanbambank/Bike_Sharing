import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Setting seaborn style
sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D').agg({
        "cnt": "sum"
    }).reset_index()
    
    daily_rentals_df.rename(columns={
        "cnt": "total_rentals"
    }, inplace=True)
    
    return daily_rentals_df

# Load cleaned data
hour_df = pd.read_csv("hour_df.csv")
day_df = pd.read_csv("day_df.csv")

day_2011_df = day_df[day_df["yr"] == 0]

# Convert datetime columns to datetime objects
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
hour_df.set_index("dteday", inplace=True)

# Filter data
min_date = hour_df.index.min()
max_date = hour_df.index.max()

with st.sidebar:    
    # Selecting start_date and end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df.index >= str(start_date)) & 
                (hour_df.index <= str(end_date))]

# Prepare various dataframes
daily_rentals_df = create_daily_rentals_df(main_df)

# Streamlit application
st.title('Bike Sharing Dashboard :sparkles:')

# Display total rentals
st.subheader('Total Rentals')
total_rentals = daily_rentals_df.total_rentals.sum()
st.metric("Total Rentals", value=total_rentals)


# Pertanyaan 1: Perbandingan Penyewaan Sepeda Setiap Bulan (Pada tahun 2011)
st.subheader('Perbandingan Penyewaan Sepeda Setiap Bulan (Pada tahun 2011)')
user_monthly = day_2011_df.groupby(by='mnth').agg({
    'cnt': ['sum']
}).reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=user_monthly, x='mnth', y=('cnt', 'sum'), ax=ax)
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Jumlah Penyewaan Sepeda per Bulan (2011)')
ax.set_xticks(range(12))
ax.set_xticklabels([
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
], rotation=45)

st.pyplot(fig)

# Pertanyaan 2: Pengaruh kondisi cuaca
st.subheader('Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda')
weather_stats = hour_df.groupby('weathersit')['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_stats, ax=ax)
ax.set_yscale('log')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
for index, row in weather_stats.iterrows():
    ax.text(index, row['cnt'] * 1.05, int(row['cnt']), color='black', ha="center")

st.pyplot(fig)

# Pertanyaan 3: Pengaruh hari kerja
st.subheader('Pengaruh Hari Kerja terhadap Penyewaan Sepeda')
weekend_rentals = hour_df.groupby('workingday')['cnt'].sum()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(weekend_rentals, labels=['Hari Libur', 'Hari Kerja'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'], wedgeprops=dict(width=0.3))
ax.set_title('Proporsi Jumlah Penyewaan Sepeda pada Hari Kerja dan Hari Libur')

st.pyplot(fig)

# Pertanyaan 4: Tren penyewaan sepeda setiap jamnya
st.subheader('Tren Penyewaan Sepeda Setiap Jam')
hourly_rentals = hour_df.groupby('hr')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_rentals, x='hr', y='cnt', marker='o', ax=ax)
ax.set_title('Tren Penyewaan Sepeda per Jam (rata-rata selama 2011-2012)')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewa')
ax.set_xticks(range(0, 24))
ax.grid(True)

st.pyplot(fig)
