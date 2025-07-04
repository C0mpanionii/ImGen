# Contributing Guidelines

Thank you for your interest in contributing to this project! This document outlines the process and requirements for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch from `main` for your changes
4. Make your changes following our coding standards
5. Test your changes thoroughly
6. Submit a pull request

## Branch Policy

- **Main Branch**: `main`
- All pull requests must target the `main` branch
- Feature branches should be named descriptively (e.g., `feature/add-user-auth`, `fix/login-bug`)
- Branch names should use kebab-case

## Commit Requirements

### GPG Signing
All commits **must** be GPG-signed. This ensures the authenticity and integrity of your contributions.

To set up GPG signing:
1. Generate a GPG key if you don't have one
2. Add your GPG key to your GitHub account
3. Configure Git to sign commits by default:
   ```bash
   git config --global commit.gpgsign true
   git config --global user.signingkey YOUR_GPG_KEY_ID
   ```

### Conventional Commits
We use the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages. This helps with automated changelog generation and semantic versioning.

#### Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries

#### Examples
```
feat(auth): add OAuth2 authentication
fix(api): resolve user session timeout issue
docs(readme): update installation instructions
style(linting): fix code formatting issues
refactor(utils): simplify helper functions
test(auth): add unit tests for login flow
chore(deps): update dependency versions
```

## Code Style

Please refer to our style guides in the `styleguides/` directory for language-specific coding standards.

## Pull Request Process

1. Ensure your code follows our style guidelines
2. Update documentation if necessary
3. Add tests for new functionality
4. Ensure all tests pass
5. Update the changelog if your changes are user-facing
6. Submit a pull request with a clear description of your changes

### Pull Request Template
- **Description**: What changes does this PR introduce?
- **Type**: Feature, Bug fix, Documentation, etc.
- **Testing**: How was this tested?
- **Breaking Changes**: Are there any breaking changes?
- **Related Issues**: Link to any related issues

## Code Review

All submissions require code review. We use GitHub pull requests for this purpose. Reviewers will check for:

- Code quality and adherence to style guidelines
- Test coverage
- Documentation updates
- GPG-signed commits
- Proper commit message format

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
