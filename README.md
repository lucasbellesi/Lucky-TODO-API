# API REST de ToDo (Lista de tareas)

## Resumen

Backend para una aplicación de lista de tareas. Permite registrar usuarios, autenticarse con JWT y gestionar tareas personales (crear, listar, actualizar y eliminar). Pensada para ejecutarse localmente y/o integrarse con un frontend.

## Base URL

```
# Desarrollo local
http://localhost:8000
```

La especificación OpenAPI de referencia está en `docs/todo-openapi.yaml`. La documentación interactiva del servidor corre en `http://localhost:8000/docs` (Swagger UI).

## Autenticación

- Autenticación mediante JWT Bearer.
- Rutas públicas: `POST /auth/register`, `POST /auth/login`.
- El resto de rutas requieren `Authorization: Bearer <token>`.

## Endpoints

### Autenticación

- POST `/auth/register`
  - Cuerpo JSON:
    ```json
    { "email": "string", "password": "string", "username": "string" }
    ```
  - Respuestas: `201 Created` con el usuario creado. Puede incluir cabecera `Location` informativa.

- POST `/auth/login`
  - Content-Type: `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm)
  - Campos del body:
    - `username`: email del usuario
    - `password`: contraseña
  - `200 OK` con:
    ```json
    { "accessToken": "jwt...", "refreshToken": "jwt...", "expiresIn": 1800 }
    ```

### Tareas

- GET `/tasks`
  - Query params soportados: `status`, `priority`, `limit`, `offset`
  - `status`: `pending | completed`
  - `priority`: `low | medium | high`
  - `200 OK` con `{ tasks: [...], pagination: { total, limit, offset } }`

- POST `/tasks`
  - Requiere `Authorization: Bearer <token>`
  - Cuerpo JSON (campos opcionales salvo `title`):
    ```json
    { "title": "string", "description": "string", "dueDate": "2025-12-31T23:59:59Z", "priority": "medium", "categoryId": "<uuid>" }
    ```
  - `201 Created` con la tarea creada

- GET `/tasks/{id}`
  - `200 OK` con la tarea

- PUT `/tasks/{id}`
  - Actualiza la tarea (esta implementación acepta actualización parcial vía `PUT`).
  - `200 OK` con la tarea actualizada

- PATCH `/tasks/{id}/complete`
  - Marca la tarea como completada.
  - `200 OK` con la tarea actualizada

- DELETE `/tasks/{id}`
  - `204 No Content`

### Categorías

- POST `/categories/` (sin autenticación)
  - ```json
    { "name": "string", "color": "#rrggbb" }
    ```
  - `201 Created`

- GET `/categories/` (sin autenticación)
  - `200 OK` con la lista de categorías

## Códigos HTTP

- 200 OK — Operación exitosa
- 201 Created — Recurso creado
- 204 No Content — Eliminación exitosa
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error

## Estado y características

- Paginación: `limit` y `offset` en listados.
- Validación: Esquemas Pydantic para entradas/salidas.
- Errores: Respuesta consistente con `error`, `timestamp`, `path`.
- No implementado (aún): búsqueda por texto, ordenamiento, rate limiting.

## Cómo usar la API (curl)

Usando `http://localhost:8000`:

```bash
# 1) Registrar usuario
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"password123","username":"alice"}'

# 2) Login (form-encoded). username = email
ACCESS_TOKEN=$(\
  curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=alice@example.com&password=password123" \
  | python -c "import sys,json; print(json.load(sys.stdin)['accessToken'])" \
)
echo "TOKEN=$ACCESS_TOKEN"

# 3) Crear categoría (no requiere auth)
curl -s -X POST http://localhost:8000/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Work","color":"#ff0000"}'

# 4) Listar categorías
curl -s http://localhost:8000/categories/

# 5) Crear tarea
curl -s -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "title":"Complete API documentation",
        "description":"Write OpenAPI spec for Todo API",
        "dueDate":"2025-12-31T23:59:59Z",
        "priority":"medium"
      }'

# 6) Listar tareas con paginación y filtros
curl -s "http://localhost:8000/tasks/?limit=20&offset=0&status=pending&priority=medium" \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 7) Obtener tarea por id
TASK_ID="<uuid>"
curl -s http://localhost:8000/tasks/$TASK_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 8) Marcar tarea como completa
curl -s -X PATCH http://localhost:8000/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 9) Eliminar tarea
curl -s -X DELETE http://localhost:8000/tasks/$TASK_ID \
  -H "Authorization: Bearer $ACCESS_TOKEN" -i
```

## Ejecutar el servidor (dev)

- Requisitos: Python 3.11+, `pip`.

1) Instalar dependencias

```
python -m pip install -r python_api/requirements.txt
```

2) Variables de entorno (crear `python_api/.env`)

```
SECRET_KEY=change-me
# DATABASE_URL=sqlite:///./todo.db   # por defecto usa SQLite local
# ACCESS_TOKEN_EXPIRE_MINUTES=30     # por defecto 30 minutos
```

3) Levantar el servidor

```
uvicorn python_api.main:app --reload --host 0.0.0.0 --port 8000
```

Luego abre `http://localhost:8000/docs`.

## CORS

Se permiten orígenes `http://localhost:5173` y `http://127.0.0.1:5173` por defecto (ajustable en `python_api/main.py`).

## Ejecutar tests

```
python -m pytest -q
```

## Notas de implementación

- SQLAlchemy + SQLite por defecto (archivo `todo.db`).
- Migraciones no incluidas; el esquema se crea al iniciar la app.
- Estructura por routers: `auth`, `tasks`, `categories`.

