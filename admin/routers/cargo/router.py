import streamlit as st
from routers.cargo.schemas import CargoBase
from routers.core_api import api


def cargo_tab_page(cargo_tab):
    """Логика вкладки грузов."""

    with cargo_tab:
        cargos = api.cargo.get_cargos()
        cargo_name_to_id = {cargo.name: cargo.id for cargo in cargos}
        cargos_inner_ids = (cargo.name for cargo in cargos)

        cargo_widget = st.multiselect(
            "Выбрать Груз",
            cargos_inner_ids,
            default=None,
            max_selections=1,
        )

        st.divider()

        if cargo_widget:
            cargo_id = cargo_name_to_id[cargo_widget[0]]
            cargo = api.cargo.get_cargo(cargo_id)

            cargo_id = st.text_input("ID", value=cargo.id, disabled=True, key="cargo_id")
            cargo_name = st.text_input("Имя", value=cargo.name, key="cargo_name")
            cargo_weight = st.number_input("Масса", value=cargo.weight, key="cargo_weight")

            col1, col2, _, _, _, _ = st.columns(6, gap="small")

            change_clicked = col1.button("Изменить", key="cargo_update_btn")
            if change_clicked:
                cargo_data = CargoBase(
                    name=cargo_name,
                    weight=cargo_weight,
                )
                try:
                    api.cargo.update_cargo(cargo_id, cargo_data)
                except Exception as error:
                    st.error(f"Груз не обновлен по причине: {error}")
                else:
                    st.success("Груз обновлен")

            delete_clicked = col2.button("Удалить", key="cargo_delete_btn")
            if delete_clicked:
                try:
                    api.cargo.delete_cargo(cargo_id)
                except Exception as error:
                    st.error(f"Груз не удален по причине: {error}")
                else:
                    st.success("Груз удален")

        else:
            cargo_name = st.text_input("Имя", key="cargo_name")
            cargo_weight = st.number_input("Масса", key="cargo_weight")
            cargo_data = CargoBase(
                name=cargo_name,
                weight=cargo_weight,
            )

            add_clicked = st.button("Добавить", key="cargo_create_btn")
            if add_clicked:
                try:
                    api.cargo.create_cargo(cargo_data)
                except Exception as error:
                    st.error(f"Груз не создан по причине: {error}")
                else:
                    st.success("Груз создан")
