# Backend Portfolio

REST API backend for my [portfolio](https://github.com/mejsiejdev/portfolio), providing data for projects and certificates.

## Tech Stack

### Core

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, high-performance Python web framework
- **[UV](https://docs.astral.sh/uv/)** - Fast Python package manager and project tool

### Database & Caching

- **[Supabase](https://supabase.com/)** - PostgreSQL database with Storage for images
- **[Redis](https://redis.io/)** - In-memory caching for fast response times

### Code Quality

- **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter and formatter
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints

## Features

- **Redis Caching**: Async caching decorator with automatic cache invalidation on data changes
- **Connection Pooling**: Efficient Redis connection management for high performance
- **Environment Config**: Pydantic Settings for type-safe configuration from `.env`
- **Image Storage**: Supabase Storage integration for project images (light/dark variants)
- **API Key Auth**: Simple API key authentication for protected endpoints

## API Endpoints

| Method | Endpoint             | Description                          |
| ------ | -------------------- | ------------------------------------ |
| GET    | `/health`            | Health check                         |
| GET    | `/projects/`         | List all projects (with caching)     |
| POST   | `/projects/`         | Create a project                     |
| PUT    | `/projects/{id}`     | Update a project                     |
| DELETE | `/projects/{id}`     | Delete a project                     |
| GET    | `/certificates/`     | List all certificates (with caching) |
| POST   | `/certificates/`     | Create a certificate                 |
| DELETE | `/certificates/{id}` | Delete a certificate                 |

## Development

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload

# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Environment Variables

```env
API_KEY=your-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
REDIS_URL=redis://localhost:6379
```
