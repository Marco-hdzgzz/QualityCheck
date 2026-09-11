import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)


def vista_dashboard(page: ft.Page):
    page.title = "QualityCheck - Dashboard"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    aplicar_tema(page)

    header = crear_header()
    menu_mas = crear_menu_mas()

    cont = ft.Container(
        content=ft.Text(
            "ola",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=estilos.COLOR_TEXTO,
        ),
        padding=20,
        expand=True,
    )

    contenido = ft.Stack(
        [
            cont,
            ft.Container(
                content=menu_mas,
                right=15,
                bottom=15,
            ),
        ],
        expand=True,
    )

    configurar_navbar(
        page,
        menu_mas,
        indice_inicial=0,
    )

    page.add(
        ft.Column(
            [
                header,
                contenido,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
