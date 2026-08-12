require('./tracing');
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3001;

app.get('/orders', async (req, res) => {
  // Simulate processing and calling payment service
  const paymentCheck = await axios.get('http://payment-service:3002/payments/verify');
  res.json({
    orders: [
      { id: 'ORD-001', item: 'Widget A', quantity: 3, status: 'confirmed', payment: paymentCheck.data },
      { id: 'ORD-002', item: 'Widget B', quantity: 1, status: 'pending' }
    ]
  });
});

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'order-service' }));

app.listen(PORT, () => console.log(`Order Service listening on port ${PORT}`));
