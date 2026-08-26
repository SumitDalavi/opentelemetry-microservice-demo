'use strict';
/**
 * W3C Trace Context Baggage propagation helper.
 * Attaches business context to every request so it flows through all services.
 */
const { propagation, context } = require('@opentelemetry/api');

/**
 * setBaggage — set baggage entries on the current context.
 * Example: { userId: '123', tenantId: 'acme', requestId: 'uuid' }
 */
function setBaggage(entries) {
  let bag = propagation.getBaggage(context.active()) || propagation.createBaggage();
  for (const [key, value] of Object.entries(entries)) {
    bag = bag.setEntry(key, { value: String(value) });
  }
  return propagation.setBaggage(context.active(), bag);
}

/**
 * getBaggageValue — read a baggage entry from the current context.
 */
function getBaggageValue(key) {
  const bag = propagation.getBaggage(context.active());
  return bag ? bag.getEntry(key)?.value : undefined;
}

/**
 * baggageMiddleware — Express middleware that injects request-level baggage.
 * Attach this to the API gateway so all downstream spans inherit the context.
 */
function baggageMiddleware(req, res, next) {
  const entries = {
    'user.id':      req.headers['x-user-id']   || 'anonymous',
    'tenant.id':    req.headers['x-tenant-id'] || 'default',
    'request.id':   req.headers['x-request-id'] || require('crypto').randomUUID(),
    'service.name': 'api-gateway',
  };

  const ctx = setBaggage(entries);
  context.with(ctx, () => {
    // Expose baggage as response headers for observability
    res.setHeader('X-Request-Id', entries['request.id']);
    next();
  });
}

module.exports = { baggageMiddleware, getBaggageValue, setBaggage };
