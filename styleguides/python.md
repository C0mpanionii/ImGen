# Python Style Guide

This document outlines Python-specific coding standards for this project, following PEP 8 and other Python best practices.

## Code Formatting

### Line Length
- Maximum line length: 88 characters (Black formatter default)
- For docstrings and comments: 72 characters

### Indentation
- Use 4 spaces per indentation level
- Never use tabs

### Blank Lines
- Two blank lines around top-level functions and classes
- One blank line around methods within classes
- Use blank lines sparingly within functions

## Imports

### Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

### Import Style
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import requests
import numpy as np

# Local
from .utils import helper_function
from .models import User
```

### Import Guidelines
- Use absolute imports when possible
- Avoid wildcard imports (`from module import *`)
- Import only what you need
- Use `from module import name` for frequently used names

## Naming Conventions

### Variables and Functions
- Use `snake_case` for variables and functions
- Use descriptive names
```python
# Good
user_count = 10
def calculate_total_price():
    pass

# Bad
uc = 10
def calcTotPrice():
    pass
```

### Classes
- Use `PascalCase` for class names
```python
class UserManager:
    pass

class HTTPClient:
    pass
```

### Constants
- Use `UPPER_SNAKE_CASE` for constants
```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"
```

### Private Variables
- Use single underscore prefix for internal use
- Use double underscore prefix for name mangling
```python
class Example:
    def __init__(self):
        self._internal_var = "internal"
        self.__private_var = "private"
```

## Code Structure

### Function and Method Definitions
```python
def function_name(param1: str, param2: int = 0) -> str:
    """Brief description of the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this exception is raised
    """
    return f"{param1}: {param2}"
```

### Class Definitions
```python
class ExampleClass:
    """Brief description of the class.
    
    Attributes:
        attribute1: Description of attribute1
        attribute2: Description of attribute2
    """
    
    def __init__(self, param1: str) -> None:
        """Initialize the class."""
        self.attribute1 = param1
        self.attribute2 = []
    
    def public_method(self) -> None:
        """Public method description."""
        pass
    
    def _private_method(self) -> None:
        """Private method description."""
        pass
```

## Type Hints

### Basic Usage
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

### Complex Types
```python
from typing import Optional, Union, Dict, List, Tuple, Callable

def complex_function(
    data: Dict[str, Union[int, str]],
    callback: Optional[Callable[[str], None]] = None
) -> Tuple[bool, Optional[str]]:
    pass
```

### Generic Types
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
```

## Documentation

### Docstrings
- Use triple quotes for docstrings
- Follow Google-style docstring format
- Include type information in docstrings when type hints are not sufficient

```python
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.
    
    This function multiplies length and width to get the area.
    
    Args:
        length: The length of the rectangle in meters
        width: The width of the rectangle in meters
        
    Returns:
        The area of the rectangle in square meters
        
    Raises:
        ValueError: If length or width is negative
        
    Example:
        >>> calculate_area(5.0, 3.0)
        15.0
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width must be non-negative")
    return length * width
```

## Error Handling

### Exception Handling
```python
# Good
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error occurred: {e}")
    handle_error(e)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise

# Bad
try:
    result = risky_operation()
except:
    pass
```

### Custom Exceptions
```python
class CustomError(Exception):
    """Custom exception for specific error conditions."""
    
    def __init__(self, message: str, error_code: int = None) -> None:
        super().__init__(message)
        self.error_code = error_code
```

## Best Practices

### List Comprehensions
```python
# Good
squared_numbers = [x**2 for x in range(10) if x % 2 == 0]

# Bad (for complex logic)
result = []
for x in range(10):
    if x % 2 == 0:
        if x > 5:
            result.append(x**2)
```

### Context Managers
```python
# Good
with open('file.txt', 'r') as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_connection():
    conn = create_connection()
    try:
        yield conn
    finally:
        conn.close()
```

### String Formatting
```python
# Preferred (f-strings)
name = "Alice"
age = 30
message = f"Hello, {name}! You are {age} years old."

# Acceptable (format method)
message = "Hello, {}! You are {} years old.".format(name, age)

# Avoid (% formatting)
message = "Hello, %s! You are %d years old." % (name, age)
```

## Testing

### Test Structure
```python
import pytest
from unittest.mock import Mock, patch

class TestUserManager:
    """Test cases for UserManager class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user_manager = UserManager()
    
    def test_create_user_success(self):
        """Test successful user creation."""
        user = self.user_manager.create_user("alice", "alice@example.com")
        assert user.username == "alice"
        assert user.email == "alice@example.com"
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValueError, match="Invalid email"):
            self.user_manager.create_user("alice", "invalid-email")
    
    @patch('requests.get')
    def test_api_call(self, mock_get):
        """Test API call with mocked response."""
        mock_get.return_value.json.return_value = {"status": "success"}
        result = self.user_manager.fetch_user_data("alice")
        assert result["status"] == "success"
```

## Tools and Configuration

### Recommended Tools
- **Black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter
- **mypy**: Type checker
- **pytest**: Testing framework

### Configuration Files

#### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.950
    hooks:
      - id: mypy
```

## Performance Considerations

### Efficient Data Structures
- Use `set` for membership testing
- Use `collections.defaultdict` for grouped data
- Use `collections.Counter` for counting operations

### Memory Usage
- Use generators for large datasets
- Consider using `__slots__` for classes with many instances
- Use appropriate data types (e.g., `array.array` for numeric data)

### Profiling
```python
import cProfile
import timeit

# Profile code
cProfile.run('your_function()')

# Time small code snippets
time_taken = timeit.timeit('your_function()', number=1000)
```
