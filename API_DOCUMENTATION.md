# Documentación de la API - Maderas del Sur S.A.

## 🌐 Endpoints Principales

Base URL: `http://localhost:8000/api/`

## 🔐 Autenticación

La API usa autenticación por token. Para obtener un token:

**POST** `/api/auth/token/`

```json
{
  "username": "tu_usuario",
  "password": "tu_password"
}
```

**Respuesta:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Incluye el token en el header de tus requests:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## 👨‍✈️ Conductores

### Listar conductores
**GET** `/api/conductores/`

**Query params:**
- `search`: Buscar por nombre, licencia o teléfono
- `ordering`: Ordenar por `nombre`, `created_at`

### Crear conductor
**POST** `/api/conductores/`

```json
{
  "nombre": "Juan Pérez",
  "licencia_conducir": "A12345678",
  "telefono": "+56912345678",
  "direccion": "Av. Principal 123, Santiago"
}
```

### Obtener conductor específico
**GET** `/api/conductores/{id}/`

### Actualizar conductor
**PUT** `/api/conductores/{id}/`
**PATCH** `/api/conductores/{id}/`

### Eliminar conductor
**DELETE** `/api/conductores/{id}/`

### Obtener camiones de un conductor
**GET** `/api/conductores/{id}/camiones/`

---

## 🚛 Camiones

### Listar camiones
**GET** `/api/camiones/`

**Query params:**
- `search`: Buscar por placa, modelo o nombre del conductor
- `conductor`: Filtrar por ID del conductor
- `ordering`: Ordenar por `placa`, `capacidad_carga`, `created_at`

### Crear camión
**POST** `/api/camiones/`

```json
{
  "placa": "ABC1234",
  "modelo": "Ford F-150",
  "capacidad_carga": 5.5,
  "conductor": 1
}
```

**Validaciones:**
- Placa debe tener formato válido (ej: ABC1234)
- Capacidad de carga debe ser mayor a 0

### Obtener camión específico
**GET** `/api/camiones/{id}/`

Retorna información detallada incluyendo datos del conductor.

### Obtener cargas de un camión
**GET** `/api/camiones/{id}/cargas/`

### Obtener estadísticas de un camión
**GET** `/api/camiones/{id}/estadisticas/`

**Respuesta:**
```json
{
  "camion": {...},
  "estadisticas": {
    "total_cargas": 15,
    "peso_total": 75.5
  }
}
```

---

## 🌲 Tipos de Madera

### Listar tipos de madera
**GET** `/api/tipos-madera/`

**Query params:**
- `search`: Buscar por nombre o descripción
- `ordering`: Ordenar por `nombre`, `created_at`

### Crear tipo de madera
**POST** `/api/tipos-madera/`

```json
{
  "nombre": "Pino Radiata",
  "descripcion": "Madera de pino de crecimiento rápido, ideal para construcción"
}
```

### Obtener cargas por tipo de madera
**GET** `/api/tipos-madera/{id}/cargas/`

---

## 🏢 Clientes

### Listar clientes
**GET** `/api/clientes/`

**Query params:**
- `search`: Buscar por nombre de empresa, correo o teléfono
- `ordering`: Ordenar por `nombre_empresa`, `created_at`

### Crear cliente
**POST** `/api/clientes/`

```json
{
  "nombre_empresa": "Constructora Los Andes S.A.",
  "direccion": "Av. Las Condes 123, Santiago",
  "telefono": "+56987654321",
  "correo_electronico": "contacto@losandes.cl"
}
```

**Validaciones:**
- Correo electrónico debe ser único y válido
- Teléfono debe tener formato válido

### Obtener estadísticas de un cliente
**GET** `/api/clientes/{id}/estadisticas/`

**Respuesta:**
```json
{
  "cliente": {...},
  "estadisticas": {
    "total_cargas": 25,
    "peso_total": 125.5,
    "cantidad_total": 500
  }
}
```

---

## 📦 Cargas

### Listar cargas
**GET** `/api/cargas/`

**Query params:**
- `search`: Buscar por tipo de madera, placa del camión o nombre del cliente
- `tipo_madera`: Filtrar por ID del tipo de madera
- `camion`: Filtrar por ID del camión
- `cliente`: Filtrar por ID del cliente
- `ordering`: Ordenar por `created_at`, `peso`, `cantidad`

### Crear carga
**POST** `/api/cargas/`

```json
{
  "tipo_madera": 1,
  "cantidad": 100,
  "peso": 5.5,
  "camion": 1,
  "cliente": 1
}
```

**Validaciones:**
- El peso de la carga NO puede exceder la capacidad del camión
- Cantidad y peso deben ser mayores a 0

### Obtener carga específica
**GET** `/api/cargas/{id}/`

Retorna información detallada con datos completos de relaciones.

### Estadísticas generales
**GET** `/api/cargas/estadisticas_generales/`

**Respuesta:**
```json
{
  "total_cargas": 150,
  "peso_total": 750.5,
  "cantidad_total": 15000
}
```

---

## 📊 Respuestas de la API

### Respuesta exitosa (200 OK)
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "created_at": "2024-10-01T12:00:00Z",
  ...
}
```

### Lista paginada (200 OK)
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/camiones/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error de validación (400 Bad Request)
```json
{
  "peso": [
    "El peso de la carga (10t) excede la capacidad del camión (5.5t)."
  ]
}
```

### No autorizado (401 Unauthorized)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### No encontrado (404 Not Found)
```json
{
  "detail": "Not found."
}
```

---

## 🔍 Búsqueda y Filtrado

### Búsqueda
Usa el parámetro `search`:
```
GET /api/camiones/?search=ford
```

### Filtros
Usa el nombre del campo:
```
GET /api/cargas/?camion=1&tipo_madera=2
```

### Ordenamiento
Usa el parámetro `ordering`:
```
GET /api/clientes/?ordering=-created_at
```

Usa `-` para orden descendente.

---

## 📝 Campos Comunes

Todos los modelos incluyen:
- `id`: ID único del registro
- `created_at`: Fecha y hora de creación
- `updated_at`: Fecha y hora de última actualización

---

## 🛠️ Herramientas Útiles

### Browsable API
Django REST Framework proporciona una interfaz web navegable. Accede desde tu navegador a cualquier endpoint para explorar la API interactivamente.

### Admin Panel
Accede al panel de administración de Django en:
```
http://localhost:8000/admin/
```

---

## 💡 Ejemplos con cURL

### Obtener token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Listar camiones (autenticado)
```bash
curl -H "Authorization: Token tu_token_aqui" \
  http://localhost:8000/api/camiones/
```

### Crear una carga
```bash
curl -X POST http://localhost:8000/api/cargas/ \
  -H "Authorization: Token tu_token_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_madera": 1,
    "cantidad": 100,
    "peso": 4.5,
    "camion": 1,
    "cliente": 1
  }'
```

---

## 📞 Soporte

Para más información o ayuda, contacta al equipo de desarrollo.
