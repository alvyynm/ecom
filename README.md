# ecom

A full-stack online shop.

## Key features
- Authentication with email/username + password and Google Account
- Payments with Stripe
- Sending order and payment confirmation asynchronously with RabbitMQ and Celery

## Tech Stack:
- Django
- Celery for processing tasks asynchronously
- RabbitMQ as a message broker
- Stripe for payment processing