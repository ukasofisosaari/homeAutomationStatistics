const util = require("util");
const fs = require("fs");
const jsonConfig = JSON.parse(fs.readFileSync("./config/config.json"));

const url = util.format("mongodb://%s:%s@%s:%s/%s",
    jsonConfig.mongodb_username,
    jsonConfig.mongodb_pwd,
    jsonConfig.mongodb_url,
    jsonConfig.mongodb_port,
    jsonConfig.mongodb_database
);

exports.url = url;

exports.jsonConfig = jsonConfig;