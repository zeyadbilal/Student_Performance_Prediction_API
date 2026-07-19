module.exports = {
  port: process.env.PORT || 3000,
  jwtSecret: process.env.JWT_SECRET || 'secret',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '7d',
  modelApiUrl: process.env.MODEL_API_URL || 'http://localhost:8000',
  db: {
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    name: process.env.DB_NAME || 'student_performance',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD
  },
};
