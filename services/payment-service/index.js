require('./tracing');
const express = require('express');

const app = express();
const PORT = 3002;

app.get('/payments', (req, res) => {
  // Simulate some latency
  const delay = Math.random() * 200;
  setTimeout(() => {
    res.json({
      payments: [
        { id: 'PAY-001', amount: 150.00, currency: 'USD', status: 'completed' },
        { id: 'PAY-002', amount: 75.50, currency: 'USD', status: 'pending' }
      ]
    });
  }, delay);
});

app.get('/payments/verify', (req, res) => {
  res.json({ verified: true, gateway: 'stripe' });
});

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'payment-service' }));

app.listen(PORT, () => console.log(`Payment Service listening on port ${PORT}`));
