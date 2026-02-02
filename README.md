# FastAPI Pundra

[![PyPI version](https://badge.fury.io/py/fastapi-pundra.svg)](https://badge.fury.io/py/fastapi-pundra)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Pundra: Your FastAPI Companion for Productivity**

FastAPI Pundra is a comprehensive toolkit that extends FastAPI with essential utilities, helpers, and integrations to accelerate your API development. Whether you're building REST APIs or GraphQL endpoints, Pundra provides the building blocks you need to create robust, scalable applications.

## 🚀 Features

### 🔧 Common Utilities
- **Password Management**: Secure password hashing and verification using bcrypt
- **JWT Utilities**: Token generation and validation helpers
- **Raw SQL Support**: Execute raw SQL queries with ease
- **Helper Functions**: Common utility functions for path management and more

### 📧 Email System
- **Template-based Emails**: HTML email templates with inline CSS support
- **Background Email Tasks**: Asynchronous email sending with Celery integration
- **Mail Queue Management**: Reliable email delivery with queue support
- **Multiple Recipients**: Support for CC, BCC, and reply-to functionality

### 🔄 Task Scheduling
- **Celery Integration**: Seamless Celery setup and configuration
- **Cron Scheduling**: Define and manage scheduled tasks
- **Beat Scheduler**: Redis-based beat scheduler for reliable task execution
- **Dynamic Task Discovery**: Automatic task module discovery

### 🌐 REST API Enhancements
- **Auto Router Registration**: Automatic discovery and binding of FastAPI routers
- **Exception Handling**: Comprehensive exception classes for different HTTP status codes
- **Global Exception Handler**: Centralized error handling for your FastAPI app
- **Pagination**: Built-in pagination with URL generation
- **Validation Helpers**: Enhanced request validation utilities

### 🍓 GraphQL Support (Strawberry)
- **Common GraphQL Types**: Reusable GraphQL type definitions
- **Pagination Types**: Generic paginated list types for GraphQL
- **Resolver Utilities**: Helper functions for Strawberry resolvers
- **Validation Integration**: GraphQL-specific validation helpers

## 📦 Installation

```bash
pip install fastapi-pundra
```

## 🛠️ Quick Start

### Basic Setup

```python
from fastapi import FastAPI
from fastapi_pundra.rest.global_exception_handler import setup_exception_handlers
from fastapi_pundra.common.password import generate_password_hash, compare_hashed_password

app = FastAPI()

# Setup global exception handling
setup_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI Pundra!"}
```

### Password Management

```python
from fastapi_pundra.common.password import generate_password_hash, compare_hashed_password

# Hash a password
password = "my_secure_password"
hashed = generate_password_hash(password)

# Verify a password
is_valid = compare_hashed_password(password, hashed)
print(is_valid)  # True
```

### Email Sending

```python
from fastapi import BackgroundTasks
from fastapi_pundra.common.mailer.mail import send_mail, send_mail_background

# Send email directly
await send_mail(
    subject="Welcome!",
    to=["user@example.com"],
    template_name="welcome_email.html",
    context={"username": "John Doe"}
)

# Send email in background
async def send_welcome_email(background_tasks: BackgroundTasks):
    await send_mail_background(
        background_tasks=background_tasks,
        subject="Welcome!",
        to=["user@example.com"],
        template_name="welcome_email.html",
        context={"username": "John Doe"}
    )
```

### Pagination

```python
from fastapi import Request
from fastapi_pundra.rest.paginate import paginate

@app.get("/users")
async def get_users(request: Request):
    # Assuming you have a SQLAlchemy query
    query = session.query(User)
    return paginate(
        request=request,
        query=query,
        serilizer=UserSerializer,
        the_page=1,
        the_per_page=10
    )
```

### Auto Router Registration

Automatically discover and register all routers in your API package without manual imports:

```python
from fastapi import APIRouter
from fastapi_pundra.rest import auto_bind_router

router = APIRouter()

# Auto-discover and bind all routers from your API package
# This will discover:
# - Root level modules (health.py, users.py, etc.)
# - Versioned subdirectories (v1/, v2/, etc.) with automatic prefix
auto_bind_router(router, "app.api")
```

**Project Structure Example:**

```
app/
└── api/
    ├── router.py          # Main router with auto_bind_router
    ├── health.py          # → Routes: /health/*
    ├── root.py            # → Routes: /*
    └── v1/
        ├── users.py       # → Routes: /v1/users/*
        └── posts.py       # → Routes: /v1/posts/*
```

**Configuration Options:**

```python
auto_bind_router(
    router=router,                    # Required: Your APIRouter instance
    api_package_path="app.api",       # Required: Package path to scan
    skip_files=["__init__.py", "router.py"],  # Optional: Files to skip
    discover_versioned=True,          # Optional: Scan versioned folders (v1/, v2/)
)
```

### Celery Task Scheduling

```python
from fastapi_pundra.common.scheduler.celery import create_celery_app

# Create Celery app
celery_app = create_celery_app("my_project")

@celery_app.task
def my_scheduled_task():
    print("This task runs on schedule!")
    return "Task completed"
```

### GraphQL with Strawberry

```python
import strawberry
from fastapi_pundra.gql_berry.common_gql_type import PaginatedList

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> PaginatedList[User]:
        # Your logic here
        return PaginatedList(
            data=[User(id=1, name="John", email="john@example.com")],
            pagination={"page": 1, "total": 1}
        )
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM_ADDRESS=noreply@yourdomain.com
MAIL_HOST=smtp.gmail.com
MAIL_PORT=465
MAIL_SSL_TLS=True
MAIL_STARTTLS=False
MAIL_USE_CREDENTIALS=True

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Project Configuration
PROJECT_BASE_PATH=app
```

## 📁 Project Structure

```
fastapi-pundra/
├── common/                 # Common utilities
│   ├── helpers.py         # Helper functions
│   ├── jwt_utils.py       # JWT utilities
│   ├── password.py        # Password management
│   ├── mailer/            # Email system
│   │   ├── mail.py        # Email sending
│   │   ├── mail_queue.py  # Email queue
│   │   └── ...
│   ├── raw_sql/           # Raw SQL utilities
│   └── scheduler/         # Task scheduling
├── rest/                  # REST API utilities
│   ├── route_register.py  # Auto router registration
│   ├── exceptions.py      # Exception classes
│   ├── paginate.py        # Pagination
│   └── ...
└── gql_berry/            # GraphQL utilities
    ├── common_gql_type.py # GraphQL types
    ├── pagination.py      # GraphQL pagination
    └── ...
```

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## 📚 Documentation

- [API Reference](https://github.com/code4mk/fastapi-pundra/blob/main/docs/api.md)
- [Examples](https://github.com/code4mk/fastapi-pundra/blob/main/docs/examples.md)
- [Changelog](https://github.com/code4mk/fastapi-pundra/blob/main/CHANGELOG.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mostafa Kamal**
- Email: hiremostafa@gmail.com
- GitHub: [@code4mk](https://github.com/code4mk)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The modern, fast web framework for building APIs
- [Strawberry GraphQL](https://strawberry.rocks/) - Python GraphQL library
- [Celery](https://docs.celeryproject.org/) - Distributed task queue
- [FastAPI-Mail](https://github.com/sabuhish/fastapi-mail) - Email sending for FastAPI

## 📈 Roadmap

- [ ] Add more GraphQL utilities
- [ ] Enhanced caching support
- [ ] Database migration helpers
- [ ] API rate limiting
- [ ] WebSocket utilities
- [ ] Enhanced logging system

---

**Made with ❤️ for the FastAPI community**