import streamlit as st
from routers.city.schemas import CityBase
from routers.core_api import api


def city_tab_page(city_tab):
    """Логика вкладки городов."""

    with city_tab:
        cities = api.city.get_cities()
        city_name_to_id = {city.name: city.id for city in cities}
        cities_inner_ids = (city.name for city in cities)

        city_widget = st.multiselect(
            "Выбрать Город", cities_inner_ids, default=None, max_selections=1
        )

        st.divider()

        if city_widget:
            city_id = city_name_to_id[city_widget[0]]
            city = api.city.get_city(city_id)

            city_id = st.text_input("ID", value=city.id, disabled=True, key="city_id")
            city_name = st.text_input("Имя", value=city.name, key="city_name")

            col1, col2, _, _, _, _ = st.columns(6, gap="small")

            change_clicked = col1.button("Изменить", key="city_update_btn")
            if change_clicked:
                city_data = CityBase(name=city_name)
                try:
                    api.city.update_city(city_id, city_data)
                except Exception as error:
                    st.error(f"Город не обновлен по причине: {error}")
                else:
                    st.success("Город обновлен")

            delete_clicked = col2.button("Удалить", key="city_delete_btn")
            if delete_clicked:
                try:
                    api.city.delete_city(city_id)
                except Exception as error:
                    st.error(f"Город не удален по причине: {error}")
                else:
                    st.success("Город удален")

        else:
            city_name = st.text_input("Имя", key="city_name")
            city_data = CityBase(name=city_name)

            add_clicked = st.button("Добавить", key="city_create_btn")
            if add_clicked:
                try:
                    api.city.create_city(city_data)
                except Exception as error:
                    st.error(f"Город не создан по причине: {error}")
                else:
                    st.success("Город создан")
