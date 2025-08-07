# Crehana Test Project

Este proyecto es una API construida con FastAPI y SQLModel, diseñada para gestionar listas de tareas y tareas individuales, siguiendo buenas prácticas de arquitectura, testing y despliegue.

## Propósito del Proyecto

Este proyecto corresponde a una prueba técnica para el rol de Desarrollador Backend (Python), como parte del proceso de evaluación técnica para la vacante en Crehana.

El objetivo de esta evaluación es construir una API RESTful para un sistema de gestión de tareas, evaluando las siguientes capacidades:

- Diseñar e implementar una API limpia y mantenible.
- Trabajar con Python y frameworks backend modernos.
- Implementar validaciones, autenticación y buenas prácticas.
- Escribir pruebas automatizadas.
- Documentar código, endpoints y decisiones técnicas.

## Estructura del Proyecto

- **app/**: Código fuente principal
  - **main.py**: Punto de entrada de la app
  - **config.py**: Configuración general
  - **domain/**: Lógica de negocio y repositorios
  - **graphql/**: Esquemas y resolvers GraphQL
  - **infrastructure/**: Integraciones externas (auth, db, email)
- **tests/**: Pruebas automatizadas
- **Makefile**: Comandos para gestión de infraestructura con Terraform (usando Docker)
- **pyproject.toml**: Dependencias y configuración de Python

## Requisitos

- Docker
- Make
- uv (administrador de paquetes Python)

## Instalación y Despliegue

La gestión de la infraestructura y el despliegue se realiza mediante el `Makefile`, que utiliza Docker y Terraform de forma transparente.

### Comandos principales

- Inicializar Terraform:
  ```sh
  make init
  ```
- Validar archivos de infraestructura:
  ```sh
  make validate
  ```
- Planificar cambios de infraestructura:
  ```sh
  make plan
  ```
- Aplicar cambios (desplegar):
  ```sh
  make apply
  ```
- Destruir infraestructura:
  ```sh
  make destroy
  ```
- Limpiar archivos temporales:
  ```sh
  make clean
  ```
- Ver ayuda de comandos disponibles:
  ```sh
  make help
  ```

## Instalación de uv

Para instalar el administrador de paquetes `uv`:

- **Mac y Linux:**
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

## Uso

1. Clona el repositorio y navega al directorio del proyecto.
2. Usa los comandos del `Makefile` para gestionar la infraestructura.
3. Accede a la documentación interactiva en http://127.0.0.1:8000/docs
4. Accede a la documentación interactiva en http://127.0.0.1:8000/graphql
5. Accede a MailHog http://localhost:8025, para validar el correo de inicio de login

## Dependencias principales

- FastAPI
- SQLModel
- Strawberry GraphQL
- Docker
- Terraform

## Pruebas

Las pruebas están en `tests/` y pueden ejecutarse con los siguientes comandos usando `uv`:

- Ejecutar los tests y generar el reporte de cobertura:
  ```sh
  uv run coverage run -m pytest
  ```
- Ver el reporte de cobertura:
  ```sh
  uv run coverage report
  ```

## Casos de uso principales

1. CRUD de listas de tareas
2. CRUD de tareas dentro de una lista
3. Cambiar el estado de una tarea
4. Listar tareas con filtros
5. (Bonus) Autenticación JWT, asignación de usuarios, notificación ficticia por email

---
