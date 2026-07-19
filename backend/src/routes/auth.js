const express = require('express');
const auth = require('../middleware/auth');
const validate = require('../middleware/validate');
const authValidation = require('../validations/auth');
const authController = require('../controllers/authController');

const router = express.Router();

router.post('/register', authValidation.register, validate, authController.register);
router.post('/login', authValidation.login, validate, authController.login);
router.get('/me', auth, authController.me);

module.exports = router;
