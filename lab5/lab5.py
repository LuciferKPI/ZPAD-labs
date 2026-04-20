import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

os.makedirs('.streamlit', exist_ok=True)
with open('.streamlit/config.toml', 'w', encoding='utf-8') as f:
    f.write("""
[theme]
primaryColor = "#6d28d9"
backgroundColor = "#18181b"
secondaryBackgroundColor = "#27272a"
textColor = "#e4e4e7"
font = "sans serif"
""")

st.set_page_config(layout="wide", page_title="ЗПАД Лабораторна 5")

THEME_BG = "#18181b"
THEME_PRIMARY = "#6d28d9"
THEME_TEXT = "#e4e4e7"
THEME_GRID = "#3f3f46"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {THEME_BG}; color: {THEME_TEXT}; }}
    [data-testid="stSidebar"] {{ background-color: #27272a; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        data = pd.read_csv('vhi_data_cleaned.csv')
        return data
    except FileNotFoundError:
        st.error("Файл vhi_data_cleaned.csv не знайдено")
        return pd.DataFrame()

def reset_filters():
    if not df.empty:
        st.session_state.indicator_sel = "VCI"
        st.session_state.province_sel = df['Province_Name'].unique()[0]
        st.session_state.week_slider = (int(df['Week'].min()), int(df['Week'].max()))
        st.session_state.year_slider = (int(df['Year'].min()), int(df['Year'].max()))
        st.session_state.sort_asc = False
        st.session_state.sort_desc = False

def apply_custom_plot_style(fig, ax):
    fig.patch.set_facecolor(THEME_BG)
    ax.set_facecolor(THEME_BG)
    ax.tick_params(colors=THEME_TEXT)
    ax.xaxis.label.set_color(THEME_TEXT)
    ax.yaxis.label.set_color(THEME_TEXT)
    ax.title.set_color(THEME_TEXT)
    ax.spines['bottom'].set_color(THEME_GRID)
    ax.spines['top'].set_color(THEME_BG)
    ax.spines['right'].set_color(THEME_BG)
    ax.spines['left'].set_color(THEME_GRID)

df = load_data()

if not df.empty:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Фільтри")
        
        indicator = st.selectbox("Оберіть показник", ["VCI", "TCI", "VHI"], key="indicator_sel")
        province = st.selectbox("Оберіть область", df['Province_Name'].unique(), key="province_sel")

        week_range = st.slider("Інтервал тижнів", 
                               int(df['Week'].min()), int(df['Week'].max()), 
                               (int(df['Week'].min()), int(df['Week'].max())),
                               key="week_slider")

        year_range = st.slider("Інтервал років", 
                               int(df['Year'].min()), int(df['Year'].max()), 
                               (int(df['Year'].min()), int(df['Year'].max())),
                               key="year_slider")

        st.markdown("---")
        st.write("Сортування:")
        sort_asc = st.checkbox("За зростанням", key="sort_asc")
        sort_desc = st.checkbox("За спаданням", key="sort_desc")

        sort_mode = None
        if sort_asc and sort_desc:
            st.warning("Увімкнено обидва чекбокси. Сортування скасовано.")
        elif sort_asc:
            sort_mode = True
        elif sort_desc:
            sort_mode = False

        st.markdown("---")
        st.button("Скинути всі фільтри", on_click=reset_filters)

    filtered_df = df[
        (df['Province_Name'] == province) &
        (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    ].sort_values(by=['Year', 'Week'])

    sorted_df = filtered_df.copy()
    if sort_mode is not None and not (sort_asc and sort_desc):
        sorted_df = sorted_df.sort_values(by=indicator, ascending=sort_mode)

    with col2:
        tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік показника", "Порівняння областей"])

        with tab1:
            st.subheader(f"Дані для: {province}")
            st.dataframe(sorted_df, use_container_width=True)

        with tab2:
            st.subheader(f"Динаміка {indicator}")
            if not filtered_df.empty:
                fig, ax = plt.subplots(figsize=(10, 5))
                apply_custom_plot_style(fig, ax)
                
                x_axis = filtered_df['Year'].astype(str) + "-W" + filtered_df['Week'].astype(str)
                ax.plot(x_axis, filtered_df[indicator], color=THEME_PRIMARY, linewidth=2)
                
                ax.set_ylabel(indicator)
                ax.grid(True, linestyle='--', alpha=0.4, color=THEME_GRID)
                ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=15))
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.info("Немає даних для відображення")

        with tab3:
            st.subheader(f"Порівняння {indicator}")
            compare_df = df[
                (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
                (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
            ].sort_values(by=['Year', 'Week'])
            
            if not compare_df.empty:
                fig2, ax2 = plt.subplots(figsize=(10, 5))
                apply_custom_plot_style(fig2, ax2)
                
                for prov in compare_df['Province_Name'].unique():
                    if prov != province:
                        prov_data = compare_df[compare_df['Province_Name'] == prov]
                        ax2.plot(prov_data['Year'] + prov_data['Week']/52, prov_data[indicator], 
                                 color="#3f3f46", linewidth=0.8, alpha=0.4)
                
                my_data = compare_df[compare_df['Province_Name'] == province]
                ax2.plot(my_data['Year'] + my_data['Week']/52, my_data[indicator], 
                         color=THEME_PRIMARY, linewidth=2.5, zorder=10)
                
                ax2.grid(True, linestyle='--', alpha=0.4, color=THEME_GRID)
                ax2.set_ylabel(indicator)
                ax2.set_xlabel("Рік")
                st.pyplot(fig2)
                st.caption(f"Обрана область: {province} виділена фіолетовим кольором")