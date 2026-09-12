import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

MAQUINAS = {
    "MAQ-01": {
        "codigo": "MAQ-01",
        "nombre": "Torno 03",
        "marca": "Mazak",
        "modelo": "QUICK TURN 200",
        "ubicacion": "Planta 1",
        "estado": "Operativa",
        "proxima_inspeccion": "12 de Septiembre de 2026",
        "ultima_inspeccion": "12 de Agosto de 2026",
        "hallazgos_abiertos": "2",
    },
    "MAQ-02": {
        "codigo": "MAQ-02",
        "nombre": "Fresadora 01",
        "marca": "DMG Mori",
        "modelo": "CMX 600 V",
        "ubicacion": "Planta 2",
        "estado": "Operativa",
        "proxima_inspeccion": "18 de Septiembre de 2026",
        "ultima_inspeccion": "18 de Agosto de 2026",
        "hallazgos_abiertos": "0",
    },
    "MAQ-03": {
        "codigo": "MAQ-03",
        "nombre": "Prensa 02",
        "marca": "Haas",
        "modelo": "VF-2",
        "ubicacion": "Planta 1",
        "estado": "Mantenimiento",
        "proxima_inspeccion": "25 de Septiembre de 2026",
        "ultima_inspeccion": "25 de Agosto de 2026",
        "hallazgos_abiertos": "1",
    },
}


def vista_detalle_maquina(page: ft.Page, codigo_maquina: str):
    maquina = MAQUINAS.get(codigo_maquina, MAQUINAS["MAQ-01"])

    page.title = f"QualityCheck - {maquina['nombre']}"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    aplicar_tema(page)
    header = crear_header()
    menu_mas = crear_menu_mas()

    def volver(e):
        page.go("/maquinas")

    def mostrar_mensaje(mensaje):
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor=estilos.COLOR_TEXTO,
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def realizar_inspeccion(e):
        mostrar_mensaje(f"Nueva inspección iniciada para {maquina['nombre']}.")

    def programar_revision(e):
        mostrar_mensaje(f"Programación de revisión para {maquina['nombre']}.")

    estado_color = "#166534" if maquina["estado"] == "Operativa" else "#92400E"
    estado_fondo = "#DCFCE7" if maquina["estado"] == "Operativa" else "#FEF3C7"

    def resumen(titulo, valor, icono, color=estilos.COLOR_TEXTO):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icono, color=estilos.COLOR_PRINCIPAL, size=22),
                    ft.Text(
                        titulo,
                        size=11,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                    ft.Text(
                        valor,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=color,
                    ),
                ],
                spacing=5,
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
            expand=True,
        )

    def dato_general(etiqueta, valor):
        return ft.Row(
            [
                ft.Text(
                    etiqueta,
                    size=13,
                    color=estilos.COLOR_TEXTO_SECUNDARIO,
                    expand=True,
                ),
                ft.Text(
                    valor,
                    size=13,
                    color=estilos.COLOR_TEXTO,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.RIGHT,
                    expand=True,
                ),
            ],
            spacing=10,
        )

    resumen_estado = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=estado_color, size=22),
                ft.Column(
                    [
                        ft.Text(
                            "Estado actual",
                            size=11,
                            color=estilos.COLOR_TEXTO_SECUNDARIO,
                        ),
                        ft.Text(
                            maquina["estado"],
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=estado_color,
                        ),
                    ],
                    spacing=3,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=8,
        ),
        bgcolor=estado_fondo,
        border_radius=12,
        padding=12,
        expand=True,
    )

    cuerpo = ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        tooltip="Volver a máquinas",
                        on_click=volver,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                maquina["nombre"],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=estilos.COLOR_TEXTO,
                            ),
                            ft.Text(
                                maquina["codigo"],
                                size=13,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                ],
                spacing=4,
            ),
            ft.Text(
                "Resumen de estado",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Row(
                [
                    resumen_estado,
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.WARNING_AMBER_OUTLINED,
                                    color=estilos.COLOR_PRINCIPAL,
                                    size=22,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Hallazgos abiertos",
                                            size=11,
                                            color=estilos.COLOR_TEXTO_SECUNDARIO,
                                        ),
                                        ft.Text(
                                            maquina["hallazgos_abiertos"],
                                            size=14,
                                            weight=ft.FontWeight.BOLD,
                                            color=estilos.COLOR_TEXTO,
                                        ),
                                    ],
                                    spacing=3,
                                ),
                            ],
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor="#FFFFFF",
                        border_radius=12,
                        padding=12,
                        expand=True,
                    ),
                ],
                height=60,
                spacing=10,
            ),
            ft.Row(
                [
                    resumen(
                        "Próxima inspección",
                        maquina["proxima_inspeccion"],
                        ft.Icons.EVENT_OUTLINED,
                    ),
                    resumen(
                        "Última inspección",
                        maquina["ultima_inspeccion"],
                        ft.Icons.HISTORY,
                    ),
                ],
                spacing=10,
                height=120,
            ),
            ft.Container(height=8),
            ft.Text(
                "Datos generales",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Container(
                content=ft.Column(
                    [
                        dato_general("Código", maquina["codigo"]),
                        ft.Divider(height=1, color="#E1E3E6"),
                        dato_general("Nombre", maquina["nombre"]),
                        ft.Divider(height=1, color="#E1E3E6"),
                        dato_general("Marca", maquina["marca"]),
                        ft.Divider(height=1, color="#E1E3E6"),
                        dato_general("Modelo", maquina["modelo"]),
                        ft.Divider(height=1, color="#E1E3E6"),
                        dato_general("Ubicación", maquina["ubicacion"]),
                    ],
                    spacing=12,
                ),
                bgcolor="#FFFFFF",
                border=ft.Border(
                    top=ft.BorderSide(1, "#E1E3E6"),
                    bottom=ft.BorderSide(1, "#E1E3E6"),
                    left=ft.BorderSide(1, "#E1E3E6"),
                    right=ft.BorderSide(1, "#E1E3E6"),
                ),
                border_radius=12,
                padding=16,
            ),
            ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED),
                        ft.Text(
                            "Realizar nueva inspección",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor=estilos.COLOR_PRINCIPAL,
                color=estilos.COLOR_TEXTO,
                on_click=realizar_inspeccion,
            ),
            ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.EVENT_OUTLINED),
                        ft.Text(
                            "Programar revisión",
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                bgcolor="#FFFFFF",
                color=estilos.COLOR_TEXTO,
                on_click=programar_revision,
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    configurar_navbar(page, menu_mas, indice_inicial=1)

    contenido = ft.Stack(
        [
            ft.Container(content=cuerpo, padding=20, expand=True),
            ft.Container(content=menu_mas, right=15, bottom=15),
        ],
        expand=True,
    )

    page.add(
        ft.Column(
            [header, contenido],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
