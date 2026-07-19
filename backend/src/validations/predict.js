const { body } = require('express-validator');

exports.predict = [
  body('hours_studied')
    .isFloat({ min: 0, max: 24 })
    .withMessage('hours_studied must be 0-24'),
  body('attendance_percentage')
    .isFloat({ min: 0, max: 100 })
    .withMessage('attendance_percentage must be 0-100'),
  body('previous_grade')
    .isFloat({ min: 0, max: 100 })
    .withMessage('previous_grade must be 0-100'),
  body('sleep_hours')
    .isFloat({ min: 0, max: 24 })
    .withMessage('sleep_hours must be 0-24'),
  body('assignments_completed')
    .isInt({ min: 0, max: 20 })
    .withMessage('assignments_completed must be 0-20'),
];
