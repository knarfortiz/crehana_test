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
  - **config.py**: Configuración general
  - **domain/**: Lógica de negocio y repositorios
  - **graphql/**: Esquemas y resolvers GraphQL
  - **infrastructure/**: Integraciones externas (auth, db, email)
- **tests/**: Pruebas automatizadas
- **Makefile**: Comandos para gestión de infraestructura con Terraform (usando Docker)
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

**Decisión:** Organizar el código en carpetas: `domain/`, `application/`, `infrastructure/`, `graphql/`.

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
- El token incluye el `sub` como identificador del usuario.
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

## 13. ✅ Gestión de infraestructura con Makefile + Terraform + Docker

**Decisión:** Usar un `Makefile` que encapsula comandos de Terraform dentro de contenedores Docker.

**Motivación:**
- Evita depender de instalaciones locales de Terraform.
- Reproducible y portable en cualquier sistema con Docker.
- Mejora la DX al reducir errores por versiones o configuración local.

---

## 14. ✅ Uso de `terraform plan -out` para despliegues controlados

**Decisión:** Utilizar `terraform plan -out=plan.tfplan` y `terraform apply plan.tfplan` para garantizar consistencia.

**Motivación:**
- Asegura que el plan ejecutado sea exactamente el que se revisó.
- Elimina advertencias innecesarias al aplicar.
- Buena práctica especialmente útil para ambientes productivos o CI/CD.

---

## 15. ✅ Limpieza del entorno con `make clean`

**Decisión:** Agregar el comando `make clean` para eliminar archivos temporales como `plan.tfplan`.

**Motivación:**
- Evita archivos residuales en el repo o directorio de trabajo.
- Mejora la higiene del entorno local.
- Facilita reiniciar despliegues sin residuos del anterior.

---
## 16. ✅ Envío de notificación de inicio de sesión por correo con Mailhog

**Decisión:** Utilizar Mailhog como servidor SMTP local para capturar y verificar correos durante el desarrollo. El correo se enviará como una notificación de inicio de sesión exitosa.

**Motivación:**
- Mailhog permite ver correos sin necesidad de servicios externos (Gmail, Mailgun, etc.).
- Ideal para ambientes de desarrollo y pruebas.
- Permite testear contenido, estructura y disparadores de correos.
- Mejora la experiencia del usuario al recibir confirmación de acceso.

**Implementación:**
- Se utiliza `FastAPI` + `email.message.EmailMessage` + `smtplib`.
- El servicio de envío se encapsula dentro de `infrastructure/email/mailer.py`.
- Se activa después de una autenticación exitosa (`login`).