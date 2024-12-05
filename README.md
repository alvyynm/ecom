# ecom

A full-stack online shop.

## Key features
- Authentication with email/username + password and Google Account
- Payments with Stripe
- Sending order and payment confirmation asynchronously with RabbitMQ and Celery
- Product recommendations for products frequently bought together

## Tech Stack:
- Django
- Celery for processing tasks asynchronously
- RabbitMQ as a message broker
- Stripe for payment processing
- Redis for product recommendations

## How to run
RabbitMQ locally
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0.3-management-alpine
```
Redis locally
```bash
docker run -it --rm --name redis -p 6379:6379 redis:7.2.6-alpine
```

Postgres
```bash
docker run -it --rm --network some-network postgres:17.2-alpine3.20 psql -h some-postgres -U postgres
```

## Building a multi-architecture image
1. Enable BuildKit:
   ```bash
   export DOCKER_BUILDKIT=1
   ```
2. Create a new builder:
   ```bash
   docker buildx create --name mybuilder --use
   ```
3. Build and push the image:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t [dockerhubusername]/[dockerhubimagename]:[tag] --push .
   ```
   Example:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t rasterzoo/ecom:v0.0.3 --push .
   ```
