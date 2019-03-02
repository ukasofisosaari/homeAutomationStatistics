var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var fs = require('fs');
var morgan = require('morgan');
var logger = ('./controllers/logger');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
const configFile = JSON.parse(fs.readFileSync("./config/config.json"));

var api = require('./routes/api');

var app = express();
app.use(express.static(path.join(__dirname, 'client/dist')));
// view engine setup
//app.set('views', path.join(__dirname, 'views'));
//app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

//Successfulla access logging
var accessLogStream = fs.createWriteStream(path.join(configFile.log_dir, 'access.log'), { flags: 'a' });
app.use(morgan('combined', {skip: function (req, res) {
        return res.statusCode >= 400
    }, stream: accessLogStream }));

//Error logging
var errorLogStream = fs.createWriteStream(path.join(configFile.log_dir, 'error.log'), { flags: 'a' });
app.use(morgan('combined', {skip: function (req, res) {
        return res.statusCode < 400
    }, stream: errorLogStream }));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "http://localhost:4200");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  next();
});


app.use('/api', api);

app.get('*', function (req, res) {
  res.sendFile(path.join(__dirname, 'client/dist/index.html'))
});

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    logger.error('404 page requested');
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handler
app.use(function(err, req, res, next) {
console.log(err);
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});


module.exports = app;
