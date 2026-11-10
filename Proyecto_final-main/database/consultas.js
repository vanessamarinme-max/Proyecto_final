
// ==========================================
// BASE DE DATOS
// ==========================================

use("HuellitasDeAmor");


// ==========================================
// CONSULTA 1: PERROS DISPONIBLES
// ==========================================

db.perros.find({
    estado: "Disponible"
});


// ==========================================
// CONSULTA 2: SOLICITUDES POR ESTADO
// ==========================================

db.solicitudesAdopcion.aggregate([

    {
        $group: {
            _id: "$estado",
            cantidad: { $sum: 1 }
        }
    },

    {
        $sort: {
            cantidad: -1
        }
    }

]);



// ==========================================
// CONSULTA 3: ATENCIONES VETERINARIAS
// ==========================================

db.registrosVeterinarios.aggregate([

    {
        $group: {
            _id: "$tipo",
            total: { $sum: 1 }
        }
    },

    {
        $sort: {
            total: -1
        }
    },

    {
        $limit: 10
    }

]);


// ==========================================
// CONSULTA 4: ADOPCIONES POR MES
// ==========================================

db.solicitudesAdopcion.aggregate([

    {
        $match: {
            estado: "Completada",
            fechaSolicitud: { $type: "string" }
        }
    },

    {
        $project: {
            mes: {
                $substr: ["$fechaSolicitud", 0, 7]
            }
        }
    },

    {
        $group: {
            _id: "$mes",
            totalAdopciones: { $sum: 1 }
        }
    },

    {
        $sort: {
            _id: 1
        }
    }

]);


// ==========================================
// CONSULTA 5: SOLICITUDES CON ADOPTANTES
// Y PERROS
// ==========================================

db.solicitudesAdopcion.aggregate([

    {
        $lookup: {
            from: "adoptantes",
            localField: "adoptante_id",
            foreignField: "_id",
            as: "adoptante"
        }
    },

    {
        $lookup: {
            from: "perros",
            localField: "perro_id",
            foreignField: "_id",
            as: "perro"
        }
    },

    {
        $unwind: "$adoptante"
    },

    {
        $unwind: "$perro"
    },

    {
        $project: {
            _id: 0,
            adoptante: "$adoptante.nombre",
            perro: "$perro.nombre",
            estado: 1,
            fechaSolicitud: 1
        }
    }

]);
