import flet as ft

import estilos
from componentes import aplicar_tema, crear_header, crear_menu_mas, configurar_navbar
from maquinas_data import MAQUINAS
from revision_preventiva_service import RevisionPreventivaService


service = RevisionPreventivaService()


def vista_historial_revisiones(page: ft.Page):
    """Punto 22: consulta del historial de revisiones finalizadas/canceladas."""
    page.title = "QualityCheck - Historial de revisiones"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None
    aplicar_tema(page)

    header = crear_header()
    menu_mas = crear_menu_mas()
    lista = ft.ListView(expand=True, spacing=10)
    resumen = ft.Text("", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO)

    filtro_estado = ft.Dropdown(
        label="Estado",
        value="Todos",
        options=[
            ft.DropdownOption(key="Todos", text="Todos"),
            ft.DropdownOption(key="Completada", text="Completada"),
            ft.DropdownOption(key="Cancelada", text="Cancelada"),
        ],
        width=155,
        bgcolor="#FFFFFF",
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
    )
    filtro_maquina = ft.Dropdown(
        label="Máquina",
        value="Todas",
        options=[ft.DropdownOption(key="Todas", text="Todas")] + [
            ft.DropdownOption(key=codigo, text=f"{codigo} · {m['nombre']}")
            for codigo, m in MAQUINAS.items()
        ],
        expand=True,
        bgcolor="#FFFFFF",
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
    )

    def color_estado(estado):
        if estado == "Completada":
            return "#166534", "#DCFCE7"
        return "#6B7280", "#F3F4F6"

    def cerrar(dialogo):
        dialogo.open = False
        page.update()

    def ver_detalle(revision):
        maquina = MAQUINAS.get(revision.get("maquina_id"), {})
        campos = [
            f"ID: {revision.get('id', '')}",
            f"Máquina: {revision.get('maquina_id', '')} · {maquina.get('nombre', '')}",
            f"Estado: {revision.get('estado', '')}",
            f"Tipo: {revision.get('tipo_revision', '')}",
            f"Responsable: {revision.get('responsable_id', '')}",
            f"Fecha programada: {revision.get('fecha_programada', '')}",
            f"Fecha realizada: {revision.get('fecha_realizada') or '—'}",
            f"Resultado: {revision.get('resultado') or '—'}",
            f"Descripción: {revision.get('descripcion', '')}",
            f"Observaciones: {revision.get('observaciones') or '—'}",
            f"Acciones realizadas: {revision.get('acciones_realizadas') or '—'}",
            f"Próxima revisión: {revision.get('proxima_revision') or '—'}",
        ]
        dialogo = ft.AlertDialog(
            title=ft.Text("Registro histórico", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([ft.Text(x, size=12) for x in campos], spacing=7, scroll=ft.ScrollMode.AUTO),
                width=430,
                height=360,
            ),
            bgcolor=estilos.COLOR_FONDO,
        )
        dialogo.actions = [ft.TextButton(content=ft.Text("Cerrar"), on_click=lambda e: cerrar(dialogo))]
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def tarjeta(revision):
        maquina = MAQUINAS.get(revision.get("maquina_id"), {})
        texto, fondo = color_estado(revision.get("estado"))
        fecha = revision.get("fecha_realizada") or revision.get("updated_at", "")[:10]
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(f"{revision.get('maquina_id')} · {maquina.get('nombre', '')}", size=15, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                        ft.Text(revision.get("tipo_revision", ""), size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
                    ], spacing=2, expand=True),
                    ft.Container(
                        content=ft.Text(revision.get("estado", ""), size=11, weight=ft.FontWeight.BOLD, color=texto),
                        bgcolor=fondo, padding=6, border_radius=16,
                    ),
                ]),
                ft.Text(f"Fecha de cierre: {fecha or '—'}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                ft.Text(f"Resultado: {revision.get('resultado') or 'Sin resultado registrado'}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                ft.Row([
                    ft.TextButton(
                        content=ft.Row([ft.Icon(ft.Icons.VISIBILITY_OUTLINED, size=17), ft.Text("Ver registro")], tight=True),
                        on_click=lambda e: ver_detalle(revision),
                    )
                ], alignment=ft.MainAxisAlignment.END),
            ], spacing=7),
            bgcolor="#FFFFFF",
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"), bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"), right=ft.BorderSide(1, "#E1E3E6"),
            ),
            border_radius=12,
            padding=12,
        )

    def actualizar(e=None):
        registros = service.historial()
        if filtro_estado.value != "Todos":
            registros = [r for r in registros if r.get("estado") == filtro_estado.value]
        if filtro_maquina.value != "Todas":
            registros = [r for r in registros if r.get("maquina_id") == filtro_maquina.value]
        registros = sorted(registros, key=lambda r: r.get("updated_at", ""), reverse=True)
        lista.controls = [tarjeta(r) for r in registros]
        if not registros:
            lista.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.HISTORY, size=42, color="#9CA3AF"),
                        ft.Text("No hay revisiones en el historial", weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                        ft.Text("Las revisiones completadas o canceladas aparecerán aquí.", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=35,
                    alignment=ft.Alignment.CENTER,
                )
            ]
        resumen.value = f"{len(registros)} registro(s) histórico(s)"
        page.update()

    filtro_estado.on_change = actualizar
    filtro_maquina.on_change = actualizar

    cuerpo = ft.Column([
        ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Volver", on_click=lambda e: page.go("/revisiones")),
            ft.Column([
                ft.Text("Historial de revisiones", size=20, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                ft.Text("Consulta las revisiones preventivas completadas y canceladas.", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ], spacing=3, expand=True),
        ]),
        resumen,
        ft.Row([filtro_maquina, filtro_estado], spacing=10),
        lista,
    ], spacing=12, expand=True)

    contenido = ft.Stack([
        ft.Container(content=cuerpo, padding=20, expand=True),
        ft.Container(content=menu_mas, right=15, bottom=15),
    ], expand=True)

    configurar_navbar(page, menu_mas, indice_inicial=1)
    page.add(ft.Column([header, contenido], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, expand=True))
    actualizar()
