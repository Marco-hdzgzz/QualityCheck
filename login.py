import flet as ft

from componentes import crear_header
from agregar_maquina import vista_agregar_maquina
from dashboard import vista_dashboard
from detalle_maquina import vista_detalle_maquina
from listado import vista_listado


def main(page: ft.Page):
    page.title = "QualityCheck - Login"
    page.padding = 0
    page.bgcolor = "#F5F6F8"

    page.window.width = 380
    page.window.height = 700
    page.window.resizable = False

    def mostrar_snackbar(mensaje):
        snackbar = ft.SnackBar(
            content=ft.Text(
                mensaje,
                color="#FFFFFF",
            ),
            bgcolor="#25252B",
        )

        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def cambiar_ruta(e):
        page.clean()

        if page.route == "/dashboard":
            vista_dashboard(page)

        elif page.route == "/maquinas":
            vista_listado(page)

        elif page.route == "/maquinas/agregar":
            vista_agregar_maquina(page)

        elif page.route.startswith("/maquinas/"):
            codigo_maquina = page.route.rsplit("/", 1)[-1]
            vista_detalle_maquina(page, codigo_maquina)

    def iniciar_sesion(e):
        if txt_usuario.value == "maria.lopez" and txt_password.value == "1234":
            page.window.resizable = True
            page.go("/dashboard")
        else:
            mostrar_snackbar("Usuario o contraseña incorrectos")

    def cerrar_recuperacion(e):
        dialogo_recuperacion.open = False
        page.update()

    def enviar_recuperacion(e):
        if correo_recuperacion.value:
            dialogo_recuperacion.open = False
            page.update()
            mostrar_snackbar("Se enviaron instrucciones de recuperación.")
        else:
            mostrar_snackbar("Ingrese un correo electrónico.")

    def abrir_recuperacion(e):
        if dialogo_recuperacion not in page.overlay:
            page.overlay.append(dialogo_recuperacion)

        dialogo_recuperacion.open = True
        page.update()

    page.on_route_change = cambiar_ruta

    header = crear_header()

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
        hint_style=ft.TextStyle(
            size=12,
            color="#6B7280",
        ),
        value="maria.lopez",
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(
            size=11,
            color="#616161",
        ),
        width=320,
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    txt_password = ft.TextField(
        label="CONTRASEÑA",
        hint_text="Ingrese su contraseña",
        hint_style=ft.TextStyle(
            size=12,
            color="#6B7280",
        ),
        value="1234",
        password=True,
        can_reveal_password=True,
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(
            size=11,
            color="#616161",
        ),
        width=320,
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    checkbox_recordar = ft.Checkbox(
        value=False,
        active_color="#F5A000",
    )

    recordar_usuario = ft.Container(
        content=ft.Row(
            [
                checkbox_recordar,
                ft.Text(
                    "Recordar usuario",
                    size=12,
                    color="#616161",
                ),
            ],
            spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=320,
    )

    correo_recuperacion = ft.TextField(
        label="Correo electrónico",
        hint_text="Ingrese su correo electrónico",
        hint_style=ft.TextStyle(
            size=12,
            color="#6B7280",
        ),
        border_color="#BDBDBD",
        focused_border_color="#F5A000",
        label_style=ft.TextStyle(
            size=11,
            color="#616161",
        ),
        bgcolor="#FFFFFF",
        color="#25252B",
    )

    dialogo_recuperacion = ft.AlertDialog(
        title=ft.Text(
            "Recuperación de contraseña",
            color="#25252B",
            weight=ft.FontWeight.BOLD,
        ),
        content=ft.Column(
            [
                ft.Text(
                    "Ingrese su correo electrónico para recibir instrucciones de recuperación.",
                    color="#616161",
                    size=12,
                ),
                ft.Container(height=10),
                correo_recuperacion,
            ],
            tight=True,
        ),
        bgcolor="#F5F6F8",
        actions=[
            ft.TextButton(
                content=ft.Text(
                    "Cancelar",
                    color="#25252B",
                ),
                on_click=cerrar_recuperacion,
            ),
            ft.TextButton(
                content=ft.Text(
                    "Enviar",
                    color="#25252B",
                    weight=ft.FontWeight.BOLD,
                ),
                on_click=enviar_recuperacion,
            ),
        ],
    )

    recuperar_pass = ft.TextButton(
        content=ft.Text(
            "¿Olvidaste tu contraseña?",
            color="#616161",
            size=12,
        ),
        on_click=abrir_recuperacion,
    )

    btn_entrar = ft.Button(
        content=ft.Text(
            "INICIAR SESIÓN",
            color="#25252B",
            weight=ft.FontWeight.BOLD,
            size=13,
        ),
        bgcolor="#F5A000",
        width=320,
        height=48,
        on_click=iniciar_sesion,
    )

    pie_pagina = ft.Container(
        content=ft.Row(
            [
                ft.Icon(
                    ft.Icons.LOCK_OUTLINE,
                    size=12,
                    color="#919090",
                ),
                ft.Text(
                    "Acceso seguro según rol técnico",
                    size=11,
                    color="#919090",
                    italic=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
            tight=True,
        ),
        bgcolor="#EBEEF2",
        padding=10,
        border_radius=20,
    )

    formulario = ft.Column(
        [
            txt_titulo,
            ft.Container(height=14),
            txt_usuario,
            ft.Container(height=10),
            txt_password,
            ft.Container(height=4),
            recordar_usuario,
            ft.Container(height=2),
            recuperar_pass,
            ft.Container(height=10),
            btn_entrar,
            ft.Container(height=30),
            pie_pagina,
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

    page.add(
        ft.Column(
            [
                header,
                cuerpo,
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        )
    )


ft.run(
    main,
    assets_dir="assets",
)
