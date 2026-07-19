const express = require('express');
const auth = require('../middleware/auth');
const validate = require('../middleware/validate');
const predictValidation = require('../validations/predict');
const predictController = require('../controllers/predictController');

const router = express.Router();

router.post('/predict', auth, predictValidation.predict, validate, predictController.predict);
router.get('/health/model', auth, predictController.modelHealth);

module.exports = router;
