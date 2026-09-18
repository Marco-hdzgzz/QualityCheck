import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from services import obtener_todas_las_maquinas

def vista_listado(page: ft.Page):
    page.title = "QualityCheck - Catálogo de Máquinas"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    # validar sesión de usuario activa
    usuario_id = page.session.store.get("usuario_id")
    if not usuario_id:
        page.go("/")
        return

    aplicar_tema(page)

    header = crear_header(titulo="Catálogo de Máquinas")
    menu_mas = crear_menu_mas(page)

    #consultar todas las máquinas en PostgreSQL (Supabase)
    with SessionLocal() as db:
        maquinas = obtener_todas_las_maquinas(db)

    def construir_tarjeta_maquina(maquina):
        # Asignación de color según el estado operativo de la máquina
        color_estado = "#16A34A" if maquina.estado == "Operativa" else ("#D97706" if maquina.estado == "En revisión" else "#DC2626")

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                maquina.nombre,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=estilos.COLOR_TEXTO,
                            ),
                            ft.Text(
                                f"Código: {maquina.codigo_maquina} · Tipo: {maquina.tipo or 'N/A'}",
                                size=11,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                            ft.Text(
                                f"Ubicación: {maquina.ubicacion or maquina.area or 'Sin asignar'}",
                                size=11,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text(
                                    maquina.estado or "N/A",
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color="#FFFFFF",
                                ),
                                bgcolor=color_estado,
                                padding=8,
                                border_radius=6,
                            ),
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT,
                                color=estilos.COLOR_TEXTO_SECUNDARIO,
                                size=20,
                            ),
                        ],
                        spacing=4,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
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
            padding=14,
            # Navegar al detalle pasando el código único de la máquina
            on_click=lambda _: page.go(f"/maquinas/{maquina.codigo_maquina}"),
        )

    #botón flotante superior para agregar nueva máquina
    btn_agregar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ADD, color="#25252B", size=18),
                ft.Text("REGISTRAR MÁQUINA", color="#25252B", weight=ft.FontWeight.BOLD, size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        bgcolor="#F5A000",
        height=42,
        on_click=lambda _: page.go("/maquinas/agregar"),
    )

    # Contenedor principal scrollable
    cuerpo = ft.Column(
        [
            btn_agregar,
            ft.Container(height=6),
            ft.Text(
                f"Equipos Registrados ({len(maquinas)})",
                size=15,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Column(
                [construir_tarjeta_maquina(m) for m in maquinas]
                if maquinas
                else [
                    ft.Text(
                        "No hay máquinas registradas en la base de datos.",
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    )
                ],
                spacing=10,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cont = ft.Container(content=cuerpo, padding=16, expand=True)

    contenido = ft.Stack(
        [
            cont,
            ft.Container(content=menu_mas, right=15, bottom=15),
        ],
        expand=True,
    )

    configurar_navbar(page, menu_mas, indice_inicial=1)

    page.add(
        ft.Column(
            [header, contenido],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )
