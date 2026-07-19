const config = require('../config');

class ModelService {
  constructor() {
    this.baseUrl = config.modelApiUrl;
  }

  async predict(features) {
    const response = await fetch(`${this.baseUrl}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(features),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Model API error (${response.status}): ${error}`);
    }

    return response.json();
  }

  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

module.exports = new ModelService();
