import streamlit as st
from routers.core_api import crud_api
from routers.truck.schemas import TruckBase
from routers.utils import error_to_readable_view


def truck_tab_page(truck_tab):
    """Логика вкладки грузовиков."""

    with truck_tab:
        trucks = crud_api.truck.get_trucks()
        truck_name_to_id = {truck.name: truck.id for truck in trucks}
        trucks_inner_ids = (truck.name for truck in trucks)

        truck_widget = st.multiselect(
            "Выбрать Грузовик",
            trucks_inner_ids,
            default=None,
            max_selections=1,
        )

        st.divider()
        if not truck_widget:
            st.subheader("Создать грузовик")

        if truck_widget:
            truck_id = truck_name_to_id[truck_widget[0]]
            truck = crud_api.truck.get_truck(truck_id)

            truck_id = st.text_input("ID", value=truck.id, disabled=True, key="truck_id")
            truck_name = st.text_input("Имя", value=truck.name, key="truck_name")
            truck_speed = st.number_input("Скорость", value=truck.speed, key="truck_speed")
            truck_weight = st.number_input("Масса", value=truck.weight, key="truck_weight")
            truck_height = st.number_input("Высота", value=truck.height, key="truck_height")
            truck_max_cargo_weight = st.number_input(
                "Максимальная масса груза",
                value=truck.max_cargo_weight,
                key="truck_max_cargo_weight",
            )

            col1, col2, _, _, _, _ = st.columns(6, gap="small")

            change_clicked = col1.button("Изменить", key="truck_update_btn")
            if change_clicked:
                truck_data = TruckBase(
                    name=truck_name,
                    speed=truck_speed,
                    weight=truck_weight,
                    height=truck_height,
                    max_cargo_weight=truck_max_cargo_weight,
                )
                try:
                    crud_api.truck.update_truck(truck_id, truck_data)
                except Exception as error:
                    st.error(f"Грузовик не обновлен по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Грузовик обновлен")

            delete_clicked = col2.button("Удалить", key="truck_delete_btn")
            if delete_clicked:
                try:
                    crud_api.truck.delete_truck(truck_id)
                except Exception as error:
                    st.error(f"Грузовик не удален по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Грузовик удален")

        else:
            truck_name = st.text_input("Имя", key="truck_name")
            truck_speed = st.number_input("Скорость", key="truck_speed")
            truck_height = st.number_input("Высота", key="truck_height")
            truck_weight = st.number_input("Масса", key="truck_weight")
            truck_max_cargo_weight = st.number_input(
                "Максимальная масса груза",
                key="truck_max_cargo_weight",
            )
            truck_data = TruckBase(
                name=truck_name,
                speed=truck_speed,
                weight=truck_weight,
                height=truck_height,
                max_cargo_weight=truck_max_cargo_weight,
            )

            add_clicked = st.button("Добавить", key="truck_create_btn")
            if add_clicked:
                try:
                    crud_api.truck.create_truck(truck_data)
                except Exception as error:
                    st.error(f"Грузовик не создан по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Грузовик создан")
