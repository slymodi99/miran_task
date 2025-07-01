# Miran E-Commerce Task

An e-commerce platform built with Django REST Framework

## 🏗 Architecture

### Core Components
- **Users Module**: Handles authentication and user management
  - Custom User model with phone-based authentication
  - Customer profiles with address management
  
- **Products Module**: Manages the product catalog
  - Product categories
  - Product inventory management
  
- **Orders Module**: Handles order processing
  - Order status management (pending, shipped, cancelled)
  - Order items tracking

### Tech Stack
- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Container**: Docker

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd miran_e_commerce_task
```

2. Build and start the containers:
```bash
docker compose up --build
```

The application will be available at:
- API: http://localhost:8012
- Admin Interface: http://localhost:8012/admin

### Database Setup

1. Run migrations:
```bash
# Inside the web container
docker compose exec web python manage.py migrate
```

2. Populate the database with sample data:
```bash
docker compose exec web python manage.py populate_db
```

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
DEBUG=1
DB_NAME=miran
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=db
DB_PORT=5432
```

### Docker Configuration
The project uses Docker Compose with two services:
- `web`: Django application
- `db`: PostgreSQL database
