import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from services import obtener_todas_las_maquinas, obtener_resumen_dashboard

def vista_dashboard(page: ft.Page):
    page.title = "QualityCheck - Dashboard"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    usuario_id = page.session.store.get("usuario_id")
    usuario_nombre = page.session.store.get("usuario_nombre")

    if not usuario_id:
        page.go("/")
        return

    aplicar_tema(page)

    header = crear_header()

    menu_mas = crear_menu_mas(page)

    #se obtiene la sesion de postgresql
    with SessionLocal() as db:
        m_resumen =obtener_resumen_dashboard(db)
        lista_maquinas = obtener_todas_las_maquinas(db)

    def bloque_resumen(titulo, cantidad, color, icono):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, color=color, size=22),
                    ft.Text(
                        str(cantidad),
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=estilos.COLOR_TEXTO,
                    ),
                    ft.Text(
                        titulo,
                        size=10,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"),
                bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"),
                right=ft.BorderSide(1, "#E1E3E6"),
            ),
            border_radius=12,
            padding=10,
            expand=True,
        )

    def tarjeta_revision(maquina):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                maquina.nombre,
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=estilos.COLOR_TEXTO,
                            ),
                            ft.Text(
                                f"{maquina.codigo_maquina} · {maquina.ubicacion or maquina.area}",
                                size=11,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.EVENT_OUTLINED,
                                color=estilos.COLOR_PRINCIPAL,
                                size=20,
                            ),
                            ft.Text(
                                "Pendiente",
                                size=11,
                                color=estilos.COLOR_TEXTO,
                                text_align=ft.TextAlign.RIGHT,
                            ),
                        ],
                        spacing=3,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#FFFFFF",
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"),
                bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"),
                right=ft.BorderSide(1, "#E1E3E6"),
            ),
            border_radius=12,
            padding=12,
            on_click=lambda _: page.go(f"/maquinas/{maquina.codigo_maquina}"),
        )

    resumen = ft.Column(
        [
            ft.Text(
                "Resumen general",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Row(
                [
                    bloque_resumen(
                        "Operativas",
                        m_resumen["operativas"],
                        "#16A34A",
                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                    ),
                    bloque_resumen(
                        "En revisión",
                        m_resumen["en_revision"],
                        "#D97706",
                        ft.Icons.BUILD_OUTLINED,
                    ),
                    bloque_resumen(
                        "Fuera de servicio",
                        m_resumen["fuera_de_servicio"],
                        "#DC2626",
                        ft.Icons.ERROR_OUTLINE,
                    ),
                    bloque_resumen(
                        "Total",
                        m_resumen["total"],
                        "#6B7280",
                        ft.Icons.DASHBOARD_OUTLINED,
                    ),
                ],
                height=100,
                spacing=8,
            ),
            ft.Container(height=8),
            ft.Row([
                ft.Text(
                    "Próximas revisiones",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=estilos.COLOR_TEXTO,
                    expand=True,
                ),
                ft.TextButton(
                    content=ft.Text("Gestionar revisiones", color=estilos.COLOR_TEXTO),
                    on_click=lambda e: page.go("/revisiones"),
                ),
            ]),
            ft.Column(
                [tarjeta_revision(m) for m in lista_maquinas],
                spacing=8,
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cont = ft.Container(
        content=resumen,
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
        
