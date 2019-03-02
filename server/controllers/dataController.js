const mongoClient = require("mongodb").MongoClient;
const url = require("../config/db").url;
const jsonConfig = require("../config/db").jsonConfig;

exports.mesh_data_packet = function (req, res) {
    console.log("Inbound data packet");
    var data_packet = req.body;
    data_packet["time"] = Date(data_packet["time"]);
    mongoClient.connect(url, function (err, db) {
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        dbo.collection(
            jsonConfig.mongodb_collection_data).insertOne(req.body, function(err, res) {
            if (err) throw err;
            console.log("1 document inserted");
            db.close();
        });
    });
    console.log(JSON.stringify(req.body));
    res.send();
};

exports.mesh_networks = function (req, res) {
    console.log(url);
    console.log(url);
    console.log(req.params);
    const mesh_name = req.params.mesh_network_name;
    const query = {hostname: mesh_name};
    mongoClient.connect(url, function (err, db) {
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        dbo.collection(
            jsonConfig.mongodb_collection_mesh_networks).find().toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            db.close();
            res.send(result);
        });
    });
};

exports.mesh_network_data = function (req, res) {
    console.log(req.params);
    mongoClient.connect(url, function (err, db) {
        const mesh_name = req.params.mesh_network_name;
        const start_date = req.query.start_date;
        const end_date = req.query.end_date;
        console.log(start_date);
        console.log(end_date);
        console.log(Date(start_date));
        const query = {hostname: mesh_name};
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        dbo.collection(
            jsonConfig.mongodb_collection_data).find(query).toArray(function(err, result) {
            if (err) throw err;
            //console.log(result);
            db.close();
            res.send(result);
        });
    });
};

/* Doesnt work yet*/
exports.register_mesh_network = function (req, res) {
    
    mongoClient.connect(url, function (err, db) {
        const mesh_name = req.params.mesh_network_name;
        const query = {mesh_network_name: mesh_name};
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        /* First lets check if it already has been registered*/
        dbo.collection(
            jsonConfig.mongodb_collection_data).find(query).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
            db.close();
            res.send(result);
        });

        /* If it has not been, lets register it*/
        dbo.collection(
            jsonConfig.mongodb_collection_data).insertOne(req.body, function(err, res) {
            if (err) throw err;
            console.log("1 document inserted");
            db.close();
        });
    });
    console.log(JSON.stringify(req.body));
    res.send();
};