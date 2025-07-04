# Dockerfile for MkDocs documentation
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /docs

# Install MkDocs and plugins
RUN pip install --no-cache-dir \
    mkdocs-material>=9.0.0 \
    mkdocs-git-revision-date-localized-plugin>=1.2.0 \
    mkdocs-minify-plugin>=0.6.0 \
    mkdocs-mermaid2-plugin>=0.6.0

# Copy documentation files
COPY . .

# Build the documentation
RUN mkdocs build --clean --strict

# Expose port
EXPOSE 8000

# Command to serve documentation
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
