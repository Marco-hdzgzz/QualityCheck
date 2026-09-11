import flet as ft
import estilos


def aplicar_tema(page):
    page.theme = ft.Theme(
        navigation_bar_theme=ft.NavigationBarTheme(
            label_text_style={
                ft.ControlState.DEFAULT: ft.TextStyle(
                    color="#6B7280",
                    size=11,
                ),
                ft.ControlState.SELECTED: ft.TextStyle(
                    color="#F5A000",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                ),
            },
            indicator_color="#FFD67A",
            bgcolor="#FFFFFF",
            height=72,
        )
    )


def crear_header():
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Image(
                        src="logo.png",
                        width=44,
                        height=44,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    width=44,
                    height=44,
                    bgcolor="#FFFFFF",
                    border_radius=22,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(
                            "QualityCheck",
                            color="#25252B",
                            weight=ft.FontWeight.BOLD,
                            size=20,
                        ),
                        ft.Text(
                            "SISTEMA DE INSPECCIÓN INDUSTRIAL",
                            color="#25252B",
                            size=9,
                        ),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=10,
        ),
        bgcolor=estilos.COLOR_PRINCIPAL,
        padding=15,
    )


def crear_menu_mas():
    return ft.Container(
        content=ft.Column(
            [
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.WARNING_AMBER_OUTLINED,
                        color="#4B5563",
                    ),
                    title=ft.Text("Hallazgos", color="#374151"),
                ),
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.PERSON_OUTLINE,
                        color="#4B5563",
                    ),
                    title=ft.Text("Perfil", color="#374151"),
                ),
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.SETTINGS_OUTLINED,
                        color="#4B5563",
                    ),
                    title=ft.Text("Configuración", color="#374151"),
                ),
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.LOGOUT,
                        color="#B91C1C",
                    ),
                    title=ft.Text("Cerrar sesión", color="#B91C1C"),
                ),
            ],
            tight=True,
        ),
        width=220,
        bgcolor="#FFFFFF",
        padding=10,
        border_radius=15,
        visible=False,
    )


def crear_destinos_navbar(pequeno=False):
    destinos = [
        ft.NavigationBarDestination(
            icon=ft.Icons.HOME_OUTLINED,
            selected_icon=ft.Icon(
                ft.Icons.HOME,
                color=estilos.COLOR_TEXTO,
            ),
            label="Inicio",
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(
                ft.Icons.SETTINGS,
                color=estilos.COLOR_TEXTO,
            ),
            label="Máquinas",
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.ASSIGNMENT_OUTLINED,
            selected_icon=ft.Icon(
                ft.Icons.ASSIGNMENT,
                color=estilos.COLOR_TEXTO,
            ),
            label="Inspecciones",
        ),
    ]

    if not pequeno:
        destinos.append(
            ft.NavigationBarDestination(
                icon=ft.Icons.WARNING_AMBER_OUTLINED,
                selected_icon=ft.Icon(
                    ft.Icons.WARNING_AMBER,
                    color=estilos.COLOR_TEXTO,
                ),
                label="Hallazgos",
            )
        )

    destinos.append(
        ft.NavigationBarDestination(
            icon=ft.Icons.MENU,
            selected_icon=ft.Icon(
                ft.Icons.MENU,
                color=estilos.COLOR_TEXTO,
            ),
            label="Más",
        )
    )

    return destinos


def configurar_navbar(page, menu_mas, indice_inicial=0):
    navbar_pequeno = crear_destinos_navbar(pequeno=True)
    navbar_completo = crear_destinos_navbar(pequeno=False)

    indice_actual = indice_inicial

    rutas = {
        0: "/dashboard",
        1: "/maquinas",
        2: "/inspecciones",
        3: "/hallazgos",
    }

    def cambiar_seccion(e):
        nonlocal indice_actual

        indice = e.control.selected_index
        indice_mas = 3 if page.width < 350 else 4

        if indice == indice_mas:
            menu_mas.visible = not menu_mas.visible
            barra.selected_index = indice_actual

            if page.floating_action_button:
                page.floating_action_button.visible = not menu_mas.visible

            page.update()
            return

        menu_mas.visible = False
        indice_actual = indice

        if page.floating_action_button:
            page.floating_action_button.visible = True

        ruta = rutas.get(indice)

        if ruta and ruta != page.route:
            page.go(ruta)
        else:
            page.update()

    def ajustar_tamano(e=None):
        nonlocal indice_actual

        if page.width < 350:
            barra.destinations = navbar_pequeno
            menu_mas.content.controls[0].visible = True

            if indice_actual == 3:
                indice_actual = 2

            barra.selected_index = indice_actual
        else:
            barra.destinations = navbar_completo
            menu_mas.content.controls[0].visible = False
            barra.selected_index = indice_actual

        menu_mas.visible = False

        if page.floating_action_button:
            page.floating_action_button.visible = True

        page.update()

    barra = ft.NavigationBar(
        destinations=navbar_completo,
        on_change=cambiar_seccion,
        selected_index=indice_inicial,
        bgcolor="#FFFFFF",
        indicator_color=estilos.COLOR_PRINCIPAL,
    )

    page.navigation_bar = barra
    page.on_resize = ajustar_tamano

    ajustar_tamano()

    return barra
