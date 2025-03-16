import streamlit as st
from routers.core_api import solve_api
from routers.path.utils import get_cities_names, get_city_id_by_name
from routers.task.schemas import CargoWithCount, Task
from routers.task.utils import get_cargo_id_by_name, get_cargos_names


def create_city_select_box(label: str, key: str, disabled: bool, current_value=None):
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


def task_tab_page(path_tab):
    """Логика вкладки решения задачи."""

    with path_tab:
        path_city_from = create_city_select_box(
            label="Город отправления",
            key="city_from_name_task",
            disabled=False,
        )
        path_city_to = create_city_select_box(
            label="Город прибытия",
            key="city_to_name_task",
            disabled=False,
        )
        selected_cargos = st.multiselect(
            "Выбрать грузы",
            get_cargos_names(),
            default=None,
        )

        if selected_cargos:
            cargos_count = {}
            for selected_cargo in selected_cargos:
                cargo_count = st.number_input(
                    f"Количество {selected_cargo}",
                    value=1,
                    step=1,
                    key=f"{selected_cargo}_count",
                )
                cargos_count[selected_cargo] = cargo_count

            if all(
                widget is not None
                for widget in [
                    path_city_from,
                    path_city_to,
                ]
            ):
                solve_clicked = st.button("Построить маршрут", key="task_solve_btn")
            else:
                solve_clicked = st.button("Построить маршрут", key="task_solve_btn", disabled=True)

            if solve_clicked:
                task = Task(
                    city_from_id=get_city_id_by_name(path_city_from),
                    city_to_id=get_city_id_by_name(path_city_to),
                    cargos=[
                        CargoWithCount(cargo_id=get_cargo_id_by_name(cargo_name), cargo_count=count)
                        for cargo_name, count in cargos_count.items()
                    ],
                )
                solve_api.task.solve(task=task)
