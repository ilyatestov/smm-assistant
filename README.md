# VK SMM Assistant

Platform for automating VK (VKontakte) social media management with subscription-based access control.

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ilyatestov/smm-assistant.git
cd smm-assistant
```

2. **Create environment file:**
```bash
cp .env.example .env
```

Edit `.env` and set:
```env
JWT_SECRET=your_super_secret_key_here_change_in_production
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smm_assistant
```

3. **Run with Docker Compose:**
```bash
docker-compose -f docker/docker-compose.yml up -d
```

4. **Check logs:**
```bash
docker-compose -f docker/docker-compose.yml logs -f app
```

5. **Open Swagger UI:**
Navigate to `http://localhost:8000/docs`

## 📋 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | ❌ |
| POST | `/api/v1/auth/login` | Login and get JWT token | ❌ |
| GET | `/api/v1/auth/me` | Get current user profile | ✅ |
| GET | `/health` | Health check | ❌ |

### Testing with curl

**Register:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123!"}'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "SecurePass123!"}'
```

**Get Profile (use token from login response):**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🏗️ Project Structure

```
smm-assistant/
├── core/                    # Application core
│   ├── main.py             # FastAPI app entry point
│   ├── config.py           # Configuration
│   └── security.py         # JWT & password hashing
├── api/                     # API routes
│   └── v1/
│       ├── endpoints/      # Route handlers
│       │   └── auth.py     # Authentication endpoints
│       └── schemas.py      # Pydantic models
├── models/                  # SQLAlchemy models
│   ├── base.py            # Base model class
│   └── user.py            # User model
├── utils/                   # Utilities
│   ├── logger.py          # Logging setup
│   └── dependencies.py    # Dependency injection
├── config/                  # Configuration files
│   ├── settings.py        # Pydantic settings
│   └── config.yaml        # YAML config
├── tests/                   # Tests
│   └── test_auth.py       # Auth tests
├── alembic/                 # Database migrations
├── docker/                  # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py -v
```

## 🗄️ Database Migrations

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## 🔐 Security Features

- **Password Hashing**: bcrypt via passlib
- **JWT Tokens**: 24-hour expiration
- **Protected Endpoints**: Bearer token authentication
- **Input Validation**: Pydantic models
- **SQL Injection Protection**: SQLAlchemy ORM

## 📦 Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Auth**: python-jose, passlib
- **Logging**: structlog
- **Containerization**: Docker, Docker Compose

## 🚧 Roadmap

- [ ] VK API integration
- [ ] Content generation module
- [ ] Subscription billing system
- [ ] Analytics dashboard
- [ ] Auto-posting scheduler
- [ ] Frontend (React/Streamlit)

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For issues and questions, please create an issue on GitHub.
