import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)

from database import SessionLocal
from models import Area
from services import crear_nueva_maquina, crear_criterio_inspeccion  

def vista_agregar_maquina(page: ft.Page):
    page.title = "QualityCheck - Agregar máquina"
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

    def cancelar(e):
        page.go("/maquinas")

    # 🔑 1. CONSULTAR ÁREAS ACTIVAS DESDE LA BASE DE DATOS
    with SessionLocal() as db:
        lista_areas = db.query(Area).filter(Area.activa == True).all()

    # Convertir las áreas a opciones de Dropdown de Flet
    opciones_areas = [
        ft.DropdownOption(key=str(area.id_area), text=area.nombre)
        for area in lista_areas
    ]

    # Controles del Formulario
    def crear_campo(label, hint):
        return ft.TextField(
            label=label,
            hint_text=hint,
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
            label_style=ft.TextStyle(size=11, color=estilos.COLOR_TEXTO_SECUNDARIO),
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
            expand=True,
        )

    codigo = crear_campo("Código *", "Ej. MAQ-02")
    nombre = crear_campo("Nombre *", "Ej. Torno 04")
    marca = crear_campo("Marca *", "Ej. Mazak")
    modelo = crear_campo("Modelo *", "Ej. QUICK TURN 250")
    ubicacion = crear_campo("Ubicación *", "Ej. Nave 1 - Pasillo B")

    # 📌 DROPDOWN DE ÁREAS (Cargado dinámicamente)
    dd_area = ft.Dropdown(
        label="Área *",
        hint_text="Seleccione un área",
        options=opciones_areas,
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    estado = ft.Dropdown(
        label="Estado",
        value="Operativa",
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

    # 🔑 2. FUNCIÓN DE GUARDADO ACTUALIZADA
    def guardar(e):
        # Validar que se hayan llenado los campos y seleccionado un área
        if not codigo.value or not nombre.value or not dd_area.value:
            mostrar_mensaje("Complete los campos obligatorios (*), incluyendo el área.")
            return

        datos_maquina = {
            "codigo_maquina": codigo.value.strip(),
            "nombre": nombre.value.strip(),
            "tipo": "Industrial",
            "marca": marca.value.strip() if marca.value else None,
            "modelo": modelo.value.strip() if modelo.value else None,
            "ubicacion": ubicacion.value.strip() if ubicacion.value else None,
            "id_area": int(dd_area.value),  # Clave foránea hacia la tabla 'areas'
            "estado": estado.value,
            "activa": True,
        }

        try:
            with SessionLocal() as db:
                # 1. Crear la máquina en PostgreSQL
                nueva_maquina = crear_nueva_maquina(db, datos_maquina)
                
                # 2. (Opcional) Asignar criterios de inspección por defecto a la nueva máquina
                # Ejemplo de criterios iniciales automáticos:
                criterios_base = [
                    {"categoria": "Seguridad", "nombre_criterio": "Paro de emergencia funcional"},
                    {"categoria": "Mantenimiento", "nombre_criterio": "Niveles de lubricante óptimos"},
                ]
                for crit in criterios_base:
                    crit["id_maquina"] = nueva_maquina.id_maquina
                    crear_criterio_inspeccion(db, crit)

            mostrar_mensaje("Máquina y criterios registrados correctamente.")
            page.go("/maquinas")

        except Exception as ex:
            mostrar_mensaje(f"Error al guardar: {ex}")

    header = crear_header()

    formulario = ft.Column(
        controls=[
            ft.Text("Nueva máquina", size=20, weight=ft.FontWeight.BOLD, color=estilos.COLOR_TEXTO),
            ft.Text("Registra los datos del equipo para incorporarlo al inventario.", size=13, color=estilos.COLOR_TEXTO_SECUNDARIO),
            ft.Container(height=12),
            ft.Row([codigo, nombre], spacing=12),
            ft.Row([marca, modelo], spacing=12),
            ft.Row([dd_area, ubicacion], spacing=12),  # ◄ El selector de Área reemplaza al campo de texto
            ft.Row([estado], spacing=12),
            ft.Container(height=16),
            ft.Row(
                [
                    ft.TextButton(content=ft.Text("Cancelar", color=estilos.COLOR_TEXTO), on_click=cancelar),
                    ft.Button(
                        content=ft.Text("Guardar máquina", color=estilos.COLOR_TEXTO, weight=ft.FontWeight.BOLD),
                        bgcolor=estilos.COLOR_PRINCIPAL,
                        on_click=guardar,
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
    configurar_navbar(page, menu_mas, indice_inicial=1)

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