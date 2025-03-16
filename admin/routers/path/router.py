import streamlit as st
from routers.core_api import api
from routers.path.schemas import PathBase, PathWithCities
from routers.path.utils import get_cities_names, get_city_id_by_name, get_city_name, get_path_name
from routers.utils import error_to_readable_view


def create_city_select_box(label: str, key: str, disabled: bool, current_value = None):
    cities = get_cities_names()
    index = None

    if current_value:
        index = cities.index(current_value)
    return st.selectbox(
        label,
        cities,
        key=key,
        index=index,
        disabled=disabled,
    )

def path_tab_page(path_tab):
    """Логика вкладки грузов."""

    with path_tab:
        paths = api.path.get_paths()
        path_name_to_id = {get_path_name(path): path.id for path in paths}
        paths_names = list(path_name_to_id)

        path_widget = st.multiselect(
            "Выбрать Путь",
            paths_names,
            default=None,
            max_selections=1,
        )

        st.divider()

        if path_widget:
            path_id = path_name_to_id[path_widget[0]]
            path = api.path.get_path(path_id)

            path_id = st.text_input("ID", value=path.id, disabled=True, key="path_id")
            path_city_from = create_city_select_box(
                label="Город отправления",
                key="city_from_name_view",
                current_value=get_city_name(city_id=path.city_from_id),
                disabled=True,
            )
            path_city_to = create_city_select_box(
                label="Город прибытия",
                key="city_to_name_view",
                current_value=get_city_name(city_id=path.city_to_id),
                disabled=True,
            )
            path_distance = st.number_input("Расстояние", value=path.distance, key="path_distance")
            path_max_height = st.number_input(
                "Максимально допустимая высота на пути",
                value=path.max_height,
                key="path_max_height",
            )
            path_max_weight = st.number_input(
                "Максимально допустимая масса на пути",
                value=path.max_weight,
                key="path_max_weight",
            )

            col1, col2, _, _, _, _ = st.columns(6, gap="small")

            change_clicked = col1.button("Изменить", key="path_update_btn")
            if change_clicked:
                path_data = PathBase(
                    distance=path_distance,
                    max_height=path_max_height,
                    max_weight=path_max_weight,
                )
                try:
                    api.path.update_path(path_id, path_data)
                except Exception as error:
                    st.error(f"Путь не обновлен по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Путь обновлен")

            delete_clicked = col2.button("Удалить", key="path_delete_btn")
            if delete_clicked:
                try:
                    api.path.delete_path(path_id)
                except Exception as error:
                    st.error(f"Путь не удален по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Путь удален")

        else:
            path_city_from = create_city_select_box(
                label="Город отправления",
                key="city_from_name",
                disabled=False,
            )
            path_city_to = create_city_select_box(
                label="Город прибытия",
                key="city_to_name",
                disabled=False,
            )
            path_distance = st.number_input("Расстояние", key="path_distance")
            path_max_height = st.number_input(
                "Максимально допустимая высота на пути",
                key="path_max_height",
            )
            path_max_weight = st.number_input(
                "Максимально допустимая масса на пути",
                key="path_max_weight",
            )
            if all(
                widget is not None
                for widget in [
                    path_city_from,
                    path_city_to,
                ]
            ):
                add_clicked = st.button("Добавить", key="path_create_btn")
            else:
                add_clicked = st.button("Добавить", key="path_create_btn", disabled=True)

            if add_clicked:
                path_data = PathWithCities(
                    city_from_id=get_city_id_by_name(path_city_from),
                    city_to_id=get_city_id_by_name(path_city_to),
                    distance=path_distance,
                    max_height=path_max_height,
                    max_weight=path_max_weight,
                )
                try:
                    api.path.create_path(path_data)
                except Exception as error:
                    st.error(f"Путь не создан по причине: {error_to_readable_view(error)}")
                else:
                    st.success("Путь создан")
