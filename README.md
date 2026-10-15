# FIAshion API - Sistema de Recomendaciones de Moda con Inteligencia Artificial

API REST desarrollada con FastAPI para la gestión de un catálogo de prendas de vestir y la generación de recomendaciones personalizadas mediante Modelos de Lenguaje Grande (LLMs), integrando Google Gemini, persistencia de datos, validación de información, manejo de errores y pruebas de integración.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.12
* **Backend:** FastAPI
* **Base de Datos:** SQLite
* **ORM:** SQLAlchemy
* **Validación de Datos:** Pydantic
* **Inteligencia Artificial:** Google Gemini API
* **Comunicación HTTP:** HTTPX
* **Pruebas:** Pytest y FastAPI TestClient
* **Documentación:** OpenAPI 3.0 / Swagger UI
* **Control de Versiones:** Git y GitHub
* **Integración Continua:** GitHub Actions (CI/CD)

## Objetivo del Proyecto

Desarrollar una API REST que permita administrar productos de una tienda de ropa y generar recomendaciones personalizadas mediante inteligencia artificial, utilizando diferentes técnicas de prompting para seleccionar prendas según las preferencias del cliente.

## Funcionalidades Principales

* **Gestión de Productos (CRUD):** creación, consulta, actualización y eliminación de prendas.
* **Recomendaciones con IA:** selección de prendas según talla, género, categoría y estilo.
* **Técnicas de Prompting:** implementación de Zero-Shot, Few-Shot y Chain-of-Thought (CoT).
* **Recuperación de Información (RAG básico):** consulta de productos disponibles en la base de datos e incorporación de sus características al prompt enviado al modelo.
* **Validación de Datos:** aplicación de esquemas Pydantic para validar las solicitudes.
* **Manejo de Errores:** respuestas estructuradas para errores HTTP, datos inválidos y fallas del proveedor de IA.
* **Registro de Métricas:** almacenamiento de prompts, respuestas, tokens utilizados y latencia en un archivo CSV.
* **Pruebas Automatizadas:** verificación de endpoints, validaciones y manejo de errores.
* **Integración Continua:** ejecución automática de pruebas mediante GitHub Actions.

## Técnicas de Prompting

* **Zero-Shot:** genera recomendaciones mediante instrucciones directas, sin ejemplos previos.
* **Few-Shot:** utiliza ejemplos dentro del prompt para orientar el formato y el contenido de las respuestas.
* **Chain-of-Thought (CoT):** solicita al modelo evaluar los criterios de selección antes de presentar las recomendaciones finales.

## Funcionamiento del Sistema

El sistema de recomendaciones se desarrolla en tres etapas:

1. **Retrieval:** consulta la base de datos y recupera hasta 20 productos disponibles que coincidan con los filtros del cliente.
2. **Augmentation:** incorpora la información de las prendas recuperadas al prompt junto con las preferencias del cliente.
3. **Generation:** envía el prompt a Google Gemini y devuelve las recomendaciones generadas junto con las métricas disponibles.

Si no existen productos que coincidan con los filtros, el sistema devuelve una respuesta informativa sin realizar una llamada al modelo de inteligencia artificial.

## Endpoints de la API

### Gestión de Productos

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| POST | `/api/v1/productos` | Crear un producto |
| GET | `/api/v1/productos` | Consultar todos los productos |
| GET | `/api/v1/productos/{producto_id}` | Consultar un producto por ID |
| PUT | `/api/v1/productos/{producto_id}` | Actualizar un producto |
| DELETE | `/api/v1/productos/{producto_id}` | Eliminar un producto |

### Inteligencia Artificial

| Método HTTP | Endpoint | Descripción |
|---|---|---|
| POST | `/api/v1/ai/recommend` | Generar recomendaciones personalizadas de prendas |

## Pruebas Automatizadas

El proyecto utiliza Pytest para verificar la creación y consulta de productos, la validación de datos, el manejo de errores y el funcionamiento del sistema de recomendaciones.

Las pruebas utilizan una base de datos SQLite en memoria y respuestas simuladas del proveedor de IA cuando corresponde, evitando consumir cuota de Gemini durante su ejecución.

## Registro de Métricas

Las llamadas exitosas a Google Gemini se registran en un archivo CSV que contiene:

* Técnica de prompting utilizada.
* Prompt enviado al modelo.
* Respuesta generada.
* Tokens de entrada y salida.
* Latencia de la solicitud en milisegundos.

Estas métricas permiten analizar el comportamiento del sistema y comparar las técnicas de prompting implementadas.

## Seguridad y Manejo de Errores

* Uso de variables de entorno para proteger las credenciales de la API.
* Validación de datos mediante Pydantic.
* Manejo controlado de errores HTTP.
* Respuestas específicas para productos inexistentes, datos inválidos, límites de solicitudes, fallas del proveedor de IA y tiempos de espera agotados.
* Exclusión de credenciales y archivos temporales del repositorio mediante `.gitignore`.

## Integración Continua (CI/CD)

El proyecto utiliza GitHub Actions para ejecutar automáticamente las pruebas cuando se realizan eventos `push` o `pull_request`, configurando Python 3.12, instalando las dependencias y verificando el funcionamiento de la API mediante Pytest.

