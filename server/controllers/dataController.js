var mongoClient = require("mongodb").MongoClient;
var util = require("util");
const fs = require("fs");
const jsonConfig = JSON.parse(fs.readFileSync("./config/config.json"));

var url = util.format("mongodb://%s:%s@%s:%s/%s",
    jsonConfig.mongodb_username,
    jsonConfig.mongodb_pwd,
    jsonConfig.mongodb_url,
    jsonConfig.mongodb_port,
    jsonConfig.mongodb_database
);


exports.mesh_data_packet = function (req, res) {
    console.log("Inbound data packet");
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
        const query = {hostname: mesh_name};
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        dbo.collection(
            jsonConfig.mongodb_collection_data).find(query).toArray(function(err, result) {
            if (err) throw err;
            console.log(result);
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