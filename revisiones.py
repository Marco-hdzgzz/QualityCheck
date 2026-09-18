import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from services import obtener_historial_revisiones

def vista_revisiones(page: ft.Page):
    page.title = "QualityCheck - Revisiones Técnicas"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    # recuperar credenciales de sesión activa
    usuario_id = page.session.store.get("usuario_id")
    usuario_nombre = page.session.store.get("usuario_nombre")

    if not usuario_id:
        page.go("/")
        return

    aplicar_tema(page)

    header = crear_header(titulo="Revisiones Técnicas")
    menu_mas = crear_menu_mas(page)

    # consultar las revisiones guardadas en PostgreSQL
    with SessionLocal() as db:
        lista_revisiones = obtener_historial_revisiones(db)

    def tarjeta_inspeccion(inspeccion):
        # Asignar color dinámico según el resultado
        color_resultado = "#16A34A" if inspeccion.resultado_final == "Aprobado" else "#DC2626"

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                f"Código: {inspeccion.codigo_inspeccion}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=estilos.COLOR_TEXTO,
                            ),
                            ft.Text(
                                f"Tipo: {inspeccion.tipo_inspeccion} · Fecha: {inspeccion.fecha_inspeccion.strftime('%d/%m/%Y')}",
                                size=11,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                            ft.Text(
                                f"Observaciones: {inspeccion.observaciones_generales or 'Sin observaciones'}",
                                size=11,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                                italic=True,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Text(
                            inspeccion.resultado_final or "Pendiente",
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        ),
                        bgcolor=color_resultado,
                        padding=8,
                        border_radius=6,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
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
        )

    # Construcción de la vista principal
    cuerpo = ft.Column(
        [
            ft.Text(
                "Historial General de Revisiones",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Column(
                [tarjeta_inspeccion(i) for i in lista_revisiones]
                if lista_revisiones
                else [
                    ft.Text(
                        "No se encontraron revisiones registradas.",
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    )
                ],
                spacing=8,
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cont = ft.Container(content=cuerpo, padding=20, expand=True)

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
        indice_inicial=2,  # Destaca el ícono de revisiones en la barra
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
