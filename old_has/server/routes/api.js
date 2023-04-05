var express = require('express');
var router = express.Router();

const data_controller = require("../controllers/dataController");

router.get('/mesh_networks', data_controller.mesh_networks);

router.get('/data/:mesh_network_name', data_controller.mesh_network_data);


router.post('/data', data_controller.mesh_data_packet);

router.post('/register_mesh_network/:mesh_network_name', data_controller.register_mesh_network);

module.exports = router;