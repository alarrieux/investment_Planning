# Contributing to Investment Planning Optimization

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept feedback gracefully
- Prioritize the community's best interests

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/investment_Planning.git
   cd investment_Planning
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/investment_Planning.git
   ```

## Development Setup

### Prerequisites

- Python 3.8+
- R 4.0+ (optional, for R notebooks)
- Git

### Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

3. **Verify installation**:
   ```bash
   pytest
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues in existing code
- **New features**: Add new optimization models or functionality
- **Documentation**: Improve or add documentation
- **Tests**: Increase test coverage
- **Examples**: Add new example scripts or notebooks
- **Performance**: Optimize existing code

### Contribution Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write tests** for new functionality

4. **Update documentation** as needed

5. **Run tests** to ensure everything works:
   ```bash
   pytest
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Organized using `isort`
- **Formatting**: Use `black` for code formatting

### Code Formatting

Before committing, format your code:

```bash
# Format with black
black src/ tests/ examples/

# Sort imports
isort src/ tests/ examples/

# Check style
flake8 src/ tests/ examples/
```

### Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Documentation Strings

All public functions and classes must have docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """Brief description of function.

    Longer description if needed, explaining the function's
    purpose and behavior in detail.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception is raised

    Example:
        >>> result = function_name("value1", "value2")
        >>> print(result)
        Expected output
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange: Set up test data
    optimizer = ModelOptimizer()

    # Act: Perform the action
    result = optimizer.solve()

    # Assert: Verify the result
    assert result['status'] == 'Optimal'
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_bank_loan.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v
```

### Test Coverage

- Aim for at least 80% code coverage
- Write tests for edge cases and error conditions
- Test both successful and failure scenarios

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings in code
2. **API Reference**: Detailed function/class documentation
3. **Tutorials**: Step-by-step guides
4. **Examples**: Working code examples

### Building Documentation

```bash
cd docs
sphinx-build -b html . _build
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Explain the "why" not just the "what"
- Keep documentation up to date with code changes

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Code formatted
- [ ] No breaking changes (or documented)
```

### Review Process

1. Automated tests will run on your PR
2. Maintainers will review your code
3. Address any feedback or requested changes
4. Once approved, your PR will be merged

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify the bug exists in the latest version
- Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Step 1
2. Step 2
3. ...

**Expected behavior**
What you expected to happen

**Actual behavior**
What actually happened

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.5]
- Package version: [e.g., 2.0.0]

**Additional context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Suggestions

We welcome suggestions for:

- New optimization models
- Performance improvements
- Additional features
- UI/UX improvements
- Documentation enhancements

### Enhancement Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Motivation**
Why is this feature needed?

**Proposed Solution**
How should this be implemented?

**Alternatives**
Other approaches considered

**Additional Context**
Examples, mockups, references, etc.
```

## Questions?

If you have questions:

- Check existing documentation
- Search closed issues
- Open a new issue with the `question` label
- Reach out to maintainers

## Recognition

Contributors will be:

- Listed in the project's contributors file
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing to Investment Planning Optimization!

---

**Happy Coding!** 🚀
