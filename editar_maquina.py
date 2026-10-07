import flet as ft
import estilos
from sqlalchemy.orm import joinedload

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from models import Maquina, Area, CriterioInspeccion
from services import (
    eliminar_maquina,
    obtener_criterios_por_maquina,
    crear_criterio_inspeccion,
    eliminar_criterio_inspeccion,
)

def vista_editar_maquina(page: ft.Page, codigo_maquina: str):
    page.title = f"QualityCheck - Editar {codigo_maquina}"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

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

    #1. CONSULTAR DATOS DE LA MÁQUINA Y ÁREAS EN SUPABASE
    with SessionLocal() as db:
        maquina = (
            db.query(Maquina)
            .options(joinedload(Maquina.area_rel))
            .filter(Maquina.codigo_maquina == codigo_maquina, Maquina.activa == True)
            .first()
        )
        lista_areas = db.query(Area).filter(Area.activa == True).all()

        criterios_bd = []
        if maquina:
            criterios_bd = db.query(CriterioInspeccion).filter(
                CriterioInspeccion.id_maquina == maquina.id_maquina,
                CriterioInspeccion.activo == True
            ).all()

    if not maquina:
        page.add(ft.Text("La máquina a editar no existe o fue desactivada.", color="#DC2626"))
        return

    criterios_temporales = [
        {"nombre_criterio": c.nombre_criterio, "categoria": c.categoria}
        for c in criterios_bd
    ]

    # Opciones para el selector de áreas
    opciones_areas = [
        ft.DropdownOption(key=str(area.id_area), text=area.nombre)
        for area in lista_areas
    ]

    # Controles prellenados con la información actual de la base de datos
    def crear_campo(label, value=""):
        return ft.TextField(
            label=label,
            value=value or "",
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
            label_style=ft.TextStyle(size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
            expand=True,
        )

    codigo = crear_campo("Código *", maquina.codigo_maquina)
    nombre = crear_campo("Nombre *", maquina.nombre)
    tipo = crear_campo("Tipo *", maquina.tipo)
    marca = crear_campo("Marca", maquina.marca)
    modelo = crear_campo("Modelo", maquina.modelo)
    numero_serie = crear_campo("Número de serie", maquina.numero_serie)
    ubicacion = crear_campo("Ubicación", maquina.ubicacion)

    dd_area = ft.Dropdown(
        label="Área *",
        value=str(maquina.id_area),
        options=opciones_areas,
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    estado = ft.Dropdown(
        label="Estado",
        value=maquina.estado or "Operativa",
        options=[
            ft.DropdownOption(key="Operativa", text="Operativa"),
            ft.DropdownOption(key="En revisión", text="En revisión"),
            ft.DropdownOption(key="Fuera de servicio", text="Fuera de servicio"),
        ],
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    
    # 2. FUNCIÓN PARA APLICAR LOS CAMBIOS EN POSTGRESQL (UPDATE)
    def guardar_cambios(e):
        if not codigo.value or not nombre.value or not tipo.value or not dd_area.value:
            mostrar_mensaje("Complete los campos obligatorios (*).")
            return

        datos_actualizados = {
            "codigo_maquina": codigo.value.strip(),
            "nombre": nombre.value.strip(),
            "tipo": tipo.value.strip(),
            "marca": marca.value.strip() if marca.value else None,
            "modelo": modelo.value.strip() if modelo.value else None,
            "numero_serie": numero_serie.value.strip() if numero_serie.value else None,
            "ubicacion": ubicacion.value.strip() if ubicacion.value else None,
            "id_area": int(dd_area.value),
            "estado": estado.value,
        }

        try:
            with SessionLocal() as db:
                # 1. Actualizar atributos de la máquina
                maq_db = db.query(Maquina).filter(Maquina.id_maquina == maquina.id_maquina).first()
                if maq_db:
                    for clave, valor in datos_actualizados.items():
                        setattr(maq_db, clave, valor)

                    db.commit()

            mostrar_mensaje("Máquina y criterios actualizados correctamente.")
            page.go(f"/maquinas/{codigo.value.strip()}")

        except Exception as ex:
            mostrar_mensaje(f"Error al actualizar la máquina: {ex}")

    def cancelar(e):
        page.go(f"/maquinas/{codigo_maquina}")

    def cerrar_confirmacion(e=None):
        dialogo_eliminar.open = False
        page.update()

    def confirmar_eliminacion(e):
        try:
            with SessionLocal() as db:
                eliminada = eliminar_maquina(db, maquina.id_maquina)
            cerrar_confirmacion()
            if eliminada:
                mostrar_mensaje("Máquina eliminada correctamente.")
                page.go("/maquinas")
            else:
                mostrar_mensaje("No fue posible encontrar la máquina para eliminarla.")
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar la máquina: {ex}")

    dialogo_eliminar = ft.AlertDialog(
        title=ft.Text("¿Eliminar máquina?", weight=ft.FontWeight.BOLD),
        content=ft.Text(
            "Se eliminarán la máquina, sus criterios, revisiones, hallazgos y acciones correctivas. Esta acción no se puede deshacer.",
            size=12,
        ),
        actions=[
            ft.TextButton(content=ft.Text("Cancelar"), on_click=cerrar_confirmacion),
            ft.TextButton(content=ft.Text("Eliminar", color="#DC2626"), on_click=confirmar_eliminacion),
        ],
    )

    def solicitar_eliminacion(e):
        if dialogo_eliminar not in page.overlay:
            page.overlay.append(dialogo_eliminar)
        dialogo_eliminar.open = True
        page.update()

    

    header = crear_header(titulo=f"Editar: {codigo_maquina}")

# --- CONTROLES DE CRITERIOS DE INSPECCIÓN ---
    lista_criterios_ui = ft.Column(spacing=6)

    txt_nuevo_criterio = ft.TextField(
        label="Nombre del criterio / punto a revisar",
        hint_text="Ej. Nivel de aceite hidráulico",
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    dd_categoria_criterio = ft.Dropdown(
        label="Categoría",
        value="General",
        options=[
            ft.DropdownOption("General"),
            ft.DropdownOption("Seguridad"),
            ft.DropdownOption("Mecánico"),
            ft.DropdownOption("Eléctrico"),
            ft.DropdownOption("Neumático"),
        ],
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        width=150,
    )

    def recargar_criterios():
        with SessionLocal() as db:
            criterios_bd = obtener_criterios_por_maquina(db, maquina.id_maquina)

        lista_criterios_ui.controls = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(c.nombre_criterio, size=13, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
                                ft.Text(f"Categoría: {c.categoria}", size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color="#DC2626",
                            tooltip="Eliminar criterio",
                            # 🔑 Elimina el registro por su 'id_criterio' real de la BD
                            on_click=lambda _, id_crit=c.id_criterio: borrar_criterio_bd(id_crit),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor="#FFFFFF",
                padding=8,
                border_radius=8,
                border=ft.Border(
                    top=ft.BorderSide(1, "#E1E3E6"),
                    bottom=ft.BorderSide(1, "#E1E3E6"),
                    left=ft.BorderSide(1, "#E1E3E6"),
                    right=ft.BorderSide(1, "#E1E3E6"),
                ),
            )
            for c in criterios_bd
        ]
        page.update()

    # 🔑 GUARDAR CRITERIO PERMANENTEMENTE EN LA BD
    def agregar_criterio(e):
        if txt_nuevo_criterio.value.strip():
            try:
                with SessionLocal() as db:
                    crear_criterio_inspeccion(
                        db=db,
                        id_maquina=maquina.id_maquina,
                        nombre_criterio=txt_nuevo_criterio.value.strip(),
                        categoria=dd_categoria_criterio.value or "General"
                    )
                txt_nuevo_criterio.value = ""
                recargar_criterios()  # Vuelve a consultar la BD para refrescar la lista
                mostrar_mensaje("Criterio guardado en la máquina.")
            except Exception as ex:
                mostrar_mensaje(f"Error al guardar criterio: {ex}")

    # 🔑 ELIMINAR CRITERIO DIRECTAMENTE DE LA BD
    def borrar_criterio_bd(id_criterio: int):
        try:
            with SessionLocal() as db:
                eliminar_criterio_inspeccion(db, id_criterio)
            recargar_criterios()
            mostrar_mensaje("Criterio eliminado.")
        except Exception as ex:
            mostrar_mensaje(f"Error al eliminar criterio: {ex}")

    btn_agregar_criterio = ft.IconButton(
        icon=ft.Icons.ADD_CIRCLE,
        icon_color=estilos.COLOR_PRINCIPAL,
        tooltip="Añadir criterio",
        on_click=agregar_criterio,
    )

    seccion_criterios = ft.Column(
        [
            ft.Divider(height=1, color="#E1E3E6"),
            ft.Text("Criterios de Inspección Específicos", size=16, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            ft.Text("Define los puntos técnicos que se evaluarán en cada revisión preventiva de este equipo.", size=12, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ft.Row([txt_nuevo_criterio, dd_categoria_criterio, btn_agregar_criterio], spacing=8),
            lista_criterios_ui,
        ],
        spacing=8,
    )

    # 🔑 CARGA INICIAL AL ABRIR LA PANTALLA
    recargar_criterios()

    formulario = ft.Column(
        controls=[
            ft.Text("Editar máquina", size=20, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            ft.Text("Modifica las especificaciones o ubicación de la máquina.", size=13, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ft.Container(height=12),
            ft.Row([codigo, nombre], spacing=12),
            ft.Row([tipo, numero_serie], spacing=12),
            ft.Row([marca, modelo], spacing=12),
            ft.Row([dd_area, ubicacion], spacing=12),
            ft.Row([estado], spacing=12),
            ft.Container(height=16),
            seccion_criterios,
            ft.Container(height=16),
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Text("Eliminar máquina", color="#DC2626"),
                        on_click=solicitar_eliminacion,
                    ),
                    ft.TextButton(content=ft.Text("Cancelar", color=estilos.COLOR_TEXTO), on_click=cancelar),
                    ft.Button(
                        content=ft.Text("Guardar cambios", color=estilos.COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                        bgcolor=estilos.COLOR_PRINCIPAL,
                        on_click=guardar_cambios,
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
