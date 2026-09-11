import flet as ft
import estilos
from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)


def vista_listado(page: ft.Page):
    # Página
    page.title = "QualityCheck - Máquinas"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO

    page.window.width = 380
    page.window.height = 700
    page.window.resizable = True

    aplicar_tema(page)

    # Datos
    datos_maquina = {
        "codigo": "MAQ-01",
        "nombre": "Torno 03",
        "marca": "Mazak",
        "modelo": "QUICK TURN 200",
        "ubicacion": "Planta 1",
        "estado": "Operativa",
        "proximarev": "Prox. rev: 12 de Septiembre",
    }

    # Tarjeta
    def registro(maquina):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        maquina["codigo"],
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=estilos.COLOR_TEXTO,
                                    ),
                                    ft.Text(
                                        maquina["nombre"],
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=estilos.COLOR_TEXTO,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.IconButton(
                                icon=ft.CupertinoIcons.SQUARE_PENCIL,
                                tooltip="Editar máquina",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                maquina["marca"],
                                size=12,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                            ft.Text(
                                maquina["modelo"],
                                size=12,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                            ft.Text(
                                maquina["ubicacion"],
                                size=12,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    maquina["estado"],
                                    size=12,
                                    color="#166534",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                bgcolor="#DCFCE7",
                                padding=5,
                                border_radius=20,
                            ),
                            ft.Text(
                                maquina["proximarev"],
                                size=12,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                        ]
                    ),
                ],
                tight=True,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"),
                bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"),
                right=ft.BorderSide(1, "#E1E3E6"),
            ),
            border_radius=20,
            padding=14,
            expand=True,
        )

    def seleccionar_filtro(e):
        page.update()

    # Componentes compartidos
    header = crear_header()
    menu_mas = crear_menu_mas()

    txt_titulo = ft.Text(
        "Máquinas",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=estilos.COLOR_TEXTO,
    )

    txt_cantidad = ft.Text(
        "4 equipos registrados",
        size=14,
        color=estilos.COLOR_TEXTO_SECUNDARIO,
    )

    # Buscador
    buscar = ft.Container(
        content=ft.Row(
            [
                ft.TextField(
                    hint_text="Buscar máquina por nombre, marca o modelo",
                    hint_style=ft.TextStyle(
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                    border_radius=10,
                    border_color=estilos.COLOR_TEXTO_SECUNDARIO,
                    focused_border_color=estilos.COLOR_PRINCIPAL,
                    bgcolor="#FFFFFF",
                    color=estilos.COLOR_TEXTO,
                    expand=True,
                ),
                ft.Icon(
                    ft.Icons.SEARCH,
                    size=20,
                    color=estilos.COLOR_TEXTO_SECUNDARIO,
                ),
            ],
            expand=True,
        )
    )

    filtros = ft.Row(
        [
            ft.Chip(
                label=ft.Text("Todas", color=estilos.COLOR_TEXTO),
                autofocus=True,
                selected_color=estilos.COLOR_PRINCIPAL,
                bgcolor="#FFFFFF",
                on_select=seleccionar_filtro,
            ),
            ft.Chip(
                label=ft.Text("Operativas", color=estilos.COLOR_TEXTO),
                selected_color=estilos.COLOR_PRINCIPAL,
                bgcolor="#FFFFFF",
                on_select=seleccionar_filtro,
            ),
            ft.Chip(
                label=ft.Text("Mantenimiento", color=estilos.COLOR_TEXTO),
                selected_color=estilos.COLOR_PRINCIPAL,
                bgcolor="#FFFFFF",
                on_select=seleccionar_filtro,
            ),
            ft.Chip(
                label=ft.Text("Fuera de servicio", color=estilos.COLOR_TEXTO),
                selected_color=estilos.COLOR_PRINCIPAL,
                bgcolor="#FFFFFF",
                on_select=seleccionar_filtro,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    lista_maquinas = ft.ListView(
        controls=[
            registro(datos_maquina),
            registro(datos_maquina),
            registro(datos_maquina),
        ],
        expand=True,
        spacing=10,
    )

    # Agregar máquina
    page.floating_action_button = ft.FloatingActionButton(
        ft.Row(
            [
                ft.Icon(
                    ft.Icons.ADD,
                    color=estilos.COLOR_TEXTO,
                    size=18,
                ),
                ft.Text(
                    "Agregar Máquina",
                    size=15,
                    color=estilos.COLOR_TEXTO,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            tight=True,
            spacing=6,
        ),
        bgcolor=estilos.COLOR_PRINCIPAL,
        width=160,
        on_click=lambda _: print("Agregar Máquina"),
    )

    page.floating_action_button_location = ft.FloatingActionButtonLocation.END_FLOAT

    configurar_navbar(
        page,
        menu_mas,
        indice_inicial=1,
    )

    # Contenido
    columna = ft.Column(
        controls=[
            txt_titulo,
            txt_cantidad,
            buscar,
            ft.Container(height=10),
            filtros,
            ft.Container(height=10),
            lista_maquinas,
        ],
        spacing=4,
        expand=True,
    )

    cuerpo = ft.Container(
        content=ft.Column(
            controls=[
                columna,
                ft.Container(height=10),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        padding=20,
        expand=True,
    )

    contenido = ft.Stack(
        [
            cuerpo,
            ft.Container(
                content=menu_mas,
                right=15,
                bottom=15,
            ),
        ],
        expand=True,
    )

    page.add(
        ft.Column(
            controls=[
                header,
                contenido,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
