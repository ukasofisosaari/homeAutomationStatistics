const winston = require("winston");
var fs = require('fs');
var path = require('path');

const configFile = JSON.parse(fs.readFileSync("./config/config.json"));

const level = process.env.LOG_LEVEL || 'debug';

exports.Logger = new winston.createLogger ({
    transports: [
        new winston.transports.File({
            level: level,
            filename: path.join(configFile.log_dir, 'has.log'),
            format: winston.format.json(),
            handleExceptions: true,
            timestamp: function () {
                return (new Date()).toISOString();
            }
        })
    ]
});

//module.exports = logger;