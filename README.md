# Django-CPs

Es una app minimalista en Django que implementa un API-REST para la busqueda de un código postal regresando una respuesta en formato JSON.

## Acerca del proyecto

La solucion a simple vista parece ser unos simples inserts y selects a una tabla en mysql para regresar las colonias asosiadas con un CP. Pero en los detalles es donde esta la elegancia y me gustaria explicarlos.

### Caracteristicas principales

- El servicio cuenta con un endpoint para el cargado de informacion a la base de datos de forma asincrona con ayuda de Celery.
  - Y envia un email al terminar la operacion (si ingresas uno valido).
- Se usa redis para peticiones recurrentes y asi ahorrarnos computo al no llegar hasta MYSQL.
- Todo esta dockerizado para su facil deployment.
- No se repite informacion innecesaria al momento de crear el seed a la DB.

## Primeros pasos

Para poner en marcha una copia local siga estos sencillos pasos:

### Prerequisitos

- Docker con Docker compose

### Instalacion

A continuacion se presentan los pasos a seguir para replicar la aplicacion en un ambiente local.

```sh
  git clone <REPO>
  cd <REPO>
  docker-compose up --build -d
```
