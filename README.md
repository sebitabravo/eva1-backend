# Proyecto de Backend - API para Empresa de Venta de Maderas

Este proyecto es una API RESTful desarrollada con Django REST Framework para la empresa ficticia "Maderas del Sur S.A.". La API permite gestionar la flota de camiones, conductores, tipos de madera, cargas y clientes, optimizando la logística de transporte de madera.

## Tecnologías Utilizadas

- Python
- Django
- Django REST Framework
- SQLite3

## Requisitos de Instalación

1. **Clonar el repositorio**:

```bash
git clone https://github.com/sebitabravo/maderaapi.git
cd maderaapi
```

2. **Crear y activar el entorno virtual:**:

```bash
python -m venv eva1
source eva1/bin/activate  # En Windows: eva1\Scripts\activate
```

3. **Instalar las dependencias**:

```bash
pip install -r requirements.txt
```

4. **Migrar la base de datos:**:

```bash
python manage.py migrate
```

5. **Crear un superusuario (opcional para acceder al admin de Django):**:

```bash
python manage.py createsuperuser
```

6. **Correr el servidor:**:

```bash
python manage.py runserver
```

## Características del Proyecto

### Autenticación

El sistema cuenta con autenticación básica para acceder al administrador de la API:

- **Usuario**: `backend`
- **Contraseña**: `backend`

### Modelo de Base de Datos

La base de datos está modelada para representar la flota de camiones, sus conductores, las cargas y los clientes, usando las siguientes entidades:

1. **Camión**:

   - ID
   - Placa
   - Modelo
   - Capacidad de Carga

2. **Conductor**:

   - ID
   - Nombre
   - Licencia de Conducir
   - Teléfono

3. **Carga**:

   - ID
   - Tipo de Madera
   - Cantidad
   - Peso
   - Cliente

4. **Cliente**:

   - ID
   - Nombre de la Empresa
   - Dirección
   - Teléfono
   - Correo Electrónico

5. **Tipo de Madera**:
   - ID
   - Nombre
   - Descripción

### Funcionalidades CRUD

La API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) en las siguientes entidades:

- **Camión**
- **Conductor**
- **Carga**
- **Cliente**
- **Tipo de Madera**

### Rutas de la API

- `/camiones/`: Para gestionar camiones.
- `/conductores/`: Para gestionar conductores.
- `/cargas/`: Para gestionar cargas.
- `/clientes/`: Para gestionar clientes.
- `/tipos-madera/`: Para gestionar tipos de madera.

### Ejemplos de Uso

#### Listar Camiones

```bash
GET /camiones/
```

#### Crear un Camión

```bash
POST /camiones/
{
  "placa": "ABC123",
  "modelo": "Ford F-150",
  "capacidad_carga": 5.5,
  "conductor": 1
}
```

## Licencia

Este proyecto fue desarrollado como parte de una evaluación de backend para la Universidad Tecnológica de Chile INACAP. Todos los derechos reservados para dicha institución.

Para más información, visita [INACAP](https://portal.inacap.cl).
