# QualityCheck — Puntos 22 y 23

## Punto 22 — Historial de revisiones

Se agregó `historial_revisiones.py` y la ruta `/revisiones/historial`.

El historial muestra revisiones **Completadas** y **Canceladas**, permite filtrar por máquina y estado, y consultar el registro con fecha programada/realizada, resultado, responsable, observaciones, acciones realizadas y próxima revisión.

El acceso está disponible desde la pantalla **Revisiones preventivas** mediante el botón **Historial**.

## Punto 23 — Integración y pruebas de revisiones preventivas

Se integró el flujo:

`Dashboard -> Gestionar revisiones -> Revisiones preventivas -> Historial`

Y desde maquinaria:

`Máquinas -> Detalle -> Programar revisión -> Nueva revisión preventiva`

Se separó `MAQUINAS` a `maquinas_data.py` para que el servicio pueda reutilizar los datos de maquinaria sin depender de la interfaz Flet.

Se agregó `test_revisiones_preventivas.py` con pruebas de:

- crear, editar y completar una revisión;
- historial de completadas;
- cancelar y conservar en historial;
- cálculo de revisión vencida;
- rechazo de máquina inexistente;
- persistencia entre instancias del servicio.

Ejecutar pruebas:

```powershell
py -m unittest -v test_revisiones_preventivas.py
```

Ejecutar aplicación:

```powershell
py login.py
```
