import geopandas as gpd
import folium
from folium.features import GeoJsonPopup, GeoJsonTooltip
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import json
import branca
import plotly.graph_objects as go
import os

# Загрузка данных
df_reset = pd.read_excel('region_excel.xlsx')

# Определение параметров для выпадающих списков
regions = df_reset['region'].unique()
sectors = df_reset.columns[2:]  # Предполагается, что первые два столбца — 'year' и 'region'

# Определение функций для каждого графика

# График 1: Уровень износа выбранного сектора в выбранном регионе
def plot_sector_wear(selected_region, selected_sector):
    filtered_data = df_reset[df_reset['region'] == selected_region]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data['year'],
        y=filtered_data[selected_sector],
        mode='lines+markers',
        name=f'Уровень износа {selected_sector} в {selected_region}'
    ))

    fig.update_layout(
        title=f"Уровень износа {selected_sector} в {selected_region} (2000-2024)",
        xaxis_title="Год",
        yaxis_title="Уровень износа",
        yaxis=dict(range=[0, 100])
    )
    return fig

# График 2: Уровни износа всех секторов в регионе
def plot_all_sector_wear(selected_region):
    filtered_data = df_reset[df_reset['region'] == selected_region]
    
    fig = go.Figure()
    for sector in sectors:
        fig.add_trace(go.Scatter(
            x=filtered_data['year'],
            y=filtered_data[sector],
            mode='lines+markers',
            name=sector
        ))

    fig.update_layout(
        title=f"Уровни износа по секторам в {selected_region} (2000-2024)",
        xaxis_title="Год",
        yaxis_title="Уровень износа",
        yaxis=dict(range=[0, 100]),
        legend_title="Секторы"
    )
    return fig

# График 3: Затраты в определенном секторе выбранного региона
def plot_spending_sector(selected_region, selected_sector):
    filtered_data = df_reset[df_reset['region'] == selected_region]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data['year'],
        y=filtered_data[selected_sector],
        mode='lines+markers',
        name=f'{selected_sector} в {selected_region}'
    ))

    fig.update_layout(
        title=f'Затраты в {selected_region} - {selected_sector}',
        xaxis_title="Год",
        yaxis_title="Затраты"
    )
    return fig

# График 4: Затраты по всем секторам в регионе
def plot_spending_all_sectors(selected_region):
    filtered_data = df_reset[df_reset['region'] == selected_region]
    
    fig = go.Figure()
    for sector in sectors:
        fig.add_trace(go.Scatter(
            x=filtered_data['year'],
            y=filtered_data[sector],
            mode='lines+markers',
            name=sector
        ))

    fig.update_layout(
        title=f"Затраты по всем секторам в {selected_region}",
        xaxis_title="Год",
        yaxis_title="Затраты",
        legend_title="Секторы"
    )
    return fig

# Разметка приложения Streamlit

# Заголовок страницы
st.title("Аналитическая панель инфраструктуры Казахстана")

# Раздел 1: Уровень износа выбранного сектора в регионе
st.header("1. Уровень износа выбранного сектора в регионе")
st.write("""
    Этот график отображает динамику уровня износа в определённом секторе за период с 2000 по 2024 год. 
    Выберите регион и сектор из списка, чтобы увидеть, как уровень износа изменялся в течение этого времени. 
    График строится на основе данных о состоянии инфраструктуры по каждому году и позволяет оценить тенденции износа в выбранной области.
""")
selected_region_1 = st.selectbox("Выберите регион", regions, key="region1")
selected_sector_1 = st.selectbox("Выберите сектор", sectors, key="sector1")

fig_sector_wear = plot_sector_wear(selected_region_1, selected_sector_1)
st.plotly_chart(fig_sector_wear)

st.write("---")  # Разделитель

# Раздел 2: Уровни износа всех секторов в выбранном регионе
st.header("2. Уровни износа всех секторов в выбранном регионе")
st.write("""
    Этот график отображает данные об уровне износа всех секторов инфраструктуры (например, транспорт, энергетика, социальное обеспечение) 
    в выбранном регионе за период с 2000 по 2024 год. С помощью этого графика можно сравнить износ разных секторов и выделить те, 
    которые требуют наибольшего внимания и инвестиций.
""")
selected_region_2 = st.selectbox("Выберите регион", regions, key="region2")

fig_all_sector_wear = plot_all_sector_wear(selected_region_2)
st.plotly_chart(fig_all_sector_wear)

