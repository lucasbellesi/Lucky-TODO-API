# REST API for ToDo List Application

## Overview

This API is designed to serve as the backend for a ToDo List Web Application. It allows users to register, authenticate, and manage their personal tasks efficiently. The API can be deployed locally on a personal computer, making it ideal for individual use, development, or self-hosted deployments. By integrating this API with a frontend web app, users can create, update, organize, and track their tasks securely and conveniently from their own environment.

## Base Endpoints

```
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
  - Returns `201 Created` with location header
  - Response body:
    ```json
    {
      "id": "string",
      "username": "string",
      "email": "string"
    }
    ```

- **POST /auth/login**
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
  - Returns `200 OK` with:
    ```json
    {
      "token": "string",
      "expiresIn": 3600
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

## Example Requests

```bash
# Create task
curl -X POST https://api.todoapp.com/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -d '{"title":"Buy milk","description":"Skim milk","dueDate":"2023-12-31","priority":"medium"}'

# Update task status
curl -X PATCH https://api.todoapp.com/v1/tasks/123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -d '{"status":"completed"}'
```

## Implementation Notes

1. **Production Ready**: Designed for scalability and maintainability
2. **Consistent Patterns**: Uniform approach across all endpoints
3. **Flexible**: Optional features can be implemented as needed
4. **Secure**: Robust authentication and input validation
5. **Well-Documented**: Clear specifications for easy integration