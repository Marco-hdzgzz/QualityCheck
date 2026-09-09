import flet as ft


def main(page: ft.Page):
    page.title = "MantenimientoPro - Login"
    page.padding = 0
    page.window_width = 380
    page.window_height = 700
    page.window_resizable = False
    page.bgcolor = "#F5F6F8"

    def iniciar_sesion(e):
        if txt_usuario.value == "maria.lopez" and txt_password.value == "1234":
            page.snack_bar = ft.SnackBar(ft.Text("Bienvenida, María López"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario o contraseña incorrectos"))
            page.snack_bar.open = True
            page.update()

    def cerrar_recuperacion(e):
        dialogo_recuperacion.open = False
        page.update()

    header = ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    ft.Image(
                        src="logo.png",
                        width=44,
                        height=44,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    width=44,
                    height=44,
                    bgcolor="#FFFFFF",
                    border_radius=22,
                    alignment=ft.alignment.center,
                ),
                ft.Column(
                    [
                        ft.Text(
                            "QualityCheck",
                            color="#25252B",
                            weight=ft.FontWeight.BOLD,
                            size=20,
                        ),
                        ft.Text(
                            "SISTEMA DE INSPECCIÓN INDUSTRIAL",
                            color="#25252B",
                            size=9,
                        ),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ],
            spacing=10,
        ),
        bgcolor="#F5A000",
        padding=15,
    )

    txt_titulo = ft.Text(
        "Inicia sesión",
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#25252B",
        width=320,
        text_align=ft.TextAlign.LEFT,
    )

    txt_usuario = ft.TextField(
        label="USUARIO/CORREO",
        hint_text="Ingrese su usuario o correo electrónico",
        hint_style=ft.TextStyle(size=12, color="#6B7280"),
        value="maria.lopez",
        border_color="#BDBDBD",
        focused_border_color="#1e3d2f",
        label_style=ft.TextStyle(size=12, color="#616161"),
        width=320,
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    txt_password = ft.TextField(
        label="CONTRASEÑA",
        hint_text="Ingrese su contraseña",
        hint_style=ft.TextStyle(size=12, color="#6B7280"),
        password=True,
        can_reveal_password=True,
        border_color="#BDBDBD",
        focused_border_color="#1e3d2f",
        label_style=ft.TextStyle(size=12, color="#616161"),
        width=320,
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    txr_recordar = ft.Checkbox(
        label="Recordar usuario",
        value=False,
        label_style=ft.TextStyle(size=12, color="#616161"),
        active_color="#F5A000",
        width=320,
    )

    btn_entrar = ft.ElevatedButton(
        content=ft.Text("INICIAR SESIÓN", color="#25252B", weight=ft.FontWeight.BOLD),
        bgcolor="#F5A000",
        width=320,
        height=50,
        on_click=iniciar_sesion,
    )

    correo_recuperacion = ft.TextField(
        label="Correo electrónico",
        hint_text="Ingrese su correo electrónico",
        hint_style=ft.TextStyle(size=12, color="#6B7280"),
        border_color="#BDBDBD",
        focused_border_color="#1e3d2f",
        label_style=ft.TextStyle(size=12, color="#616161"),
        width=320,
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    dialogo_recuperacion = ft.AlertDialog(
        title=ft.Text(
            "Recuperación de contraseña", color="#25252B", weight=ft.FontWeight.BOLD
        ),
        content=ft.Column(
            [
                ft.Text(
                    "Ingrese su correo electrónico para recibir instrucciones de recuperación.",
                    color="#616161",
                    size=12,
                ),
                correo_recuperacion,
            ],
            tight=True,
        ),
        bgcolor="#F5f6f8",
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=cerrar_recuperacion,
                style=ft.ButtonStyle(
                    color={"": "#25252B"}, overlay_color={"": "#F5A000"}
                ),
            ),
            ft.TextButton(
                "Enviar",
                on_click=cerrar_recuperacion,
                style=ft.ButtonStyle(
                    color={"": "#25252B"}, overlay_color={"": "#F5A000"}
                ),
            ),
        ],
    )

    def open_recuperacion(e):
        page.dialog = dialogo_recuperacion
        dialogo_recuperacion.open = True
        page.update()

    recuperar_pass = ft.TextButton(
        content=ft.Text("¿Olvidaste tu contraseña?", color="#616161"),
        on_click=open_recuperacion,
    )

    pie_pagina = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.LOCK_OUTLINE, size=12, color="#919090"),
                ft.Text(
                    "Acceso seguro según rol técnico",
                    size=11,
                    color="#919090",
                    italic=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor="#EBEEF2",
        padding=10,
        border_radius=20,
    )

    cuerpo = ft.Container(
        content=ft.Column(
            [
                txt_titulo,
                ft.Container(height=10),
                txt_usuario,
                ft.Container(height=10),
                txt_password,
                ft.Container(height=5),
                txr_recordar,
                ft.Container(height=5),
                recuperar_pass,
                ft.Container(height=10),
                btn_entrar,
                ft.Container(height=30),
                pie_pagina,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
    )

    page.add(
        ft.Column(
            [header, cuerpo],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
    )


ft.app(target=main, assets_dir="assets")
