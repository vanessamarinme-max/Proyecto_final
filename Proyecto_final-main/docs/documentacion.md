# Documentación Técnica del Proyecto: Huellitas de Amor

## Información del Proyecto
* **Nombre del Sistema:** Huellitas de Amor - Refugio y Adopción Canina
* **Integrantes / Autores:** Equipo de Desarrollo Huellitas de Amor
* **Tecnologías Backend:** Python (Flask), PyMongo, Certifi
* **Tecnologías Frontend:** HTML5, CSS3, JavaScript (ES6+ / Fetch API)
* **Base de Datos NoSQL:** MongoDB Atlas (Cloud Cluster)

---

## 1. Descripción del Problema y Necesidad
En la ciudad de Medellín y el Área Metropolitana existen numerosos refugios y fundaciones dedicados al rescate de animales en situación de calle o vulnerabilidad. La fundación *Huellitas de Amor* enfrentaba deficiencias en el seguimiento manual de las solicitudes de adopción, el control del catálogo de rescate y la gestión del stock de su tienda solidaria.

Se requería una solución web integral que permitiera digitalizar estos procesos, facilitando al público el envío de solicitudes de adopción y la compra de accesorios, mientras que el área administrativa pudiera gestionar la base de datos de forma centralizada, dinámica y visual.

---

## 2. Objetivo y Alcance de la Solución
* **Objetivo General:** Desarrollar una plataforma web full-stack conectada a una base de datos NoSQL en la nube para automatizar la gestión de adopciones, catálogo de caninos y ventas de la tienda solidaria.
* **Alcance:**
  * **Módulo Público:** Catálogo dinámico de perritos en adopción, tienda virtual de productos con redirección a atención por WhatsApp y formulario interactivo de solicitud de adopción.
  * **Módulo Administrativo:** Autenticación de administradores, registro dinámico (POST), actualización interactiva de registros (PUT), eliminación de datos (DELETE) y panel de analítica avanzada mediante consultas agregadas (`$group`, `$sum`, `$lookup`, `$unwind`).

---

## 3. Arquitectura Implementada
El sistema sigue una arquitectura cliente-servidor distribuida basada en el patrón de API RESTful:

```
[ Cliente / Browser ]  <--- HTTP / REST (JSON) --->  [ Backend Flask API ]  <--- PyMongo / TLS --->  [ MongoDB Atlas (Cloud) ]
 (HTML5 / CSS3 / JS)                                     (crud.py / routes)                            (Cluster NoSQL)
```

1. **Capa de Presentación (Frontend):** Interfaz responsive construida en HTML5 semántico, styled mediante CSS3 con variables nativas, e interactividad controlada por JavaScript asíncrono (`fetch`).
2. **Capa de Negocio (Backend API):** Desarrollada en Python con Flask. Maneja la lógica de validación, enrutamiento Blueprint y conversión de estructuras JSON/BSON.
3. **Capa de Datos (Database):** Base de datos NoSQL alojada en **MongoDB Atlas**, garantizando escalabilidad horizontal y alta disponibilidad.

---

## 4. Modelo de Datos y Decisiones de Diseño
El modelo de datos se diseñó utilizando un enfoque NoSQL orientado a documentos (JSON/BSON), priorizando la flexibilidad del esquema y el rendimiento en consultas.

### Principales Decisiones de Diseño:
* **Separación Automática de Responsabilidades:** Cuando un usuario envía una solicitud de adopción, el backend analiza si el adoptante ya existe en la colección `adoptantes` por su número de documento. Si existe, actualiza sus datos; de lo contrario, lo inserta en `adoptantes` y vincula su `ObjectId` dentro del documento de `solicitudesAdopcion`.
* **Tipado dinámico pero consistente:** Uso de `ObjectId` nativos de MongoDB para garantizar la integridad referencial en las relaciones entre documentos.

---

## 5. Descripción de Colecciones y Entidades
La base de datos en MongoDB contiene las siguientes colecciones principales:

1. **`perros`:** Almacena la información de los caninos rescatados.
   * *Campos:* `_id`, `nombre`, `edad`, `sexo`, `tamano`, `descripcion`, `estado`.
2. **`tienda`:** Almacena los artículos y accesorios de la tienda virtual.
   * *Campos:* `_id`, `nombre`, `categoria`, `precio`, `stock`, `descripcion`.
3. **`adoptantes`:** Contiene los datos personales del potencial adoptante.
   * *Campos:* `_id`, `nombre`, `documento`, `correo`, `celular`, `tipo_vivienda`, `cantidad_mascotas`.
4. **`solicitudesAdopcion`:** Registra las postulaciones a procesos de adopción.
   * *Campos:* `_id`, `adoptante_id` (ObjectId referencia), `fecha`, `tamano`, `programa`, `comentarios`.
5. **`registrosVeterinarios`:** Historial clínico de atenciones de los rescatados.

---

## 6. Explicación de Relaciones (Embedding vs. Referencing)
En el proyecto se aplicó una estrategia de **Referencing (Normalización)** entre las solicitudes de adopción y los adoptantes:

* **Estrategia Implementada (Referencing):** 
  * En la colección `solicitudesAdopcion` no se duplican todos los datos del adoptante, sino que se almacena el identificador `adoptante_id` como un `ObjectId`.
  * **Justificación:** Un mismo adoptante puede realizar múltiples solicitudes a lo largo del tiempo o actualizar sus datos telefónicos/residenciales. El referenciamiento evita la inconsistencia y duplicidad de datos en la base de datos.
  * **Uso de `$lookup`:** Para generar los reportes administrativos, el backend ejecuta etapas de agregación `$lookup` y `$unwind` para unir los datos del adoptante con su respectiva solicitud en tiempo de ejecución.

