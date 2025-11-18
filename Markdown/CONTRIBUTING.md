# Contributing to MindBody Strength Coach

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and small

## Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement `execute()` and `_initialize()` methods
3. Register tools using `register_tool()`
4. Add agent to orchestration engine in `main.py`

## Adding New Tools

1. Create a tool class inheriting from `BaseTool`
2. Implement `execute()` method
3. Register tool with agent or tool registry

## Testing

Run tests with:
```bash
pytest test_system.py
```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Update documentation
5. Submit a pull request

## Questions?

Open an issue for questions or discussions.

