/**
 * Consultas y Pipelines de Agregación Oficiales - Huellitas de Amor
 * Proyecto Final - Base de NoSQL
 */

use("huellitas_de_amor");

// ==========================================
// CONSULTA 1: PERRITOS POR TAMAÑO ($group, $sum)
// ==========================================
db.perros.aggregate([
    {
        "$group": {
            "_id": "$tamano",
            "total_perritos": { "$sum": 1 }
        }
    }
]);


// ==========================================
// CONSULTA 2: INVENTARIO DE TIENDA Y VALOR POTENCIAL ($group, $sum, $multiply, $sort)
// ==========================================
db.tienda.aggregate([
    {
        "$group": {
            "_id": "$categoria",
            "total_stock": { "$sum": "$stock" },
            "valor_inventario_potencial": { "$sum": { "$multiply": ["$precio", "$stock"] } },
            "cantidad_productos": { "$sum": 1 }
        }
    },
    { 
        "$sort": { "valor_inventario_potencial": -1 } 
    }
]);


// ==========================================
// CONSULTA 3: SOLICITUDES DETALLADAS CON ADOPTANTES ($lookup, $unwind)
// ==========================================
db.solicitudesAdopcion.aggregate([
    {
        "$lookup": {
            "from": "adoptantes",
            "localField": "adoptante_id",
            "foreignField": "_id",
            "as": "info_adoptante"
        }
    },
    { 
        "$unwind": "$info_adoptante" 
    }
]);
