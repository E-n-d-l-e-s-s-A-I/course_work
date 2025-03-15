import streamlit as st
from routers.cargo.router import cargo_tab_page
from routers.city.router import city_tab_page
from routers.truck.router import truck_tab_page


def main_page():
    city_tab, path_tab, truck_tab, cargo_tab, task_tab = st.tabs(
        [
            "Города",
            "Пути",
            "Грузовики",
            "Грузы",
            "Поиск пути",
        ]
    )
    city_tab_page(city_tab)
    truck_tab_page(truck_tab)
    cargo_tab_page(cargo_tab)


main_page()
