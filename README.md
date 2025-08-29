# REST API for ToDo List Application

## Overview

This API is designed to serve as the backend for a ToDo List Web Application. It allows users to register, authenticate, and manage their personal tasks efficiently. The API can be deployed locally on a personal computer, making it ideal for individual use, development, or self-hosted deployments. By integrating this API with a frontend web app, users can create, update, organize, and track their tasks securely and conveniently from their own environment.

## Base Endpoints

```
# Local (dev)
http://localhost:8000

# Example public base (docs examples)
https://api.todoapp.com/v1
```

## Authentication

All endpoints (except `/auth/login` and `/auth/register`) require JWT authentication.

## Endpoints

### Authentication

- **POST /auth/register**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
  - Returns `201 Created` with `Location` header
  - Response body:
    ```json
    {
      "id": "string",
      "username": "string",
      "email": "string"
    }
    ```

- **POST /auth/login**
  - Content-Type: `application/x-www-form-urlencoded` (OAuth2PasswordRequestForm)
  - Body fields:
    - `username`: email del usuario
    - `password`: contraseña
  - Returns `200 OK` with:
    ```json
    {
      "accessToken": "jwt...",
      "refreshToken": "jwt...",
      "expiresIn": 1800
    }
    ```

### Tasks

- **GET /tasks**
  - Parameters: `status`, `dueDate`, `priority`, `limit`, `offset`
  - Returns `200 OK` with:
    ```json
    {
      "tasks": [
        {
          "id": "string",
          "title": "string",
          "description": "string",
          "dueDate": "YYYY-MM-DD",
          "priority": "low/medium/high",
          "status": "pending/completed",
          "createdAt": "ISO8601",
          "updatedAt": "ISO8601"
        }
      ],
      "pagination": {
        "total": 100,
        "limit": 10,
        "offset": 0
      }
    }
    ```

- **POST /tasks**
  - Returns `201 Created` with location header
  - Body:
    ```json
    {
      "title": "string",
      "description": "string",
      "dueDate": "YYYY-MM-DD",
      "priority": "low/medium/high"
    }
    ```

- **GET /tasks/{id}**
  - Returns `200 OK` with full task resource

- **PUT /tasks/{id}**
  - Full resource update
  - Returns `200 OK` with updated resource

- **PATCH /tasks/{id}**
  - Partial updates including status changes
  - Example:
    ```json
    {"status": "completed"}
    ```
  - Returns `200 OK` with updated resource

- **DELETE /tasks/{id}**
  - Returns `204 No Content`

### Categories (Optional)

- **GET /categories**
  - Returns `200 OK` with category list

- **POST /categories**
  - Returns `201 Created`
  - Body:
    ```json
    {
      "name": "string",
      "color": "hexColor"
    }
    ```

- **POST /tasks/{id}/categories**
  - Assigns category
  - Returns `204 No Content`

## HTTP Status Codes

- 200 OK - Successful GET/PUT/PATCH
- 201 Created - Resource created
- 204 No Content - Successful DELETE
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error

## Advanced Features

1. **Pagination**: Built-in support via `limit` and `offset`
2. **Search**: Dedicated search endpoint with full-text capabilities
3. **Sorting**: Field-based sorting in all list endpoints
4. **Rate Limiting**: Protection against excessive requests
5. **Comprehensive Validation**: All inputs rigorously validated
6. **Clean Architecture**: Proper separation of concerns
7. **Detailed Documentation**: Complete with examples

## Cómo usar la API (curl)

Ejemplos usando `http://localhost:8000`:

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

# 3) Crear categoría
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
python -m pip install -r python-api/requirements.txt
```

2) Variables de entorno (opcional en dev)

- Crear `python-api/.env` con por lo menos:

```
SECRET_KEY=change-me
# DATABASE_URL=sqlite:///./todo.db   # valor por defecto
```

3) Levantar el servidor

Debido a que el paquete se llama `python-api` (con guion), el nombre de import válido es `python_api`. Para desarrollo rápido, podés usar este comando que crea un alias temporal y lanza Uvicorn:

```
python -c "import types,sys,pathlib;pkg=types.ModuleType('python_api');pkg.__path__=[str(pathlib.Path('python-api').resolve())];sys.modules['python_api']=pkg;import uvicorn;uvicorn.run('python_api.main:app', host='0.0.0.0', port=8000, reload=True)"
```

Luego abrí `http://localhost:8000/docs` para probar.

Sugerencia: a futuro, renombrar `python-api/` a `app/` o `python_api/` para evitar el alias.

## Ejecutar tests

```
python -m pytest -q
```

## Implementation Notes

1. **Production Ready**: Designed for scalability and maintainability
2. **Consistent Patterns**: Uniform approach across all endpoints
3. **Flexible**: Optional features can be implemented as needed
4. **Secure**: Robust authentication and input validation
5. **Well-Documented**: Clear specifications for easy integration

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute it, as long as the original license and copyright notice are included.
