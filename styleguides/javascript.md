# JavaScript/TypeScript Style Guide

This document outlines JavaScript and TypeScript coding standards for this project, inspired by common community standards and best practices.

## Code Formatting

### Line Length
- Maximum line length: 100 characters

### Indentation
- Use 2 spaces per indentation level
- Avoid tabs

### Semicolons
- Use semicolons at the end of statements

### Commas
- Use trailing commas in multiline object literals, arrays, and function calls
```javascript
// Good
const obj = {
    key1: 'value1',
    key2: 'value2',
};

// Good
const arr = [
    1,
    2,
    3,
];
```

## Imports

### Import Style
- Use ES6 `import` statements
- Use destructuring for specific imports
- Group imports logically

### Import Order
1. Standard library imports (in TypeScript)
2. Third-party imports
3. Local application imports

### Import Guidelines
- Use absolute imports for main dependencies
- Keep import paths short
```typescript
// Good
import { Component } from 'react';
import { Button } from '@material-ui/core';

// Bad
import Component from '../../../node_modules/react/Component';
```

## Naming Conventions

### Variables and Functions
- Use `camelCase` for variables and functions
- Use descriptive names
```typescript
// Good
let userRole = 'admin';
function calculateArea(width: number, height: number): number {
    return width * height;
}

// Bad
let u = 'admin';
function calc(w, h) {
    return w * h;
}
```

### Classes and Interfaces
- Use `PascalCase` for class and interface names
- Use the `I` prefix for interfaces
```typescript
class UserManager {
    // class logic here
}

interface IUser {
    username: string;
    email: string;
}
```

### Constants
- Use `UPPER_SNAKE_CASE` for constants
```typescript
const MAX_RETRY_COUNT = 5;
const API_ENDPOINT = 'https://api.example.com';
```

## Code Structure

### Function and Method Definitions
- Use concise syntax for arrow functions, especially in callbacks
```typescript
const add = (x: number, y: number): number => x + y;
```

### Class Definitions
```typescript
class ExampleClass {
    private _privateProperty: string;

    constructor(initialValue: string) {
        this._privateProperty = initialValue;
    }

    public getProperty(): string {
        return this._privateProperty;
    }
}
```

## Type Annotations

### Basic Usage
- Use type annotations liberally
```typescript
let count: number = 10;
let names: string[] = ['Alice', 'Bob'];
```

### Interfaces and Types
- Use interfaces for object shapes
- Use types for other custom types and unions
```typescript
interface User {
    username: string;
    password: string;
}

type ID = number | string;
```

### Generics
```typescript
type Response<T> = {
    data: T;
    status: number;
};

function fetchData<T>(url: string): Promise<Response<T>> {
    // implementation
}
```

## Documentation

### Comments
- Use comments to explain "why" instead of "what"
- Write doc comments for public methods and classes
```typescript
/**
 * Calculate the sum of two numbers.
 * @param {number} a - The first number.
 * @param {number} b - The second number.
 * @returns {number} The sum of `a` and `b`.
 */
function sum(a: number, b: number): number {
    return a + b;
}
```

## Error Handling

### Exception Handling
- Use `try/catch` blocks for exception handling
```typescript
try {
    const data = fetchData('https://api.example.com');
} catch (error) {
    console.error('Error fetching data:', error);
}
```

### Custom Errors
```typescript
class CustomError extends Error {
    constructor(message: string, public code: number) {
        super(message);
        this.name = 'CustomError';
    }
}
```

## Performance Considerations

### Efficient Data Structures
- Use `Map` and `Set` for collections
- Use typed arrays for performance-sensitive numeric operations

### Memory Usage
- Be mindful of memory usage in loops and recursive functions
- Use `WeakMap` and `WeakSet` for memory-sensitive scenarios

## Testing

### Test Organization
- Organize tests to mirror source structure
- Use descriptive test names

### Test Coverage
- Aim for high test coverage
- Test edge cases and errors

### Testing Tools
- Recommended tools: **Jest** for testing, **ESLint** for linting, **Prettier** for formatting

## Tools and Configuration

### Linting and Formatting
- Use ESLint with standard rules
- Configure formatting rules in Prettier
```json
// Example ESLint configuration
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 12,
    "sourceType": "module"
  },
  "plugins": ["@typescript-eslint"],
  "rules": {}
}
```

### Prettier Configuration
```
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100
}
```

## Continuous Integration

### Recommended Setup
- Use a CI/CD platform to automate testing
- Run linting and tests as part of the build process

### Example CI Configuration (GitHub Actions)
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - run: npm install
    - run: npm test
    - run: npm run lint
```
