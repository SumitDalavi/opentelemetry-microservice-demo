require('./tracing'); // Must be first import
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.get('/api/orders', async (req, res) => {
  try {
    const orderResponse = await axios.get('http://order-service:3001/orders');
    res.json(orderResponse.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch orders' });
  }
});

app.get('/api/payments', async (req, res) => {
  try {
    const paymentResponse = await axios.get('http://payment-service:3002/payments');
    res.json(paymentResponse.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch payments' });
  }
});

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'api-gateway' }));

app.listen(PORT, () => console.log(`API Gateway listening on port ${PORT}`));
