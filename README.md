<p align="center">
  <p align="center">
      <img src="log.webp" alt="Djangocom" height="72">
  </p>
  <h1 align="center">
    Django Ecommerce Shop
  </h1>
  <p align="center">
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white">
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white">
  <img src="https://img.shields.io/badge/Stripe-626CD9?style=for-the-badge&logo=Stripe&logoColor=white">
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">
  </p>
</p>

<p align="center">A full-stack online shop built with Django with payments, coupons, and discounts.</p>

## Key features
- Authentication is done using Django's built-in authentication module for authentication but extended to allow email and password authentication.
- Payments with Stripe, with webhooks used to verify the payment status
- Sending order and payment confirmation messages asynchronously with RabbitMQ and Celery. Celery is used as the task processor and RabbitMQ as the message broker.
- Product recommendations for products frequently bought together. This is implemented using Redis.
- Both logged in and anonymous (unauthenticated users) can place orders

## Quick Project Demo

## Tech Stack:
- Django
- PostgreSQL database
- Celery for processing tasks asynchronously
- RabbitMQ as a message broker
- Stripe for payment processing
- Redis for product recommendations
- Nginx as 1) a reverse proxy (sitting in front of your uWSGI application server) and 2) a static file server for serving static files directly instead of the slow Django server
- Docker for containerization and Docker Compose to manage the multi-container setup

## How to run

For development:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
For production:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
NB: You need to specify `.env.dev` for development and `.env.prod` for production at the root


## Building a multi-architecture image
1. Enable BuildKit:
   ```bash
   export DOCKER_BUILDKIT=1
   ```
2. Create a new builder:
   ```bash
   docker buildx create --name mybuilder --use
   ```
   NB: You can remove the builder by running the following command:
   ```bash
   docker buildx rm mybuilder
   ```
3. Build and push the image:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t [dockerhubusername]/[dockerhubimagename]:[tag] --push .
   ```
   Example:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t rasterzoo/ecom:v0.0.3 --push .
   ```
