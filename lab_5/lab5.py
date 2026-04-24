import streamlit as st
import pandas as pd
import glob
import plotly.express as px

st.set_page_config(page_title="Лабораторна 5: Аналіз NOAA", layout="wide")
st.title("Аналіз вегетаційних індексів (VCI, TCI, VHI) України 🇺🇦")

@st.cache_data
def load_and_clean_data():
    files = glob.glob("vhi_data/*.csv")
    if not files:
        st.error("Папку 'vhi_data' з файлами не знайдено! Переконайтеся, що ви запускаєте додаток у тій самій директорії, де виконували 2-гу лабу.")
        st.stop()
        
    dataframes = []
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    for file in files:
        province_id = int(file.split('vhi_id_')[1].split('_')[0])
        df = pd.read_csv(file, header=1, names=headers, skipinitialspace=True)
        df.drop(columns=['empty'], inplace=True, errors='ignore')
        df.dropna(subset=['VHI'], inplace=True)
        df['Year'] = df['Year'].astype(str).str.replace(r'<tt><pre>', '', regex=True)
        df = df[df['Year'] != '']
        df['Year'] = df['Year'].astype(int)
        df['Old_Province_ID'] = province_id
        dataframes.append(df)
        
    df_combined = pd.concat(dataframes, ignore_index=True)

    ukr_alphabet_order = [
        'Вінницька', 'Волинська', 'Дніпропетровська', 'Донецька', 'Житомирська',
        'Закарпатська', 'Запорізька', 'Івано-Франківська', 'Київська', 'Кіровоградська',
        'Луганська', 'Львівська', 'Миколаївська', 'Одеська', 'Полтавська',
        'Рівненська', 'Сумська', 'Тернопільська', 'Харківська', 'Херсонська',
        'Хмельницька', 'Черкаська', 'Чернівецька', 'Чернігівська', 
        'Республіка Крим', 'м. Київ', 'м. Севастополь'
    ]
    mapping = {idx: province for idx, province in enumerate(ukr_alphabet_order, start=1)}
    old_to_new = {1:22, 2:24, 3:23, 4:25, 5:3, 6:4, 7:8, 8:19, 9:20, 10:21, 11:9, 12:26, 
                  13:10, 14:11, 15:12, 16:13, 17:14, 18:15, 19:16, 20:27, 21:17, 22:18, 
                  23:6, 24:1, 25:2, 26:7, 27:5}
    
    df_combined['Province_ID'] = df_combined['Old_Province_ID'].map(old_to_new)
    df_combined['Province_Name'] = df_combined['Province_ID'].map(mapping)

    df_combined = df_combined[(df_combined['VHI'] >= 0) & (df_combined['VCI'] >= 0) & (df_combined['TCI'] >= 0)]
    return df_combined

df = load_and_clean_data()

default_year_min, default_year_max = int(df['Year'].min()), int(df['Year'].max())

def reset_filters():
    st.session_state.indicator = "VHI"
    st.session_state.region = "Вінницька"
    st.session_state.year_range = (default_year_min, default_year_max)
    st.session_state.week_range = (1, 52)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

st.sidebar.header(" Параметри фільтрації")

st.sidebar.button(" Скинути всі фільтри", on_click=reset_filters, use_container_width=True)
st.sidebar.markdown("---")

indicator = st.sidebar.selectbox("Оберіть індекс:", ["VHI", "VCI", "TCI"], key="indicator")
region = st.sidebar.selectbox("Оберіть область:", df['Province_Name'].dropna().unique(), key="region")

years = st.sidebar.slider("Інтервал років:", 
                          min_value=default_year_min, max_value=default_year_max, 
                          value=(default_year_min, default_year_max), key="year_range")

weeks = st.sidebar.slider("Інтервал тижнів:", 1, 52, (1, 52), key="week_range")

st.sidebar.markdown("---")
st.sidebar.subheader("Сортування таблиці")
sort_asc = st.sidebar.checkbox("За зростанням (Min -> Max)", key="sort_asc")
sort_desc = st.sidebar.checkbox("За спаданням (Max -> Min)", key="sort_desc")

if sort_asc and sort_desc:
    st.sidebar.warning("Обрано обидва сортування! Пріоритет надано сортуванню 'За зростанням'.")
    sort_desc = False

df_filtered = df[
    (df['Province_Name'] == region) & 
    (df['Year'] >= years[0]) & (df['Year'] <= years[1]) &
    (df['Week'] >= weeks[0]) & (df['Week'] <= weeks[1])
].copy()

if sort_asc:
    df_filtered = df_filtered.sort_values(by=indicator, ascending=True)
elif sort_desc:
    df_filtered = df_filtered.sort_values(by=indicator, ascending=False)

df_filtered['Date_Label'] = df_filtered['Year'].astype(str) + " - Тиждень " + df_filtered['Week'].astype(str)

tab1, tab2, tab3 = st.tabs([" Таблиця даних", " Динаміка індексу", " Порівняння областей"])

with tab1:
    st.subheader(f"Дані: {region} область ({indicator})")
    st.dataframe(df_filtered[['Year', 'Week', 'Province_Name', 'VCI', 'TCI', 'VHI']], use_container_width=True)

with tab2:
    st.subheader(f"Часовий ряд {indicator} для області: {region}")
    if not df_filtered.empty:
        df_plot = df_filtered.sort_values(by=['Year', 'Week'])
        fig1 = px.line(df_plot, x='Date_Label', y=indicator, markers=True,
                       labels={'Date_Label': 'Рік та Тиждень', indicator: f'Значення {indicator}'})
        fig1.update_xaxes(showticklabels=False) 
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Немає даних за обраний період.")

with tab3:
    st.subheader(f"Порівняння середнього {indicator} (Роки: {years[0]}-{years[1]}, Тижні: {weeks[0]}-{weeks[1]})")
    df_all_regions = df[
        (df['Year'] >= years[0]) & (df['Year'] <= years[1]) &
        (df['Week'] >= weeks[0]) & (df['Week'] <= weeks[1])
    ]
    if not df_all_regions.empty:
        avg_data = df_all_regions.groupby('Province_Name')[indicator].mean().reset_index()
        avg_data = avg_data.sort_values(by=indicator, ascending=False)
        avg_data['Color'] = avg_data['Province_Name'].apply(lambda x: 'Обрана область' if x == region else 'Інші')
        color_map = {'Обрана область': '#ef553b', 'Інші': '#636efa'}
        
        fig2 = px.bar(avg_data, x='Province_Name', y=indicator, color='Color', color_discrete_map=color_map,
                      labels={'Province_Name': 'Область', indicator: f'Середній {indicator}'})
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Немає даних для побудови графіка.")