import flet as ft
from componentes import crear_header

def vista_editar_maquina(page: ft.Page, codigo_maquina: str):
    page.clean()
    page.title = f"QualityCheck - Editar {codigo_maquina}"
    page.padding = 0
    page.bgcolor = "#F5F6F8"

    maquinas_datos = {
        "MAQ-01": {"nombre": "Torno 03", "marca": "Mazak", "modelo": "QUICK TURN 200", "planta": "Planta 1", "estado": "Operativa"},
        "MAQ-02": {"nombre": "Fresadora 01", "marca": "DMG Mori", "modelo": "CMX 600 V", "planta": "Planta 2", "estado": "Operativa"},
    }

    datos = maquinas_datos.get(codigo_maquina, {"nombre": "Máquina Genérica", "marca": "Marca", "modelo": "Modelo", "planta": "Planta 1", "estado": "Operativa"})

    def mostrar_snackbar(mensaje):
        snackbar = ft.SnackBar(
            content=ft.Text(mensaje, color="#FFFFFF"),
            bgcolor="#25252B",
        )
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def guardar_cambios(e):
        mostrar_snackbar(f"¡Cambios guardados para {codigo_maquina}!")
        page.go("/maquinas")

    def cancelar(e):
        page.go("/maquinas")

    header = crear_header()

    txt_titulo = ft.Text(
        f"Editar Máquina: {codigo_maquina}",
        size=18,
        weight=ft.FontWeight.BOLD,
        color="#25252B",
    )

    txt_nombre = ft.TextField(
        label="NOMBRE DE LA MÁQUINA",
        value=datos["nombre"],
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(size=11, color="#616161"),
        bgcolor="#FFFFFF",
        color="#25252B",
        width=320,
    )

    txt_marca = ft.TextField(
        label="MARCA",
        value=datos["marca"],
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(size=11, color="#616161"),
        bgcolor="#FFFFFF",
        color="#25252B",
        width=320,
    )

    txt_modelo = ft.TextField(
        label="MODELO",
        value=datos["modelo"],
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(size=11, color="#616161"),
        bgcolor="#FFFFFF",
        color="#25252B",
        width=320,
    )

    txt_planta = ft.TextField(
        label="PLANTA / UBICACIÓN",
        value=datos["planta"],
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(size=11, color="#616161"),
        bgcolor="#FFFFFF",
        color="#25252B",
        width=320,
    )

    btn_guardar = ft.Button(
        content=ft.Text(
            "GUARDAR CAMBIOS",
            color="#25252B",
            weight=ft.FontWeight.BOLD,
            size=13,
            text_align=ft.TextAlign.CENTER # <-- Agrega esta línea
        ),
        bgcolor="#F5A000",
        width=150,
        height=45,
        on_click=guardar_cambios,
    )

    btn_cancelar = ft.Button(
        content=ft.Text("CANCELAR", color="#616161", weight=ft.FontWeight.BOLD, size=13),
        bgcolor="#E0E0E0",
        width=150,
        height=45,
        on_click=cancelar,
    )

    acciones = ft.Row(
        [btn_cancelar, btn_guardar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    formulario = ft.Column(
        [
            txt_titulo,
            ft.Container(height=15),
            txt_nombre,
            ft.Container(height=10),
            txt_marca,
            ft.Container(height=10),
            txt_modelo,
            ft.Container(height=10),
            txt_planta,
            ft.Container(height=25),
            acciones,
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    cuerpo = ft.Container(
        content=formulario,
        padding=20,
        alignment=ft.Alignment.TOP_CENTER,
        expand=True,
    )

    vista_final = ft.Column(
        [
            header,
            cuerpo,
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    page.add(vista_final)
    page.update()