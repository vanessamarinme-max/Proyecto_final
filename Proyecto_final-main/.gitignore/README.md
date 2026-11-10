# 🐾 Huellitas de Amor | Refugio y Adopción de Perritos

Sistema web integral y backend analítico desarrollado para la gestión de un refugio de animales, combinando una interfaz interactiva con tecnologías modernas y una arquitectura de base de datos NoSQL basada en MongoDB.

---

## Autores y Contexto Académico
* **Proyecto:** Trabajo Final - Bases de NoSQL / Ingeniería Web
* **Institución:** Universidad Católica Luis Amigó
* **Ciudad:** Medellín, Colombia

---

## Tecnologías Utilizadas

### Backend y Servidor
* **Python / Flask:** Framework minimalista para el desarrollo de la API RESTful.
* **PyMongo:** Controlador oficial para la conexión y gestión de operaciones con MongoDB.

### Base de Datos
* **MongoDB Atlas / Local:** Base de datos NoSQL orientada a documentos.
* **Aggregation Pipelines:** Consultas avanzadas utilizando operadores de etapas (`$group`, `$sum`, `$multiply`, `$lookup`, `$unwind`, `$sort`).

### Frontend e Interfaz de Usuario
* **HTML5 Semántico y CSS3:** Estructuración de páginas y diseño responsivo basado en variables personalizadas y accesibilidad web.
* **JavaScript (ES6+):** Gestión de peticiones asíncronas (`fetch`), consumo de la API, renderizado dinámico de catálogos y operaciones del panel de control.

---

## Estructura del Repositorio

```text
PROYECTO_FINAL/
│
├── backend/            # Lógica del servidor Flask y rutas de la API (crud.py)
├── database/           # Scripts de pruebas y consultas de agregación oficial (consultas.js)
├── frontend/           # Páginas HTML, estilos (styles.css) y lógica de cliente (main.js)
└── README.md           # Documentación técnica del proyecto
