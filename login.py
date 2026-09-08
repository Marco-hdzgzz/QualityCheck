import flet as ft


def main(page: ft.Page):
  page.title = "MantenimientoPro - Login"
  page.padding = 0
  page.window_width = 380
  page.window_height = 700
  page.window_resizable = False  # Evita que se deforme al maximizar
  page.bgcolor = "#FFFFFF"

  def iniciar_sesion(e):
    if txt_usuario.value == "maria.lopez" and txt_password.value == "1234":
      page.snack_bar = ft.SnackBar(ft.Text("Bienvenida, María López"))
      page.snack_bar.open = True
      page.update()
    else:
      page.snack_bar = ft.SnackBar(
          ft.Text("Usuario o contraseña incorrectos")
      )
      page.snack_bar.open = True
      page.update()

  # Encabezado adaptado para ocupar el ancho completo de la vista móvil
  header = ft.Container(
      content=ft.Row(
          [
              ft.Text(
                  "QualityCheck",
                  color="#FFFFFF",
                  weight=ft.FontWeight.BOLD,
                  size=15,
              ),
              ft.Text(
                  "SISTEMA DE INSPECCIÓN INDUSTRIAL",
                  color="#B0BEC5",
                  size=9,
              ),
          ],
          alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
      ),
      bgcolor="#1e3d2f",
      padding=15,
  )

  txt_usuario = ft.TextField(
      label="USUARIO",
      value="maria.lopez",
      border_color="#BDBDBD",
      focused_border_color="#1e3d2f",
      label_style=ft.TextStyle(size=12, color="#616161"),
      width=320,
  )

  txt_password = ft.TextField(
      label="CONTRASEÑA",
      value="........",
      password=True,
      can_reveal_password=True,
      border_color="#BDBDBD",
      focused_border_color="#1e3d2f",
      label_style=ft.TextStyle(size=12, color="#616161"),
      width=320,
  )

  btn_entrar = ft.ElevatedButton(
      content=ft.Text(
          "INICIAR SESIÓN", color="#FFFFFF", weight=ft.FontWeight.BOLD
      ),
      bgcolor="#23884e",
      width=320,
      on_click=iniciar_sesion,
  )

  recuperar_pass = ft.TextButton(
      content=ft.Text("¿Olvidaste tu contraseña?", color="#616161"),
  )

  pie_pagina = ft.Text(
      "Acceso seguro según rol técnico",
      size=11,
      color="#9E9E9E",
      italic=True,
  )

  cuerpo = ft.Container(
      content=ft.Column(
          [
              ft.Container(height=30),
              txt_usuario,
              ft.Container(height=10),
              txt_password,
              ft.Container(height=5),
              recuperar_pass,
              ft.Container(height=25),
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
          [header, cuerpo], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH
      )
  )


ft.app(target=main)