var express = require('express');
var router = express.Router();


router.get('/files', function(req, res, next) {
  res.json([]);
});

router.get('/data', function(req, res, next) {
  res.json([]);
});


router.post('/data', function(req, res) {
    console.log(JSON.stringify(req.body));

    res.send();
});

module.exports = router;