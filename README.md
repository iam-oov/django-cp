# Django-CPs

Django-CPs es una aplicación minimalista en Django que implementa una API-REST para la búsqueda de códigos postales, devolviendo respuestas en formato JSON.

## Acerca del Proyecto

A primera vista, la solución parece consistir en simples inserciones y selecciones en una tabla de MySQL para recuperar los vecindarios asociados a un código postal. Pero requiere un analisis correcto de las relaciones a DB, UX en los tiempos de carga y mantener la informacion actualizada.

### Características Principales

- El servicio cuenta con un punto final para la carga asincrónica de información en la base de datos utilizando Celery.
  - Se envía un correo electrónico al completar la operación (si se proporciona un correo válido).
- Redis se utiliza para peticiones recurrentes, optimizando los recursos computacionales al evitar consultas innecesarias a MySQL.
- Toda la aplicación está dockerizada para facilitar su implementación.
- Se elimina la información redundante durante la carga inicial de datos.

## Primeros Pasos

Para configurar una copia local, sigue estos sencillos pasos:

### Prerrequisitos

- Docker con Docker Compose
- Crea un archivo llamado `dev.env` dentro del directorio `environments` para asignar crear e inicialiar las variables de entorno.

Aquí tienes un ejemplo del contenido del archivo:

```sh
# Configuración General de la Aplicación
DJANGO_APP_SECRET_KEY=django-insecure-eoxp
DJANGO_DEBUG=True

# Correo Electrónico
EMAIL_HOST_PASSWORD=1234abcd
EMAIL_HOST_USER=osvaldo@mail.com

# MySQL
MYSQL_DATABASE=mysql_database
MYSQL_LOCAL_HOST=my-mysql
MYSQL_PASSWORD=mysql_pass
MYSQL_ROOT_PASSWORD=mysql_pass
MYSQL_TCP_PORT=3307
MYSQL_USER=mysql_pass

# Redis
REDIS_DB=0
REDIS_HOST=my-redis
REDIS_PORT=6381
```

## Instalación

Los siguientes pasos describen cómo replicar la aplicación en un entorno local.

```sh
git clone <REPO>
cd <REPO>
docker-compose up --build -d
```

Esto hara que django ocupe el puerto 8000. Mysql el puerto 3007. Redis el puerto 6381 y celery el puerto

### Cargar la Base de Datos (seeds)

```sh
[GET] http://localhost:8000/load-db/?email=osvaldo@mail.com
```

Esto desencadena una tarea de Celery que tarda aproximadamente de 15 a 20 minutos en completarse. Al finalizar, se envía una notificación por correo electrónico confirmando la carga de datos.

### Obtener Detalles del Código Postal

```sh
[GET] http://localhost:8000/api/v1/codes/<código-postal>

```

Reemplaza <código-postal> con un número de 5 dígitos. Si hay una coincidencia en la base de datos, se devuelven los detalles del código postal ingresado.

## Lecciones Aprendidas

- Una arquitectura de base de datos bien estructurada ahorra código al momento de consultar códigos postales.
- La carga inicial, originalmente un script en Python ejecutado con `docker compose exec my-django python load_seeds.py`, pero se cambió a un enfoque asíncrono que llama a Celery para realizar esta chamba.
- En la búsqueda de la optimización, se agregó Redis para evitar consultas a MySQL por cada solicitud repetida.

Pendiente

- Pruebas E2E
- Implementar el despliegue mediante integración continua hacia un servidor.
- Crear un `beat` en Celery (tarea periódica) para que diariamente, a las 23:59, descargue el archivo de códigos - postales, lo compare con el actual y, en caso de haber alguna diferencia, inserte las nuevas modificaciones en la base de datos.
- Proteger los endpoints con una API KEY.
- Expirar Redis cada vez que se detecten nuevas inserciones en la base de datos desde el `beat``.
- Tener una variable `BOOL` en DB que indique si el proceso de cargado se encuentra ejecutandose para evitar procesos innecesarios.
