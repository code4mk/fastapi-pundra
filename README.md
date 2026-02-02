# FastAPI Pundra

[![PyPI version](https://badge.fury.io/py/fastapi-pundra.svg)](https://badge.fury.io/py/fastapi-pundra)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/fastapi-pundra)](https://pepy.tech/project/fastapi-pundra)

**Pundra: Your FastAPI Companion for Productivity**

FastAPI Pundra is a comprehensive toolkit that extends FastAPI with essential utilities, helpers, and integrations to accelerate your API development. Whether you're building REST APIs or GraphQL endpoints, Pundra provides the building blocks you need to create robust, scalable applications.

---

## 📖 [**Full Documentation**](https://opensource.code4mk.org/docs/fastapi-pundra) | [Quick Start Guide](https://opensource.code4mk.org/docs/fastapi-pundra) | [Templates](https://opensource.code4mk.org/docs/fastapi-pundra)

---

## ✨ Why FastAPI Pundra?

- 🚀 **Zero Boilerplate**: Auto-discover routes, automatic pagination, built-in exception handling
- 🔋 **Batteries Included**: Email system, JWT auth, GraphQL support, raw SQL utilities out of the box
- 📦 **Production Ready**: Battle-tested utilities for password hashing, validation, and error handling
- 🎯 **Developer Experience**: Write less code, focus on business logic, ship faster

## 🚀 Features

- 🔧 **Common Utilities**: Password hashing, JWT auth, raw SQL support, helper functions
- 📧 **Email System**: Template-based emails, background tasks, mail templating with inline CSS
- 🌐 **REST API**: Auto router registration, exception handling, pagination, validation helpers
- 🍓 **GraphQL (Strawberry)**: Common types, pagination, resolver utilities, validation integration

**[📖 Explore all features in detail →](https://opensource.code4mk.org/docs/fastapi-pundra)**

## 📦 Installation

**Using pip:**
```bash
pip install fastapi-pundra
```

**Using uv (recommended for faster installation):**
```bash
uv pip install fastapi-pundra
```

Or add to your project:
```bash
uv add fastapi-pundra
```

## ⚡ Quick Start (30 Seconds)

```python
from fastapi import FastAPI
from fastapi_pundra.rest import auto_bind_router
from fastapi_pundra.rest.global_exception_handler import setup_exception_handlers

app = FastAPI()

# Setup global exception handling
setup_exception_handlers(app)

# Auto-discover and bind all API routes
router = APIRouter()
auto_bind_router(router, "app.api")
app.include_router(router)
```

**Project Structure:**

```
app/
└── api/
    ├── health.py      # → /health/*
    └── v1/
        ├── users.py   # → /v1/users/*
        └── posts.py   # → /v1/posts/*
```

**[📖 View complete tutorials and examples →](https://opensource.code4mk.org/docs/fastapi-pundra)**

## 🔧 Key Features Showcase

### Auto Router Registration
No more manual router imports! Pundra automatically discovers and registers all your API routes.

### Email System
Send beautiful HTML emails with templates and background tasks using FastAPI's native BackgroundTasks.

### REST & GraphQL
Comprehensive utilities for both REST APIs and GraphQL (Strawberry) endpoints.

**[📖 See detailed examples and configuration →](https://opensource.code4mk.org/docs/fastapi-pundra)**

## 📚 Documentation & Resources

🌐 **[Full Documentation Site](https://opensource.code4mk.org/docs/fastapi-pundra)** ← Start here!

**Quick Links:**
- [📖 Getting Started Guide](https://opensource.code4mk.org/docs/fastapi-pundra)
- [🎯 API Reference](https://opensource.code4mk.org/docs/fastapi-pundra)
- [📝 Tutorials & Examples](https://opensource.code4mk.org/docs/fastapi-pundra)
- [🎨 Templates](https://opensource.code4mk.org/docs/fastapi-pundra)
- [📋 Changelog](https://github.com/code4mk/fastapi-pundra/blob/main/CHANGELOG.md)

## 💬 Community & Support

- 📖 [Documentation](https://opensource.code4mk.org/docs/fastapi-pundra) - Comprehensive guides and tutorials
- 🐛 [Issues](https://github.com/code4mk/fastapi-pundra/issues) - Report bugs or request features
- 💡 [Discussions](https://github.com/code4mk/fastapi-pundra/discussions) - Ask questions and share ideas
- 🔗 [LinkedIn](https://linkedin.com/in/code4mk) - Follow for updates
- 📧 [Email](mailto:hiremostafa@gmail.com) - Direct support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you would like to change.

**[📖 Contributing Guide →](https://opensource.code4mk.org/docs/fastapi-pundra)**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mostafa Kamal** ([@code4mk](https://github.com/code4mk))
- Email: hiremostafa@gmail.com
- GitHub: [github.com/code4mk](https://github.com/code4mk)
- LinkedIn: [linkedin.com/in/code4mk](https://linkedin.com/in/code4mk)

## 🙏 Acknowledgments

Built with these amazing tools:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [Strawberry GraphQL](https://strawberry.rocks/) - Python GraphQL library



---

<div align="center">

**Made with ❤️ for the FastAPI community**

⭐ Star us on [GitHub](https://github.com/code4mk/fastapi-pundra) | 📖 Read the [Docs](https://opensource.code4mk.org/docs/fastapi-pundra)

</div>