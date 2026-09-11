import flet as ft
import estilos

from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)


def vista_agregar_maquina(page: ft.Page):
    page.title = "QualityCheck - Agregar máquina"
    page.padding = 0
    page.bgcolor = estilos.COLOR_FONDO
    page.floating_action_button = None

    aplicar_tema(page)
    menu_mas = crear_menu_mas()

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

    def guardar(e):
        campos_requeridos = [codigo, nombre, marca, modelo, ubicacion]

        if any(not campo.value.strip() for campo in campos_requeridos):
            mostrar_mensaje("Complete todos los campos obligatorios.")
            return

        mostrar_mensaje("Máquina registrada correctamente.")
        page.go("/maquinas")

    def seleccionar_fecha(e):
        if selector_fecha.value:
            fecha_adquisicion.value = selector_fecha.value.strftime("%d/%m/%Y")
            page.update()

    selector_fecha = ft.DatePicker(
        on_change=seleccionar_fecha,
    )

    page.overlay.append(selector_fecha)

    def crear_campo(label, hint):
        return ft.TextField(
            label=label,
            hint_text=hint,
            border_color="#BDBDBD",
            focused_border_color=estilos.COLOR_PRINCIPAL,
            label_style=ft.TextStyle(
                size=11,
                color=estilos.COLOR_TEXTO_SECUNDARIO,
            ),
            bgcolor="#FFFFFF",
            color=estilos.COLOR_TEXTO,
            expand=True,
        )

    header = crear_header()
    codigo = crear_campo("Código *", "Ej. MAQ-02")
    nombre = crear_campo("Nombre *", "Ej. Torno 04")
    marca = crear_campo("Marca *", "Ej. Mazak")
    modelo = crear_campo("Modelo *", "Ej. QUICK TURN 250")
    ubicacion = crear_campo("Ubicación *", "Ej. Planta 1")
    estado = ft.Dropdown(
        label="Estado",
        value="Operativa",
        options=[
            ft.DropdownOption(key="Operativa", text="Operativa"),
            ft.DropdownOption(key="Mantenimiento", text="Mantenimiento"),
            ft.DropdownOption(key="Fuera de servicio", text="Fuera de servicio"),
        ],
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        bgcolor="#FFFFFF",
        color=estilos.COLOR_TEXTO,
        expand=True,
    )
    fecha_adquisicion = ft.TextField(
        label="Fecha de adquisición",
        read_only=True,
        bgcolor="#FFFFFF",
        border_color="#BDBDBD",
        focused_border_color=estilos.COLOR_PRINCIPAL,
        color=estilos.COLOR_TEXTO,
        expand=True,
    )

    formulario = ft.Column(
        controls=[
            ft.Text(
                "Nueva máquina",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=estilos.COLOR_TEXTO,
            ),
            ft.Text(
                "Registra los datos del equipo para incorporarlo al inventario.",
                size=13,
                color=estilos.COLOR_TEXTO_SECUNDARIO,
            ),
            ft.Container(height=12),
            ft.Row([codigo, nombre], spacing=12),
            ft.Row([marca, modelo], spacing=12),
            ft.Row([ubicacion, estado], spacing=12),
            ft.Row(
                [
                    fecha_adquisicion,
                    ft.IconButton(
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=lambda e: setattr(selector_fecha, "open", True),
                    ),
                ]
            ),
            ft.Container(height=8),
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Text("Cancelar", color=estilos.COLOR_TEXTO),
                        on_click=cancelar,
                    ),
                    ft.Button(
                        content=ft.Text(
                            "Guardar máquina",
                            color=estilos.COLOR_TEXTO,
                            weight=ft.FontWeight.BOLD,
                        ),
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

    cuerpo = ft.Container(
        content=formulario,
        padding=20,
        expand=True,
    )

    configurar_navbar(page, menu_mas, indice_inicial=1)

    contenido = ft.Stack(
        [
            cuerpo,
            ft.Container(
                content=menu_mas,
                right=15,
                bottom=15,
            ),
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
