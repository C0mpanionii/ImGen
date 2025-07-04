# Docker Setup for Anime Wallpaper Remaster

This Docker Compose setup provides a containerized environment for running the Anime Wallpaper Remaster application with GPU acceleration.

## Docker Compose Location Update

⚠️ **Important**: With recent Docker Desktop updates, `docker-compose` is now located in:
```
C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe
```

The Docker Desktop installer automatically adds this directory to the system PATH, so existing scripts continue to work without modification. All commands in this guide use the standard `docker compose` or `docker-compose` commands that rely on PATH resolution.

## Prerequisites

1. **Docker & Docker Compose**: Install Docker Desktop with Docker Compose
2. **NVIDIA Docker Runtime**: For GPU acceleration (Linux/WSL2 only)
   ```bash
   # Install nvidia-container-toolkit
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

## Quick Start

### 1. Basic Setup (Main Application Only)

```bash
# Build and start the main application
docker compose up --build

# Run in detached mode
docker compose up -d --build

# View logs
docker compose logs -f anime-wallpaper-remaster
```

### 2. With Optional Services

```bash
# Include web interface
docker compose --profile web up -d

# Include caching (Redis)
docker compose --profile cache up -d

# Include monitoring (Prometheus + Grafana)
docker compose --profile monitoring up -d

# All services
docker compose --profile web --profile cache --profile monitoring up -d
```

## Usage Examples

### Process a Single Image

```bash
# Copy your image to the input directory
cp your_image.jpg anime-wallpaper-remaster/input_images/

# Run the processing
docker compose exec anime-wallpaper-remaster python -m anime_wallpaper_remaster.main \
  /app/input/your_image.jpg \
  -o /app/output \
  --style anime \
  --strength 0.75

# Check the output
ls anime-wallpaper-remaster/output/
```

### Process a Directory of Images

```bash
# Copy images to input directory
cp -r /path/to/your/images/* anime-wallpaper-remaster/input_images/

# Run batch processing
docker compose exec anime-wallpaper-remaster python -m anime_wallpaper_remaster.main \
  /app/input \
  -o /app/output \
  --style anime \
  --strength 0.75

# Check processing report
cat anime-wallpaper-remaster/output/processing_report.json
```

### Interactive Shell

```bash
# Access the container shell
docker compose exec anime-wallpaper-remaster /bin/bash

# Run commands interactively
python -m anime_wallpaper_remaster.main --help
```

## Configuration

### Environment Variables

You can customize the application by modifying environment variables in `docker-compose.yml`:

```yaml
environment:
  - CUDA_VISIBLE_DEVICES=0  # GPU device to use
  - PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512  # Memory management
  - HF_HOME=/app/models/huggingface_cache  # Hugging Face cache location
```

### Volume Mounts

- `./anime-wallpaper-remaster/models:/app/models:rw` - Model storage
- `./anime-wallpaper-remaster/input_images:/app/input:rw` - Input images
- `./anime-wallpaper-remaster/output:/app/output:rw` - Output images

## Available Services

### Core Services

1. **anime-wallpaper-remaster**: Main application container
   - Port: 8080 (if web interface is added)
   - GPU acceleration enabled
   - Persistent model storage

### Optional Services (Profiles)

2. **web-interface** (profile: `web`)
   - Nginx-based web interface
   - Port: 80
   - Static file serving

3. **redis** (profile: `cache`)
   - Redis cache for model caching
   - Port: 6379
   - Persistent data storage

4. **prometheus** (profile: `monitoring`)
   - Metrics collection
   - Port: 9090

5. **grafana** (profile: `monitoring`)
   - Metrics visualization
   - Port: 3000
   - Default credentials: admin/admin

## Troubleshooting

### GPU Not Detected

```bash
# Check GPU availability in container
docker compose exec anime-wallpaper-remaster python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# Check NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:12.1-base-ubuntu22.04 nvidia-smi
```

### Memory Issues

```bash
# Monitor GPU memory usage
watch -n 1 nvidia-smi

# Adjust memory allocation in docker-compose.yml
environment:
  - PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256
```

### Model Download Issues

```bash
# Check model directory
docker compose exec anime-wallpaper-remaster ls -la /app/models/

# Download models manually
docker compose exec anime-wallpaper-remaster python -c "
from diffusers import StableDiffusionImg2ImgPipeline
pipeline = StableDiffusionImg2ImgPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')
"
```

## Clean Up

```bash
# Stop all services
docker compose down

# Remove volumes (WARNING: This will delete cached models)
docker compose down -v

# Remove images
docker compose down --rmi all
```

## Development

For development, you can mount the source code as a volume:

```bash
# The source code is already mounted as read-only
# Edit files on the host and restart the container
docker compose restart anime-wallpaper-remaster
```

## Performance Tips

1. **Model Caching**: Keep the models volume to avoid re-downloading models
2. **GPU Memory**: Adjust `PYTORCH_CUDA_ALLOC_CONF` based on your GPU memory
3. **Batch Processing**: Process multiple images at once for better efficiency
4. **Image Size**: Larger images require more GPU memory and processing time
