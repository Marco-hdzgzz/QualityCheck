import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)
from detalle_maquina import MAQUINAS


def vista_dashboard(page: ft.Page):
    page.title = "QualityCheck - Dashboard"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    aplicar_tema(page)

    header = crear_header()
    menu_mas = crear_menu_mas()

    maquinas = list(MAQUINAS.values())
    conteos = {
        "Operativas": sum(maquina["estado"] == "Operativa" for maquina in maquinas),
        "En revisión": sum(
            maquina["estado"] == "Mantenimiento" for maquina in maquinas
        ),
        "Fuera de servicio": sum(
            maquina["estado"] == "Fuera de servicio" for maquina in maquinas
        ),
    }
    conteos["Total"] = sum(conteos.values())

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
                                maquina["nombre"],
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=estilos.COLOR_TEXTO,
                            ),
                            ft.Text(
                                f"{maquina['codigo']} · {maquina['ubicacion']}",
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
                                maquina["proxima_inspeccion"],
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
            on_click=lambda _: page.go(f"/maquinas/{maquina['codigo']}"),
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
                        conteos["Operativas"],
                        "#16A34A",
                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                    ),
                    bloque_resumen(
                        "En revisión",
                        conteos["En revisión"],
                        "#D97706",
                        ft.Icons.BUILD_OUTLINED,
                    ),
                    bloque_resumen(
                        "Fuera de servicio",
                        conteos["Fuera de servicio"],
                        "#DC2626",
                        ft.Icons.ERROR_OUTLINE,
                    ),
                    bloque_resumen(
                        "Total",
                        conteos["Total"],
                        "#6B7280",
                        ft.Icons.DASHBOARD_OUTLINED,
                    ),
                ],
                height=100,
                spacing=8,
            ),
            ft.Container(height=8),
            ft.Text(
                "Próximas revisiones",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Column(
                [tarjeta_revision(maquina) for maquina in maquinas],
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
