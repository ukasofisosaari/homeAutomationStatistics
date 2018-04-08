var express = require('express');
var router = express.Router();

const data_controller = require("../controllers/dataController");

router.get('/files', function(req, res, next) {
  res.json([]);
});

router.get('/data', function(req, res, next) {
  res.json([]);
});

router.post('/data', data_controller.mesh_data_packet);

module.exports = router;