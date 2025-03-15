import streamlit as st
from settings import settings


def main_page():
    city_tab, path_tab, truck_tab, cargo_tab, task_tab = st.tabs([
        'Города',
        'Пути',
        'Грузы',
        'Грузовики',
        'Поиск пути',
    ])


main_page()

