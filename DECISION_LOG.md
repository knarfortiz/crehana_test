# 🧠 Decision Log – Prueba Técnica Backend (GraphQL + FastAPI)

Este documento registra las decisiones técnicas clave tomadas durante el desarrollo de la prueba técnica. El objetivo es dejar evidencia clara y razonada de cada elección, priorizando buenas prácticas, mantenibilidad y alineación con los requisitos del desafío.

---

## 1. ✅ Uso de FastAPI + Strawberry GraphQL

**Decisión:** Utilizar `Strawberry` como librería de GraphQL sobre `FastAPI`.

**Motivación:**
- Strawberry tiene una integración oficial y limpia con FastAPI.
- Permite aprovechar decoradores tipo `@strawberry.type`, similares a dataclasses.
- Soporta GraphQL moderno con tipado fuerte.
- Muy buena documentación y comunidad activa.

**Alternativas consideradas:** Graphene (más antiguo, pero menos actualizado).

---

## 2. ✅ Modularización de queries y mutations por entidad

**Decisión:** Separar las queries y mutations por entidad (`Task`, `User`, etc.), y luego unificarlas en `query.py` y `mutation.py`.

**Motivación:**
- Permite mantener cada entidad desacoplada.
- Facilita el mantenimiento y la escalabilidad del schema.
- Evita archivos monolíticos difíciles de navegar.
- Evita el uso incorrecto de `__init__.py` para lógica de composición.

**Estructura:**
<br>graphql/
<br>├── queries/
<br>│ ├── task.py
<br>│ └── user.py
<br>├── mutations/
<br>│ ├── task.py
<br>│ └── user.py
<br>├── query.py
<br>├── mutation.py
<br>└── schema.py
<br>└── permissions.py PENDIENTE


---

## 3. ✅ Tipos GraphQL separados por entidad

**Decisión:** Crear tipos GraphQL separados en `graphql/types/`, uno por entidad, y exponerlos desde `__init__.py`.

**Motivación:**
- Mejora la organización de los tipos.
- Facilita el acceso desde los resolvers (`from app.graphql.types import TaskType`).
- Permite escalar a más entidades sin perder claridad.

---

## 4. ✅ Evitar lógica en `__init__.py`

**Decisión:** No usar `__init__.py` para componer clases (`Query`, `Mutation`, etc.), y limitar su uso a exposición de tipos u objetos.

**Motivación:**
- Seguir buenas prácticas de Python.
- Prevenir errores de imports circulares.
- Mejorar el descubrimiento de código por parte de otros desarrolladores.

---

## 5. ✅ Estructura del proyecto orientada a Clean Architecture

**Decisión:** Organizar el código en carpetas: `domain/`, `application/`, `infrastructure/`, `graphql/`.

**Motivación:**
- Facilitar la separación de responsabilidades (SRP).
- Alinear con patrones como Clean Architecture o Hexagonal.
- Favorecer testeo, escalabilidad y claridad de propósito por capa.

---

## 6. ✅ Uso de SQLModel como ORM

**Decisión:** Utilizar `sqlmodel` en lugar de SQLAlchemy directamente.

**Motivación:**
- Combina lo mejor de Pydantic y SQLAlchemy.
- Más simple para leer, tipar y validar datos.
- Integración directa con FastAPI.
- Ideal para un proyecto de tamaño medio como este.

---

## 7. ✅ Estrategia de testing y estructura

**Decisión:** Ubicar los tests fuera de `app/`, en una carpeta raíz `tests/`, usando `pytest`.

**Motivación:**
- Es la estructura recomendada por pytest y comunidad Python.
- Permite un entorno de producción limpio.
- Facilita cobertura por tipo de test (unitario, integración, GraphQL).

---

## 8. ✅ Linting y formateo

**Decisión:** Usar:
- `black` para formateo
- `isort` para orden de imports
- `flake8` y `ruff` para linting

**Motivación:**
- Cumplir con los requisitos de la prueba.
- Seguir convenciones populares y compatibles.
- `ruff` permite ejecución rápida y múltiples reglas en un solo chequeo.

---

## 9. ✅ Uso de `uv` como gestor de paquetes

**Decisión:** Gestionar dependencias y entorno virtual con `uv`.

**Motivación:**
- Es ultrarrápido y moderno.
- Facilita mantener `pyproject.toml` como único punto de configuración.
- Mejora tiempos de instalación y gestión del entorno virtual.

---

