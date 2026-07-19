const modelService = require('../services/modelService');

exports.predict = async (req, res) => {
  try {
    const {result} = await modelService.predict(req.body);

    res.json({
      user: req.user.email,
      prediction: result.prediction,
      probability: result.probability,
    });
  } catch (err) {
    res.status(502).json({ error: 'Model API unavailable', detail: err.message });
  }
};

exports.modelHealth = async (req, res) => {
  try {
    const status = await modelService.healthCheck();
    res.json(status);
  } catch (err) {
    res.status(502).json({ error: 'Model API unreachable', detail: err.message });
  }
};
