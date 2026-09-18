import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from models import Maquina, Inspeccion
from services import obtener_historial_revisiones

def vista_detalle_maquina(page: ft.Page, codigo_maquina: str):
    page.title = f"QualityCheck - Detalle {codigo_maquina}"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    #Validar sesión activa
    usuario_id = page.session.store.get("usuario_id")
    if not usuario_id:
        page.go("/")
        return

    aplicar_tema(page)

    #Consultar la máquina y sus inspecciones en Supabase
    with SessionLocal() as db:
        maquina = db.query(Maquina).filter(Maquina.codigo_maquina == codigo_maquina, Maquina.activa == True).first()

        if not maquina:
            page.add(ft.Text("Máquina no encontrada", color="#DC2626"))
            return

        historial = obtener_historial_revisiones(db, maquina.id_maquina)

    header = crear_header(titulo=f"Detalle: {maquina.codigo_maquina}")
    menu_mas = crear_menu_mas(page)

    #Color del Badge de Estado
    color_estado = "#16A34A" if maquina.estado == "Operativa" else ("#D97706" if maquina.estado == "En revisión" else "#DC2626")

    # componentes Visuales
    tarjeta_info = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(maquina.nombre, size=18, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO, expand=True),
                        ft.Container(
                            content=ft.Text(maquina.estado or "Desconocido", color="#FFFFFF", size=11, weight=ft.FontWeight.BOLD),
                            bgcolor=color_estado,
                            padding=8,
                            border_radius=6,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#E1E3E6"),
                ft.Text(f"Tipo: {maquina.tipo or 'N/A'}", size=12, color=estilos.COLOR_TEXTO),
                ft.Text(f"Marca / Modelo: {maquina.marca or 'N/A'} - {maquina.modelo or 'N/A'}", size=12, color=estilos.COLOR_TEXTO),
                ft.Text(f"Número de Serie: {maquina.numero_serie or 'N/A'}", size=12, color=estilos.COLOR_TEXTO),
                ft.Text(f"Ubicación / Área: {maquina.ubicacion or 'N/A'} ({maquina.area or 'General'})", size=12, color=estilos.COLOR_TEXTO),
            ],
            spacing=8,
        ),
        bgcolor="#FFFFFF",
        padding=16,
        border_radius=12,
        border=ft.Border(
            top=ft.BorderSide(1, "#E1E3E6"),
            bottom=ft.BorderSide(1, "#E1E3E6"),
            left=ft.BorderSide(1, "#E1E3E6"),
            right=ft.BorderSide(1, "#E1E3E6"),
        ),
    )

    def fila_historial(inspeccion):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(f"Inspección #{inspeccion.codigo_inspeccion}", size=13, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                            ft.Text(f"Fecha: {inspeccion.fecha_inspeccion.strftime('%d/%m/%Y')}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                        ],
                        spacing=2,
                    ),
                    ft.Text(
                        inspeccion.resultado_final or "Pendiente",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color="#16A34A" if inspeccion.resultado_final == "Aprobado" else "#DC2626"
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#FFFFFF",
            padding=10,
            border_radius=8,
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"),
                bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"),
                right=ft.BorderSide(1, "#E1E3E6"),
            ),
        )

    btn_nueva_revision = ft.ElevatedButton(
        content=ft.Text("NUEVA INSPECCIÓN", color="#25252B", weight=ft.FontWeight.BOLD),
        bgcolor="#F5A000",
        width=320,
        height=44,
        on_click=lambda _: page.go(f"/revisiones/maquina/{maquina.codigo_maquina}"),
    )

    cuerpo = ft.Column(
        [
            tarjeta_info,
            ft.Container(height=10),
            btn_nueva_revision,
            ft.Container(height=10),
            ft.Text("Historial de Revisiones", size=15, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            ft.Column(
                [fila_historial(h) for h in historial] if historial else [ft.Text("Sin revisiones registradas", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO)],
                spacing=6,
            ),
        ],
        spacing=6,
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
