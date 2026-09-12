import flet as ft

import estilos
from componentes import aplicar_tema, crear_header, crear_menu_mas, configurar_navbar
from detalle_maquina import MAQUINAS
from revision_preventiva_service import RevisionPreventivaService, TIPOS_REVISION


service = RevisionPreventivaService()


def vista_revisiones_preventivas(page: ft.Page, maquina_inicial: str | None = None):
    page.title = "QualityCheck - Revisiones preventivas"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None
    aplicar_tema(page)

    header = crear_header()
    menu_mas = crear_menu_mas()

    lista = ft.ListView(expand=True, spacing=10)
    txt_resumen = ft.Text("", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO)
    filtro_estado = ft.Dropdown(
        label="Estado",
        value="Todos",
        options=[ft.DropdownOption(key=x, text=x) for x in [
            "Todos", "Programada", "Pendiente", "En proceso", "Vencida", "Completada", "Cancelada"
        ]],
        width=150,
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

    def mensaje(texto):
        snack = ft.SnackBar(content=ft.Text(texto, color="#FFFFFF"), bgcolor=estilos.COLOR_TEXTO)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def color_estado(estado):
        return {
            "Completada": ("#166534", "#DCFCE7"),
            "Vencida": ("#991B1B", "#FEE2E2"),
            "Cancelada": ("#6B7280", "#F3F4F6"),
            "En proceso": ("#1D4ED8", "#DBEAFE"),
        }.get(estado, ("#92400E", "#FEF3C7"))

    def cerrar_dialogo(dialogo):
        dialogo.open = False
        page.update()

    def abrir_formulario(revision=None, maquina_prefijada=None):
        maquina = ft.Dropdown(
            label="Máquina *",
            value=(revision or {}).get("maquina_id") or maquina_prefijada or next(iter(MAQUINAS)),
            options=[ft.DropdownOption(key=c, text=f"{c} · {m['nombre']}") for c, m in MAQUINAS.items()],
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        responsable = ft.TextField(
            label="Responsable *",
            value=(revision or {}).get("responsable_id", "maria.lopez"),
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        tipo = ft.Dropdown(
            label="Tipo de revisión *",
            value=(revision or {}).get("tipo_revision") or TIPOS_REVISION[0],
            options=[ft.DropdownOption(key=t, text=t) for t in TIPOS_REVISION],
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        descripcion = ft.TextField(
            label="Descripción *",
            value=(revision or {}).get("descripcion", ""),
            multiline=True,
            min_lines=2,
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        fecha_programada = ft.TextField(
            label="Fecha programada *",
            hint_text="AAAA-MM-DD",
            value=(revision or {}).get("fecha_programada", ""),
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        observaciones = ft.TextField(
            label="Observaciones",
            value=(revision or {}).get("observaciones", ""),
            multiline=True,
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )
        proxima = ft.TextField(
            label="Próxima revisión",
            hint_text="AAAA-MM-DD",
            value=(revision or {}).get("proxima_revision") or "",
            bgcolor="#FFFFFF",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
        )

        titulo = "Editar revisión preventiva" if revision else "Nueva revisión preventiva"
        dialogo = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            content=ft.Container(
                content=ft.Column(
                    [maquina, responsable, tipo, descripcion, fecha_programada, observaciones, proxima],
                    tight=True,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=430,
                height=460,
            ),
            bgcolor=estilos.COLOR_FONDO,
        )

        def guardar(e):
            datos = dict(
                maquina_id=maquina.value,
                responsable_id=responsable.value,
                tipo_revision=tipo.value,
                descripcion=descripcion.value,
                fecha_programada=fecha_programada.value,
                observaciones=observaciones.value,
                proxima_revision=proxima.value or None,
            )
            try:
                if revision:
                    service.actualizar(revision["id"], **datos)
                    texto = "Revisión actualizada correctamente."
                else:
                    service.crear(**datos)
                    texto = "Revisión programada correctamente."
                cerrar_dialogo(dialogo)
                actualizar_lista()
                mensaje(texto)
            except ValueError as exc:
                mensaje(str(exc))

        dialogo.actions = [
            ft.TextButton(content=ft.Text("Cancelar", color=estilos.COLOR_TEXTO), on_click=lambda e: cerrar_dialogo(dialogo)),
            ft.Button(content=ft.Text("Guardar", color=estilos.COLOR_TEXTO, weight=ft.FontWeight.BOLD), bgcolor=estilos.COLOR_PRINCIPAL, on_click=guardar),
        ]
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def abrir_detalle(revision):
        maquina = MAQUINAS.get(revision["maquina_id"], {})
        contenido = [
            ft.Text(f"{revision['id']} · {revision['estado']}", weight=ft.FontWeight.BOLD),
            ft.Text(f"Máquina: {revision['maquina_id']} · {maquina.get('nombre', '')}"),
            ft.Text(f"Tipo: {revision['tipo_revision']}"),
            ft.Text(f"Fecha programada: {revision['fecha_programada']}"),
            ft.Text(f"Responsable: {revision['responsable_id']}"),
            ft.Text(f"Descripción: {revision['descripcion']}"),
        ]
        if revision.get("fecha_realizada"):
            contenido.append(ft.Text(f"Fecha realizada: {revision['fecha_realizada']}"))
        if revision.get("resultado"):
            contenido.append(ft.Text(f"Resultado: {revision['resultado']}"))
        if revision.get("observaciones"):
            contenido.append(ft.Text(f"Observaciones: {revision['observaciones']}"))
        if revision.get("acciones_realizadas"):
            contenido.append(ft.Text(f"Acciones: {revision['acciones_realizadas']}"))
        if revision.get("proxima_revision"):
            contenido.append(ft.Text(f"Próxima revisión: {revision['proxima_revision']}"))
        dialogo = ft.AlertDialog(
            title=ft.Text("Detalle de revisión", weight=ft.FontWeight.BOLD),
            content=ft.Column(contenido, tight=True, spacing=8, scroll=ft.ScrollMode.AUTO),
            bgcolor=estilos.COLOR_FONDO,
        )
        dialogo.actions = [ft.TextButton(content=ft.Text("Cerrar"), on_click=lambda e: cerrar_dialogo(dialogo))]
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def abrir_completar(revision):
        resultado = ft.Dropdown(
            label="Resultado *",
            options=[
                ft.DropdownOption(key="Aprobada", text="Aprobada"),
                ft.DropdownOption(key="Requiere atención", text="Requiere atención"),
                ft.DropdownOption(key="No aprobada", text="No aprobada"),
            ],
            bgcolor="#FFFFFF",
        )
        observaciones = ft.TextField(label="Observaciones", multiline=True, bgcolor="#FFFFFF")
        acciones = ft.TextField(label="Acciones realizadas", multiline=True, bgcolor="#FFFFFF")
        proxima = ft.TextField(label="Próxima revisión", hint_text="AAAA-MM-DD", bgcolor="#FFFFFF")
        dialogo = ft.AlertDialog(
            title=ft.Text("Completar revisión", weight=ft.FontWeight.BOLD),
            content=ft.Column([resultado, observaciones, acciones, proxima], tight=True, spacing=10),
            bgcolor=estilos.COLOR_FONDO,
        )

        def completar(e):
            try:
                service.completar(
                    revision["id"],
                    resultado=resultado.value or "",
                    observaciones=observaciones.value or "",
                    acciones_realizadas=acciones.value or "",
                    proxima_revision=proxima.value or None,
                )
                cerrar_dialogo(dialogo)
                actualizar_lista()
                mensaje("Revisión completada correctamente.")
            except ValueError as exc:
                mensaje(str(exc))

        dialogo.actions = [
            ft.TextButton(content=ft.Text("Cancelar"), on_click=lambda e: cerrar_dialogo(dialogo)),
            ft.Button(content=ft.Text("Completar", color=estilos.COLOR_TEXTO, weight=ft.FontWeight.BOLD), bgcolor=estilos.COLOR_PRINCIPAL, on_click=completar),
        ]
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def cancelar_revision(revision):
        try:
            service.cancelar(revision["id"])
            actualizar_lista()
            mensaje("Revisión cancelada.")
        except ValueError as exc:
            mensaje(str(exc))

    def eliminar_revision(revision):
        try:
            service.eliminar(revision["id"])
            actualizar_lista()
            mensaje("Revisión eliminada.")
        except ValueError as exc:
            mensaje(str(exc))

    def tarjeta(revision):
        maquina = MAQUINAS.get(revision["maquina_id"], {})
        texto_color, fondo_color = color_estado(revision["estado"])
        acciones = [
            ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, tooltip="Ver", on_click=lambda e: abrir_detalle(revision)),
        ]
        if revision["estado"] not in {"Completada", "Cancelada"}:
            acciones.extend([
                ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, tooltip="Editar", on_click=lambda e: abrir_formulario(revision=revision)),
                ft.IconButton(icon=ft.Icons.CHECK_CIRCLE_OUTLINE, tooltip="Completar", on_click=lambda e: abrir_completar(revision)),
                ft.IconButton(icon=ft.Icons.CANCEL_OUTLINED, tooltip="Cancelar", on_click=lambda e: cancelar_revision(revision)),
            ])
        if revision["estado"] in {"Programada", "Pendiente", "Cancelada"}:
            acciones.append(ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, tooltip="Eliminar", on_click=lambda e: eliminar_revision(revision)))

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(f"{revision['maquina_id']} · {maquina.get('nombre', '')}", size=15, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                        ft.Text(revision["tipo_revision"], size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
                    ], spacing=2, expand=True),
                    ft.Container(content=ft.Text(revision["estado"], size=11, weight=ft.FontWeight.BOLD, color=texto_color), bgcolor=fondo_color, padding=6, border_radius=16),
                ]),
                ft.Row([
                    ft.Text(f"Programada: {revision['fecha_programada']}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                    ft.Text(f"Responsable: {revision['responsable_id']}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row(acciones, alignment=ft.MainAxisAlignment.END, spacing=0),
            ], spacing=8),
            bgcolor="#FFFFFF",
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"), bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"), right=ft.BorderSide(1, "#E1E3E6")
            ),
            border_radius=12,
            padding=12,
        )

    def actualizar_lista(e=None):
        registros = service.listar()
        if filtro_estado.value and filtro_estado.value != "Todos":
            registros = [r for r in registros if r["estado"] == filtro_estado.value]
        if filtro_maquina.value and filtro_maquina.value != "Todas":
            registros = [r for r in registros if r["maquina_id"] == filtro_maquina.value]
        lista.controls = [tarjeta(r) for r in registros]
        txt_resumen.value = f"{len(registros)} revisión(es) · {len(service.vencidas())} vencida(s)"
        page.update()

    filtro_estado.on_change = actualizar_lista
    filtro_maquina.on_change = actualizar_lista

    btn_nueva = ft.Button(
        content=ft.Row([ft.Icon(ft.Icons.ADD), ft.Text("Nueva revisión", weight=ft.FontWeight.BOLD)], tight=True),
        bgcolor=estilos.COLOR_PRINCIPAL,
        color=estilos.COLOR_TEXTO,
        on_click=lambda e: abrir_formulario(maquina_prefijada=maquina_inicial),
    )

    cuerpo = ft.Column([
        ft.Row([
            ft.Column([
                ft.Text("Revisiones preventivas", size=20, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                ft.Text("Programa, controla y consulta el mantenimiento preventivo de la maquinaria.", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ], spacing=3, expand=True),
            btn_nueva,
        ]),
        txt_resumen,
        ft.Row([filtro_maquina, filtro_estado], spacing=10),
        lista,
    ], spacing=12, expand=True)

    contenido = ft.Stack([
        ft.Container(content=cuerpo, padding=20, expand=True),
        ft.Container(content=menu_mas, right=15, bottom=15),
    ], expand=True)

    configurar_navbar(page, menu_mas, indice_inicial=1)
    page.add(ft.Column([header, contenido], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH, expand=True))
    actualizar_lista()

    if maquina_inicial:
        abrir_formulario(maquina_prefijada=maquina_inicial)
