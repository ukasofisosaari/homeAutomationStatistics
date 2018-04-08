var mongoClient = require("mongodb").MongoClient;
var util = require("util");
const fs = require("fs");
const jsonConfig = JSON.parse(fs.readFileSync("./config/config.json"));

var url = util.format("mongodb://%s:%s@%s:%s",
    jsonConfig.mongodb_username,
    jsonConfig.mongodb_pwd,
    jsonConfig.mongodb_url,
    jsonConfig.mongodb_port,
    jsonConfig.mongodb_database
);


exports.mesh_data_packet = function (req, res) {
    MongoClient.connect(url, function (err, db) {
        if (err) throw err;
        var dbo = db.db(jsonConfig.mongodb_database);
        var myData = {  };
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