---

## 7. Plataforma de Base de Datos en la Nube
* **Plataforma Seleccionada:** **MongoDB Atlas (Cloud)**.
* **Justificación de Elección:**
  * Permite conectividad global segura mediante cadenas de conexión `mongodb+srv://` protegidas por TLS/SSL.
  * Facilita el monitoreo del almacenamiento, rendimiento y creación de índices sin necesidad de administrar servidores físicos.
  * Integración nativa con Python utilizando la librería `pymongo` y certificados de seguridad `certifi`.

---

## 8. Conexión entre Backend y Base de Datos
La conexión se gestiona en un módulo centralizado (`config.py`):

```python
import certifi
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://samuelsalazarmo_db_user:vFLbpXoIA83mE5sw@huellitasdeamor.wuoxemk.mongodb.net/"

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["HuellitasDeAmor"]
```
Cada endpoint de la API accede al objeto `db` para realizar operaciones CRUD o consultas de agregación, capturando posibles fallos mediante excepciones de `PyMongoError`.

---

## 9. Funcionalidades Desarrolladas
1. **Autenticación Administrativa:** Control de acceso mediante verificación de credenciales con la API de Flask (`/api/login`).
2. **Registro de Rescatados y Productos (CREATE):** Formularios en el panel de control para crear nuevos documentos en `perros` y `tienda` (`POST`).
3. **Catálogo Dinámico (READ):** Carga en tiempo real de tarjetas de productos y perritos consumidos directamente desde la API REST (`GET`).
4. **Gestión de Stock y Modificación (UPDATE):** Función interactiva para actualizar el inventario de la tienda vía `PUT`.
5. **Eliminación de Documentos (DELETE):** Remoción de registros de la base de datos con actualización visual instantánea.
6. **Módulo de Analítica y Reportes:** Agregaciones dinámicas procesadas directamente en la base de datos NoSQL.

---

## 10. Reglas de Negocio y Validaciones
* **Validación de Identificadores:** El backend inspecciona todos los campos terminados en `_id` e invalida la solicitud (`400 Bad Request`) si el valor no corresponde a un `ObjectId` válido de MongoDB.
* **Separación de Adoptante Automática:** Al registrar una solicitud de adopción, la API comprueba mediante `find_one({"documento": ...})` si el adoptante existe para actualizarlo con `$set` o crearlo con `insert_one`.
* **Seguridad en Actualizaciones:** Durante las peticiones `PUT`, el backend remueve explícitamente el campo `_id` de la carga útil para evitar la alteración accidental de la llave primaria del documento.

---

## 11. Consultas Analíticas, Reportes y Métricas
Se implementaron tres pipelines de agregación en MongoDB dentro de `crud.py`:

1. **Inventario por Categoría (`/api/reportes/tienda-por-categoria`):**
   * *Operadores:* `$group`, `$sum`, `$multiply`, `$sort`.
   * *Utilidad:* Muestra el total de productos únicos, el stock acumulado y calcula el valor financiero potencial del inventario por cada categoría de la tienda.
2. **Cruce de Solicitudes y Adoptantes (`/api/reportes/solicitudes-detalladas`):**
   * *Operadores:* `$lookup`, `$unwind`.
   * *Utilidad:* Permite a la administración ver qué adoptante está vinculado a cada solicitud sin duplicar la información.
3. **Métricas de Rescatados por Tamaño (`/api/reportes/perritos-por-tamano`):**
   * *Operadores:* `$group`, `$sum`, `$sort`.
   * *Utilidad:* Permite saber la distribución de la capacidad del refugio según el tamaño de los caninos (Pequeño, Mediano, Grande).

---

## 12. Evidencias de Funcionamiento
* **Base de Datos NoSQL en la Nube:** Almacenamiento activo en el cluster de MongoDB Atlas bajo la base de datos `HuellitasDeAmor`.
* **Interfaz de Administración:** Sección interactiva en `dashboard-admin.html` con botones funcionales para ejecutar agregaciones, editar stock y eliminar registros.

---

## 13. Conclusiones y Aprendizajes
* El modelo orientado a documentos de NoSQL ofreció una flexibilidad superior en comparación con el modelo relacional tradicional, permitiendo adaptar estructuras de datos complejas como las solicitudes de adopción sin migraciones costosas de esquema.
* La implementación del patrón de agregación (`$group`, `$lookup`) directamente en el motor de MongoDB mejoró notablemente el rendimiento del sistema, evitando procesar pesadas iteraciones en la capa del backend.
* La arquitectura RESTful decoupled (separando el cliente JavaScript del servidor Flask) garantizó una aplicación web escalable, fácil de mantener y de rápida respuesta.

---

## Enlaces del Proyecto
* **Repositorio en GitHub:** `https://github.com/luisachoachisa-ctrl/Proyecto_final`
* **Aplicación Desplegada en Internet:** `http://127.0.0.1:5000` (Ejecución local / enlace de despliegue)

---
## Enlaces del Proyecto Desplegado
* **Frontend (AWS Amplify):** https://main.d3ji3n4vrmn0nx.amplifyapp.com/
* **Backend API (AWS EC2):** http://54.210.12.34:5000
