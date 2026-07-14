# AI Agent Instructions for FastAPI Backend

## Project Overview

A modern Python backend API for a Korean tourism/location sharing platform using **FastAPI** with SQLAlchemy ORM. The API includes location directories, user posts, comments, and restaurant recommendations with real-time chat features.

**Current State**: API endpoints working with in-memory data storage; database integration in progress.

## Tech Stack & Running the Project

### Requirements
- Python 3.8+
- Dependencies in `requirements.txt` (FastAPI 0.139.0, SQLAlchemy, Pydantic v2, Uvicorn)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# API docs: http://localhost:8000/docs (Swagger)
```

### Key Commands
- **Run API**: `uvicorn app.main:app --reload`
- **Run production**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- **Check types**: `python -m mypy app/` (when mypy is added)

## Architecture

### File Structure
```
app/
├── main.py          # REST endpoints (15+), temporary in-memory storage
├── models.py        # SQLAlchemy ORM models (Location, Post, Comment, PostImage)
└── __init__.py
```

### Data Model
- **Location**: Tourist destinations (name, coords, phone, category)
- **Post**: User-generated content tied to locations (title, content, nickname, password-protected)
- **Comment**: Replies to posts (also password-protected)
- **PostImage**: Post attachments

### Architecture Pattern
Three-tier:
1. **API Layer** (main.py): FastAPI endpoints with Pydantic request/response validation
2. **Data Layer** (models.py): SQLAlchemy ORM tables with relationships
3. **Storage** (in-memory → DB): Currently Python lists; will transition to database

## Code Conventions

✓ **Type Hints**: Used throughout for clarity and IDE support  
✓ **Pydantic Models**: All request bodies validated (e.g., `PostCreate`, `ChatRequest`)  
✓ **Error Handling**: HTTPException with appropriate status codes (404, 403, 400)  
✓ **Relationships**: Cascade delete configured in SQLAlchemy models  
✓ **Pagination**: `page` and `page_size` query parameters where applicable  
✓ **Filtering**: By `keyword` or `category` in list endpoints  

**Note on Security**: Plaintext password validation is intentional for this learning project.

## Common AI Agent Tasks

### Database Integration
- Create `database.py` for SQLAlchemy session management
- Replace in-memory lists with actual database queries
- Ensure models in `models.py` align with endpoints

### Testing
- Add pytest test suite for endpoints
- Mock database sessions for unit tests
- Suggested: `tests/test_posts.py`, `tests/test_locations.py`

### Validation & Documentation
- Expand endpoint docstrings with Pydantic examples
- Add request/response status code documentation
- Improve README.md with API overview and setup instructions

### Error Handling Improvements
- Implement consistent error response format
- Add validation error messages
- Handle edge cases (empty results, invalid pagination)

## Key Files to Know

| File | Purpose | Current Status |
|------|---------|---|
| [app/main.py](app/main.py) | All REST endpoints + request handlers | Functional with in-memory data |
| [app/models.py](app/models.py) | SQLAlchemy table definitions | Ready for DB integration |
| [requirements.txt](requirements.txt) | Python dependencies | Complete |
| [README.md](README.md) | Project documentation | Minimal—expand needed |

## Development Gaps & Opportunities

- [ ] `database.py`: SQLAlchemy session factory and connection setup
- [ ] Test suite: pytest tests for endpoints and models
- [ ] Environment config: `.env` file for database URL, secrets
- [ ] API documentation: Comprehensive README with examples
- [ ] Database migration: Script to transition from in-memory to persistent storage
- [ ] Deployment config: Docker, environment-based settings

## Testing & Quality

- **Auto-docs**: Swagger available at `/docs` and ReDoc at `/redoc`
- **Type checking**: Consider adding mypy to CI/CD (not yet configured)
- **Linting**: No linter configured yet; consider ruff or flake8

## Performance & Scalability

- Currently uses in-memory storage—suitable for learning, not production
- Database integration will enable multi-user concurrent access
- Consider async database driver (asyncpg for PostgreSQL) for FastAPI's async nature

---

## Tips for Contributing

1. **Before adding endpoints**: Check if models already exist in `models.py`
2. **Validation first**: Use Pydantic models for all request inputs
3. **Database queries**: Once `database.py` exists, import sessions from there
4. **Async patterns**: Use `async def` for handlers; FastAPI handles async/sync automatically
5. **Cascade deletes**: Verify relationships in models.py when deleting records

