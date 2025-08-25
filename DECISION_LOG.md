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
- **app/**: Código fuente principal
  - **main.py**: Punto de entrada de la app
  - **config.py**: Configuración general
  - **domain/**: Lógica de negocio y repositorios
  - **graphql/**: Esquemas y resolvers GraphQL
  - **infrastructure/**: Integraciones externas (auth, db, email)
- **tests/**: Pruebas automatizadas
- **Makefile**: Comandos para gestión de infraestructura con Docker Compose
- **pyproject.toml**: Dependencias y configuración de Python

---

## 3. ✅ Tipos GraphQL separados por entidad

**Decisión:** Crear tipos GraphQL separados en `graphql/types/`, uno por entidad.

**Motivación:**
- Mejora la organización de los tipos.
- Facilita el acceso desde los resolvers mediante imports explícitos.
- Permite escalar a más entidades sin perder claridad.

---

## 4. ✅ Estructura del proyecto orientada a Clean Architecture

**Decisión:** Organizar el código en carpetas: `domain/`, `infrastructure/`, `graphql/`.

**Motivación:**
- Facilitar la separación de responsabilidades (SRP).
- Alinear con patrones como Clean Architecture o Hexagonal.
- Favorecer testeo, escalabilidad y claridad de propósito por capa.

---

## 5. ✅ Uso de SQLModel como ORM

**Decisión:** Utilizar `sqlmodel` en lugar de SQLAlchemy directamente.

**Motivación:**
- Combina lo mejor de Pydantic y SQLAlchemy.
- Más simple para leer, tipar y validar datos.
- Integración directa con FastAPI.
- Ideal para un proyecto de tamaño medio como este.

---

## 6. ✅ Estrategia de testing y estructura

**Decisión:** Ubicar los tests fuera de `app/`, en una carpeta raíz `tests/`, usando `pytest`.

**Motivación:**
- Es la estructura recomendada por pytest y comunidad Python.
- Permite un entorno de producción limpio.
- Facilita cobertura por tipo de test (unitario, integración, GraphQL).

---

## 7. ✅ Linting y formateo

**Decisión:** Usar:
- `black` para formateo
- `isort` para orden de imports
- `flake8` y `ruff` para linting

**Motivación:**
- Cumplir con los requisitos de la prueba.
- Seguir convenciones populares y compatibles.
- `ruff` permite ejecución rápida y múltiples reglas en un solo chequeo.

---

## 8. ✅ Uso de `uv` como gestor de paquetes

**Decisión:** Gestionar dependencias y entorno virtual con `uv`.

**Motivación:**
- Es ultrarrápido y moderno.
- Facilita mantener `pyproject.toml` como único punto de configuración.
- Mejora tiempos de instalación y gestión del entorno virtual.

---

## 9. ✅ Manejo de autenticación con JWT

**Decisión:** Implementar autenticación con tokens JWT usando un servicio propio (`jwt_service.py`), protegido por permisos en GraphQL.

**Motivación:**
- Es una práctica común y escalable en APIs modernas.
- Permite proteger resolvers GraphQL con `@strawberry.permission`.
- El token incluye el `id`, `username` como identificador del usuario.
- Fácil de probar e integrar con clientes externos.

---

## 10. ✅ Hashing de contraseñas con `passlib`

**Decisión:** Usar `passlib` y el algoritmo `bcrypt` para almacenar contraseñas de forma segura.

**Motivación:**
- Evita guardar contraseñas en texto plano.
- `passlib` es una librería robusta y ampliamente adoptada.
- Compatible con verificación posterior (`verify_password`) y hashing (`hash_password`) al registrar o loguear un usuario.

---

## 11. ✅ Protecciones con permisos personalizados

**Decisión:** Implementar permisos en Strawberry con `IsAuthenticated` usando `@strawberry.permission`.

**Motivación:**
- Permite proteger resolvers sensibles como `me`, `users`, etc.
- Utiliza el token JWT enviado en el header `Authorization`.
- Permite extender fácilmente a permisos más específicos (`IsAdmin`, etc.).

---

## 12. ✅ Testing de GraphQL con JWT

**Decisión:** Incluir tests para resolvers protegidos (`me`) usando autenticación real con JWT emitido en `login`.

**Motivación:**
- Asegura la validez del flujo completo: login → token → autorización → acceso a datos.
- Permite detectar fallas de seguridad o integración.
- Refuerza el enfoque "end-to-end" sobre resolvers críticos.

---

## 13. ✅ Gestión de infraestructura con Docker Compose

**Decisión:** Usar Docker Compose para levantar todos los servicios del proyecto (FastAPI, Mailhog) de forma reproducible.

**Motivación:**
- Evita instalaciones manuales y dependencias en la máquina del desarrollador.
- Permite correr toda la aplicación (API, correo, red interna) con un solo comando (`make up`).
- Facilita el uso en CI/CD y la colaboración en equipo.

**Implementación:**
- `docker-compose.yml` define:
  - **fastapi_app**: Contenedor principal con FastAPI.
  - **mailhog**: Servidor SMTP para pruebas de correo.
  - **app_network**: Red interna para comunicación entre contenedores.
- `Makefile` encapsula comandos comunes (`up`, `down`, `logs`, `clean`).

---

## 14. ✅ Limpieza y reinicio del entorno con Makefile

**Decisión:** Agregar comandos `make clean` y `make restart` para simplificar el manejo del entorno Docker.

**Motivación:**
- Permite reiniciar la infraestructura sin residuos.
- Mejora la experiencia del desarrollador y reduce fricciones.

---

## 15. ✅ Envío de notificación de inicio de sesión por correo con Mailhog

**Decisión:** Utilizar Mailhog como servidor SMTP local para capturar y verificar correos durante el desarrollo. El correo se enviará como una notificación de inicio de sesión exitosa.

**Motivación:**
- Mailhog permite ver correos sin necesidad de servicios externos.
- Ideal para ambientes de desarrollo y pruebas.
- Permite testear contenido, estructura y disparadores de correos.

**Implementación:**
- Se utiliza `FastAPI` + `email.message.EmailMessage` + `smtplib`.
- El servicio de envío se encapsula dentro de `infrastructure/email/mailer.py`.
- Se activa después de una autenticación exitosa (`login`).

---

## 16. ✅ Envío de correos en segundo plano con BackgroundTasks

**Decisión:** Utilizar `BackgroundTasks` de FastAPI para ejecutar el envío del correo de notificación en segundo plano.

**Motivación:**
- Evita bloquear la respuesta de la mutación `login`.
- Mejora la experiencia del usuario.
- Integración directa con Strawberry pasando `background_tasks` por el `context`.

---

## 17. ✅ Uso de variables de entorno para configuración

**Decisión:** Centralizar la configuración sensible y contextual del proyecto utilizando variables de entorno, gestionadas mediante `pydantic.BaseSettings`.

**Motivación:**
- Evita hardcodear valores sensibles.
- Facilita portabilidad entre entornos.
- Integración natural con Docker Compose y CI/CD.
- Mejora seguridad y mantenibilidad.

**Variables empleadas:**
- `SMTP_HOST`, `SMTP_PORT`, `FROM_EMAIL`: Configuración del servidor SMTP.
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`: Configuración JWT.
- `DEBUG_DB`: Activación de debug en base de datos.

**Extras:**
- `.env.example` incluido.
- Tests configuran las variables necesarias internamente.
