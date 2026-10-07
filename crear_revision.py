import flet as ft
import estilos
from datetime import datetime
from sqlalchemy.orm import joinedload

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from models import Maquina, CriterioInspeccion, Inspeccion, Hallazgo, AccionCorrectiva

def vista_crear_revision(page: ft.Page, codigo_maquina: str):
    page.title = f"QualityCheck - Nueva Inspección {codigo_maquina}"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    usuario_id = page.session.store.get("usuario_id") or 1  

    aplicar_tema(page)
    menu_mas = crear_menu_mas(page)

    def mostrar_mensaje(mensaje):
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor=estilos.COLOR_TEXTO,
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    # 🔗 1. CONSULTAR MÁQUINA Y SUS CRITERIOS DESDE SUPABASE
    with SessionLocal() as db:
        maquina = (
            db.query(Maquina)
            .options(joinedload(Maquina.area_rel))
            .filter(Maquina.codigo_maquina == codigo_maquina, Maquina.activa == True)
            .first()
        )
        criterios = (
            db.query(CriterioInspeccion)
            .filter(CriterioInspeccion.id_maquina == maquina.id_maquina, CriterioInspeccion.activo == True)
            .all()
        ) if maquina else []

    if not maquina:
        page.add(ft.Text("La máquina especificada no existe.", color="#DC2626"))
        return

    # Controles generales de la inspección
    tipo_inspeccion = ft.Dropdown(
        label="Tipo de Inspección *",
        value="Preventiva",
        options=[
            ft.DropdownOption("Preventiva"),
            ft.DropdownOption("Rutinaria"),
            ft.DropdownOption("Especial"),
        ],
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    observaciones_generales = ft.TextField(
        label="Observaciones Generales",
        hint_text="Comentarios opcionales sobre el estado global del equipo...",
        multiline=True,
        min_lines=2,
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
    )

    # Lista dinámica de evaluación por criterio
    evaluaciones_ui = []

    def construir_control_criterio(criterio):
        sw_cumple = ft.Switch(
            label="Cumple con el estándar",
            value=True,
            active_color=estilos.COLOR_PRINCIPAL,
        )

        txt_hallazgo = ft.TextField(
            label="Descripción del Fallo / Hallazgo *",
            hint_text="Describa la falla detectada...",
            visible=False,
            border_color="#DC2626",
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
        )

        dd_severidad = ft.Dropdown(
            label="Severidad *",
            value="Media",
            visible=False,
            options=[
                ft.DropdownOption("Baja"),
                ft.DropdownOption("Media"),
                ft.DropdownOption("Alta"),
                ft.DropdownOption("Crítica"),
            ],
            border_color="#DC2626",
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
            width=150,
        )

        txt_accion = ft.TextField(
            label="Acción Correctiva Sugerida *",
            hint_text="Ej. Reemplazar manguera / Ajustar presión",
            visible=False,
            border_color="#BDBDBD",
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
            expand=True,
        )

        def on_switch_change(e):
            es_fallo = not sw_cumple.value
            txt_hallazgo.visible = es_fallo
            dd_severidad.visible = es_fallo
            txt_accion.visible = es_fallo
            page.update()

        sw_cumple.on_change = on_switch_change

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(criterio.nombre_criterio, size=14, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                                    ft.Text(f"Categoría: {criterio.categoria}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                                ],
                                expand=True,
                            ),
                            sw_cumple,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row([txt_hallazgo, dd_categoria := dd_severidad], spacing=8),
                    txt_accion,
                ],
                spacing=8,
            ),
            bgcolor="#FFFFFF",
            padding=12,
            border_radius=8,
            border=ft.Border(
                top=ft.BorderSide(1, "#E1E3E6"),
                bottom=ft.BorderSide(1, "#E1E3E6"),
                left=ft.BorderSide(1, "#E1E3E6"),
                right=ft.BorderSide(1, "#E1E3E6"),
            ),
        )

        evaluaciones_ui.append({
            "criterio": criterio,
            "sw_cumple": sw_cumple,
            "txt_hallazgo": txt_hallazgo,
            "dd_severidad": dd_severidad,
            "txt_accion": txt_accion,
        })

        return card

    lista_criterios_cont = ft.Column(
        controls=[construir_control_criterio(c) for c in criterios] if criterios else [
            ft.Text("Esta máquina no tiene criterios de inspección asignados. Configure los criterios en la pantalla de edición.", color=estilos.COLOR_TEXTO_SECUNDARIO)
        ],
        spacing=10,
    )

    # 🔑 2. GUARDAR INSPECCIÓN, HALLAZGOS Y ACCIONES CORRECTIVAS
    def guardar_inspeccion(e):
        hubo_fallas = False

        # Validaciones si hay fallos
        for item in evaluaciones_ui:
            if not item["sw_cumple"].value:
                hubo_fallas = True
                if not item["txt_hallazgo"].value.strip() or not item["txt_accion"].value.strip():
                    mostrar_mensaje("Describa el hallazgo y la acción correctiva para los puntos marcados con fallo.")
                    return

        try:
            with SessionLocal() as db:
                codigo_insp = f"INS-{int(datetime.now().timestamp())}"
                resultado_final = "Con Hallazgos" if hubo_fallas else "Aprobado"

                # A. Registrar Inspección
                nueva_inspeccion = Inspeccion(
                    codigo_inspeccion=codigo_insp,
                    id_maquina=maquina.id_maquina,
                    id_inspector=usuario_id,
                    tipo_inspeccion=tipo_inspeccion.value,
                    fecha_inspeccion=datetime.now(),
                    resultado_final=resultado_final,
                    observaciones_generales=observaciones_generales.value.strip() if observaciones_generales.value else None,
                )
                db.add(nueva_inspeccion)
                db.flush()  # Genera id_inspeccion

                # B. Registrar Hallazgos y Acciones Correctivas
                for item in evaluaciones_ui:
                    if not item["sw_cumple"].value:
                        nuevo_hallazgo = Hallazgo(
                            id_inspeccion=nueva_inspeccion.id_inspeccion,
                            id_criterio=item["criterio"].id_criterio,
                            nivel_severidad=item["dd_severidad"].value,
                            descripcion=item["txt_hallazgo"].value.strip(),
                            estado="Pendiente",
                        )
                        db.add(nuevo_hallazgo)
                        db.flush()  # Genera id_hallazgo

                        nueva_accion = AccionCorrectiva(
                            id_hallazgo=nuevo_hallazgo.id_hallazgo,
                            descripcion_accion=item["txt_accion"].value.strip(),
                            responsable="Por Asignar",
                            # La fecha es obligatoria en la tabla de acciones
                            # correctivas. Al crear el hallazgo se deja como
                            # compromiso inicial la fecha de registro.
                            fecha_compromiso=datetime.now(),
                            completada=False,
                        )
                        db.add(nueva_accion)

                # C. Actualizar estado de la máquina
                maq_db = db.query(Maquina).filter(Maquina.id_maquina == maquina.id_maquina).first()
                if maq_db:
                    maq_db.estado = "En revisión" if hubo_fallas else "Operativa"

                db.commit()

            mostrar_mensaje("Inspección guardada correctamente.")
            page.go(f"/maquinas/{codigo_maquina}")

        except Exception as ex:
            mostrar_mensaje(f"Error al guardar la inspección: {ex}")

    def cancelar(e):
        page.go(f"/maquinas/{codigo_maquina}")

    header = crear_header(titulo=f"Inspección: {codigo_maquina}")

    formulario = ft.Column(
        controls=[
            ft.Text(f"Nueva Inspección - {maquina.nombre}", size=18, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            ft.Text("Evalúa los puntos técnicos del equipo para registrar el reporte de mantenimiento.", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ft.Container(height=10),
            tipo_inspeccion,
            ft.Divider(height=1, color="#E1E3E6"),
            ft.Text("Puntos de Control / Criterios", size=15, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            lista_criterios_cont,
            ft.Container(height=10),
            observaciones_generales,
            ft.Container(height=14),
            ft.Row(
                [
                    ft.TextButton(content=ft.Text("Cancelar", color=estilos.COLOR_TEXTO), on_click=cancelar),
                    ft.Button(
                        content=ft.Text("Finalizar Inspección", color=estilos.COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                        bgcolor=estilos.COLOR_PRINCIPAL,
                        on_click=guardar_inspeccion,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=10,
            ),
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    cuerpo = ft.Container(content=formulario, padding=20, expand=True)
    configurar_navbar(page, menu_mas, indice_inicial=0)

    contenido = ft.Stack(
        [
            cuerpo,
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
