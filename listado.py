import estilos
import flet as ft
from componentes import (
    aplicar_tema,
    crear_header,
    crear_menu_mas,
    configurar_navbar,
)


def vista_listado(page: ft.Page):
  page.title = "QualityCheck - Máquinas"
  page.padding = 0
  page.bgcolor = estilos.COLOR_FONDO

  page.window.width = 380
  page.window.height = 700
  page.window.resizable = True

  aplicar_tema(page)

  datos_maquina = {
      "codigo": "MAQ-01",
      "nombre": "Torno 03",
      "marca": "Mazak",
      "modelo": "QUICK TURN 200",
      "ubicacion": "Planta 1",
      "estado": "Operativa",
      "proximarev": "Prox. rev: 12 de Septiembre",
  }

  maquinas = [
      datos_maquina,
      {
          **datos_maquina,
          "codigo": "MAQ-02",
          "nombre": "Fresadora 01",
          "marca": "DMG Mori",
          "modelo": "CMX 600 V",
          "ubicacion": "Planta 2",
      },
      {
          **datos_maquina,
          "codigo": "MAQ-03",
          "nombre": "Prensa 02",
          "marca": "Haas",
          "modelo": "VF-2",
          "ubicacion": "Planta 1",
          "estado": "Mantenimiento",
          "proximarev": "Prox. rev: 15 de Septiembre",
      },
      {
          **datos_maquina,
          "codigo": "MAQ-04",
          "nombre": "Cortadora Laser",
          "marca": "Trumpf",
          "modelo": "TruLaser 3030",
          "ubicacion": "Planta 3",
          "estado": "Fuera de servicio",
          "proximarev": "Sin programar",
      },
  ]

  lista_maquinas = ft.ListView(
      expand=True,
      spacing=10,
  )

  txt_cantidad = ft.Text(
      "",
      size=14,
      color=estilos.COLOR_TEXTO_SECUNDARIO,
  )

  def construir_tarjeta(maquina):
    if maquina["estado"] == "Operativa":
      color_estado = "#166534"
      fondo_estado = "#DCFCE7"
    elif maquina["estado"] == "Mantenimiento":
      color_estado = "#92400E"
      fondo_estado = "#FEF3C7"
    else:
      color_estado = "#991B1B"
      fondo_estado = "#FEE2E2"

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    maquina["codigo"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=estilos.COLOR_TEXTO,
                                ),
                                ft.Text(
                                    maquina["nombre"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=estilos.COLOR_TEXTO,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.IconButton(
                            icon=ft.CupertinoIcons.SQUARE_PENCIL,
                            tooltip="Editar máquina",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row([
                    ft.Text(
                        maquina["marca"],
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                    ft.Text(
                        maquina["modelo"],
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                    ft.Text(
                        maquina["ubicacion"],
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                ]),
                ft.Row([
                    ft.Container(
                        content=ft.Text(
                            maquina["estado"],
                            size=12,
                            color=color_estado,
                            weight=ft.FontWeight.BOLD,
                        ),
                        bgcolor=fondo_estado,
                        padding=5,
                        border_radius=20,
                    ),
                    ft.Text(
                        maquina["proximarev"],
                        size=12,
                        color=estilos.COLOR_TEXTO_SECUNDARIO,
                    ),
                ]),
            ],
            tight=True,
        ),
        bgcolor="#FFFFFF",
        border=ft.Border(
            top=ft.BorderSide(1, "#E1E3E6"),
            bottom=ft.BorderSide(1, "#E1E3E6"),
            left=ft.BorderSide(1, "#E1E3E6"),
            right=ft.BorderSide(1, "#E1E3E6"),
        ),
        border_radius=20,
        padding=14,
        expand=True,
        on_click=lambda _: page.go(f"/maquinas/{maquina['codigo']}"),
    )

  filtro_actual = "Todas"

  def filtrar_y_actualizar():
    texto_busqueda = txt_buscador.value.lower().strip()
    filtradas = []

    for m in maquinas:
      if filtro_actual != "Todas" and m["estado"] != filtro_actual:
        continue

      coincide_texto = (
          texto_busqueda in m["codigo"].lower()
          or texto_busqueda in m["nombre"].lower()
          or texto_busqueda in m["marca"].lower()
          or texto_busqueda in m["modelo"].lower()
          or texto_busqueda in m["ubicacion"].lower()
      )

      if texto_busqueda == "" or coincide_texto:
        filtradas.append(m)

    lista_maquinas.controls = [construir_tarjeta(m) for m in filtradas]
    total = len(filtradas)
    txt_cantidad.value = (
        f"{total} equipo registrado"
        if total == 1
        else f"{total} equipos registrados"
    )
    page.update()

  def on_busqueda_change(e):
    filtrar_y_actualizar()

  txt_buscador = ft.TextField(
      hint_text="Buscar máquina por nombre, marca o modelo",
      hint_style=ft.TextStyle(
          color=estilos.COLOR_TEXTO_SECUNDARIO,
      ),
      border_radius=10,
      border_color=estilos.COLOR_TEXTO_SECUNDARIO,
      focused_border_color=estilos.COLOR_PRINCIPAL,
      bgcolor="#FFFFFF",
      color=estilos.COLOR_TEXTO,
      expand=True,
      on_change=on_busqueda_change,
  )

  buscar = ft.Container(
      content=ft.Row(
          [
              txt_buscador,
              ft.Icon(
                  ft.Icons.SEARCH,
                  size=20,
                  color=estilos.COLOR_TEXTO_SECUNDARIO,
              ),
          ],
          expand=True,
      )
  )

  chips_refs = {}

  def seleccionar_filtro(e, categoria):
    nonlocal filtro_actual
    filtro_actual = categoria

    for cat, chip in chips_refs.items():
      if cat == categoria:
        chip.bgcolor = estilos.COLOR_PRINCIPAL
        chip.label = ft.Text(cat, color="#FFFFFF", weight=ft.FontWeight.BOLD)
      else:
        chip.bgcolor = "#FFFFFF"
        chip.label = ft.Text(cat, color=estilos.COLOR_TEXTO)

    filtrar_y_actualizar()

  categorias_chips = ["Todas", "Operativas", "Mantenimiento", "Fuera de servicio"]
  chips_controles = []

  for cat in categorias_chips:
    es_primer = cat == "Todas"
    chip = ft.Chip(
        label=ft.Text(
            cat,
            color="#FFFFFF" if es_primer else estilos.COLOR_TEXTO,
            weight=ft.FontWeight.BOLD if es_primer else ft.FontWeight.NORMAL,
        ),
        bgcolor=estilos.COLOR_PRINCIPAL if es_primer else "#FFFFFF",
        on_select=lambda e, c=cat: seleccionar_filtro(e, c),
    )
    chips_refs[cat] = chip
    chips_controles.append(chip)

  filtros = ft.Row(
      controls=chips_controles,
      scroll=ft.ScrollMode.AUTO,
  )

  header = crear_header()
  menu_mas = crear_menu_mas()

  txt_titulo = ft.Text(
      "Máquinas",
      size=20,
      weight=ft.FontWeight.BOLD,
      color=estilos.COLOR_TEXTO,
  )

  page.floating_action_button = ft.FloatingActionButton(
      ft.Row(
          [
              ft.Icon(
                  ft.Icons.ADD,
                  color=estilos.COLOR_TEXTO,
                  size=18,
              ),
              ft.Text(
                  "Agregar Máquina",
                  size=15,
                  color=estilos.COLOR_TEXTO,
                  weight=ft.FontWeight.BOLD,
              ),
          ],
          tight=True,
          spacing=6,
      ),
      bgcolor=estilos.COLOR_PRINCIPAL,
      width=160,
      on_click=lambda _: page.go("/maquinas/agregar"),
  )

  page.floating_action_button_location = (
      ft.FloatingActionButtonLocation.END_FLOAT
  )

  configurar_navbar(
      page,
      menu_mas,
      indice_inicial=1,
  )

  columna = ft.Column(
      controls=[
          txt_titulo,
          txt_cantidad,
          buscar,
          ft.Container(height=10),
          filtros,
          ft.Container(height=10),
          lista_maquinas,
      ],
      spacing=4,
      expand=True,
  )

  cuerpo = ft.Container(
      content=ft.Column(
          controls=[
              columna,
              ft.Container(height=10),
          ],
          horizontal_alignment=ft.CrossAxisAlignment.START,
          expand=True,
      ),
      padding=20,
      expand=True,
  )

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
          controls=[
              header,
              contenido,
          ],
          spacing=0,
          horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
          expand=True,
      )
  )

  filtrar_y_actualizar()
