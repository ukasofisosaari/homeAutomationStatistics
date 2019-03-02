const winston = require("winston");

var fs = require('fs');
const configFile = JSON.parse(fs.readFileSync("./config/config.json"));

const level = process.env.LOG_LEVEL || 'debug';

const logger = new winston.Logger({
    transports: [
        new winston.transports.File({
            level: level,
            filename: path.join(configFile.log_dir, 'has.log'),
            timestamp: function () {
                return (new Date()).toISOString();
            }
        })
    ]
});

module.exports = logger;