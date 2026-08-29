require('./tracing');
const { trace } = require('@opentelemetry/api');
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3001;

const tracer = trace.getTracer('order-service-tracer');

app.get('/orders', async (req, res) => {
  return await tracer.startActiveSpan('process-orders', async (span) => {
    try {
      span.setAttribute('order.process.start', true);
      // Simulate processing and calling payment service
      const paymentCheck = await axios.get('http://payment-service:3002/payments/verify');
      span.addEvent('payment-verification-completed', { status: paymentCheck.data.status });
      
      const responsePayload = {
        orders: [
          { id: 'ORD-001', item: 'Widget A', quantity: 3, status: 'confirmed', payment: paymentCheck.data },
          { id: 'ORD-002', item: 'Widget B', quantity: 1, status: 'pending' }
        ]
      };
      
      span.setAttribute('order.count', responsePayload.orders.length);
      res.json(responsePayload);
    } catch (error) {
      span.recordException(error);
      span.setStatus({ code: 2 }); // Error
      res.status(500).json({ error: 'Failed to process orders' });
    } finally {
      span.end();
    }
  });
});

app.get('/health', (req, res) => res.json({ status: 'ok', service: 'order-service' }));

app.listen(PORT, () => console.log(`Order Service listening on port ${PORT}`));