st.write("---")  # Разделитель

# Раздел 3: Затраты в определенном секторе выбранного региона
st.header("3. Затраты в определенном секторе выбранного региона")
st.write("""
    Этот график показывает, сколько средств было потрачено на развитие и поддержание выбранного сектора инфраструктуры 
    в определённом регионе за период с 2000 по 2024 год. Он позволяет понять, как распределялись финансовые ресурсы 
    и как это связано с изменениями в уровне износа и потребностями сектора.
""")
selected_region_3 = st.selectbox("Выберите регион", regions, key="region3")
selected_sector_3 = st.selectbox("Выберите сектор", sectors, key="sector3")

fig_spending_sector = plot_spending_sector(selected_region_3, selected_sector_3)
st.plotly_chart(fig_spending_sector)

st.write("---")

# Раздел 4: Затраты по всем секторам в выбранном регионе
st.header("4. Затраты по всем секторам в выбранном регионе")
st.write("""
    Этот график иллюстрирует общие затраты по всем секторам в выбранном регионе на протяжении последних 24 лет. 
    Он помогает увидеть, как распределялись инвестиции по различным секторам и как это могло повлиять на состояние инфраструктуры региона.
""")
selected_region_spending = st.selectbox("Выберите регион", regions, key="region4")

fig_spending_all_sectors = plot_spending_all_sectors(selected_region_spending)
st.plotly_chart(fig_spending_all_sectors)

st.write("---")

# Загрузка данных GeoJSON
gdf = gpd.read_file('kazakhstan_regions_simplified.geojson')

# Конвертация данных JSON в DataFrame
folder_path = 'clustering_data'

# Initialize an empty list to hold priority data
priority_data = []

# Iterate through each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):  # Only process JSON files
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            priorities = json.load(file)  # Load the JSON content
            
            # Extract priority data from the JSON
            industry = os.path.splitext(file_name)[0]  # Use file name as industry name
            for priority, region_list in priorities.items():
                for region in region_list:
                    priority_data.append({'region': region, 'priority': int(priority), 'industry': industry})

# Convert the list to a DataFrame
priority_df = pd.DataFrame(priority_data)

# Приложение Streamlit
st.header("Интерактивная карта ранжирования регионов Казахстана по отраслям")
st.write("""
    Интерактивная карта позволяет выбрать отрасль и просмотреть рейтинг приоритетности регионов по различным аспектам (например, уровень износа инфраструктуры). 
    Каждый регион на карте будет окрашен в зависимости от приоритета, что помогает визуализировать, какие регионы требуют наиболее срочных мер для улучшения состояния инфраструктуры.
""")
st.write("Выберите отрасль, чтобы просмотреть приоритетные рейтинги регионов.")

# Выпадающий список для выбора отрасли
industry = st.selectbox("Выберите отрасль", priority_df['industry'].unique())

# Фильтрация DataFrame по выбранной отрасли
industry_df = priority_df[priority_df['industry'] == industry]

# Объединение GeoDataFrame с данными приоритетов
gdf = gdf.merge(industry_df, left_on='shapeName', right_on='region')

# Определение цветовой шкалы на основе приоритетов (с использованием линейной шкалы branca)
min_priority = gdf['priority'].min()
max_priority = gdf['priority'].max()

color_scale = branca.colormap.linear.YlOrRd_09.scale(min_priority, max_priority)

# Создание карты folium
m = folium.Map(location=[48.0196, 66.9237], zoom_start=4)

# Добавление слоя GeoJson с пользовательским стилем
folium.GeoJson(
    gdf.to_json(),
    name="Регионы Казахстана",
    zoom_on_click=True,
    popup_keep_highlighted=True,
    tooltip=GeoJsonTooltip(fields=["shapeName"], aliases=["Регион:"]),
    popup=GeoJsonPopup(
        fields=["shapeName", "priority"],
        aliases=["Название региона:", "Приоритет:"],
        localize=True,
        labels=True,
        style="background-color: white; font-size: 14px; padding: 10px;"
    ),
    style_function=lambda feature: {
        'fillColor': color_scale(feature['properties']['priority']),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.9,
    },
    highlight_function=lambda feature: {
        'fillColor': '#1f78b4',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.9,
    }
).add_to(m)

# Добавление легенды цветовой шкалы на карту
color_scale.add_to(m)

# Отображение карты в Streamlit
st_folium(m, width=700, height=500)
