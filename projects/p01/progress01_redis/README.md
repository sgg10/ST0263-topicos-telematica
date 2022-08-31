# ST0263 Tópicos Especiales en Telemática | Avance 1 del proyecto 1

## Tabla de contenidos
1. [Estudiantes](#estudiantes)
2. [Profesor](#profesor)
3. [Nombre de la actividad](#nombre)
4. [Descripción](#descripcion)
5. [Información general](#info)
6. [Ambiente de desarrollo](#dev)
7. [Ambiente productivo](#prod)
8. [Referencias](#ref)


## Estudiantes: <a name="estudiantes"/>

- Pascual Gómez: pgomezl@eafit.edu.co
- Sebastian Granda: sgrandag@eafit.edu.co

## Profesor: <a name="profesor"/>

- Edwin Nelson Montoya Munera: emontoya@eafit.edu.co


# URR (User's Redmes on Redis) <a name="nombre"/>

## Descripción de la actividad <a name="descripcion"/>

Este proyecto consiste en una API que permite realizar operaciones CRUD para el manejo de usuarios (este CRUD se estaria gestionanado a traves de Redis). Los usuarios podran solicitar un README sencillo que sera sera renderizado segun el orden de llegada con un tiempo aleatorio entre 30 a 60 segundos, esto con el objetivo de mostar la implementación de PubSub en Redis.


## Información General <a name="info"/>

Este proyecto se diseño como una API que contiene 2 divisiones:
- Usuarios: para gestionar el CRUD de los usuarios que se deesen ingresar a la plataforma
- Readme: espacio donde un usuario registrado puede solicitar la creación de su readme y este sera procesado segun la disponinilidad o cantidad de mensajes que se tengan pendientes por procesar.

Cada uno de los endpoint correspondientes se encuentra documentado y cuenta con su entorno para ser ejecutado de manera directa, esto haciendo uso de OPENAPI para tener esta docuemntación.

## Ambiente de desarrollo <a name="dev">

- Desarrollado en Python con FastAPI
- Librerias:
  - redis==4.3.4
  - uvicorn==0.18.2
  - Jinja2==3.1.2
  - fastapi==0.79.1

### ¿Como se ejecuta?

Antes de ejecutar es necesario contar con Docker Compose y Python instalados, se deben instalar las dependencias alojadas en el archivo `requirements.txt` o `Pipfile`(se recomiendo el uso de `pipenv` para facilitar el manejo de entornos virtuales)

- Ejecutar `docker-compose up` o `docker compose up` (segun la versión) para levantar el cluster de Redis de manera sencilla
- Ejecutar en otra terminal el comando `uvicorn app.main:app --reload` para ejecutar el proyecto y tener acceso a la API

### Estructura de directorios
```
.
├── app
│   ├── cruds
│   │   ├── __init__.py
│   │   └── users.py
│   ├── exceptions.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── users.py
│   ├── redis.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── readmes.py
│   │   └── users.py
│   └── workers
│       ├── html_generator
│       │   ├── __init__.py
│       │   └── suscriber.py
│       └── __init__.py
├── docker-compose.yml
├── Pipfile
├── Pipfile.lock
├── README.md
├── README__.md
└── requirements.txt
```

## Ambiente productivo <a name="prod">

- Desarrollado en Python con FastAPI
- Librerias:
  - redis==4.3.4
  - uvicorn==0.18.2
  - Jinja2==3.1.2
  - fastapi==0.79.1
- Herramientas:
  - Supervisor

### ¿Como se ejecuta?
No es necesario levantar nada, ya que gracias a la herramienta de Supervisor se levanta todo el proyecto de manera automatica, esto ayuda a tomar el proyecto como un servicio, el cual se reiniciara en caso tal de que llegara a fallar para garantizar que va a estar disponible.

Sin embargo, la forma de ejecutarlo de manera manual es muy similar al entorno de desarrollo

- Ejecutar `docker-compose up` o `docker compose up` (segun la versión) para levantar el cluster de Redis de manera sencilla
- Ejecutar en otra terminal el comando `uvicorn app.main:app --host 0.0.0.0 --port 8888` para ejecutar el proyecto y tener acceso a la API

La razon por la cual la API no se levanta en conjunto al cluster dentro del mismo docker compose es debido a que el proyecto necesitaba configuraciones adicionales para esto y por cuestiones de tiempo no se vio viable aplicar estar configuraciones. Sin embargo, se soluciona el levantamiento de manera autonoma con supervisor.

## Referencias <a name="ref"/>

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [Redis](https://redis.io/)