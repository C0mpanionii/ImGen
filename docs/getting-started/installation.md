# Installation Guide

This guide provides detailed instructions for installing and setting up the Image Generation Workspace on different platforms.

## 🖥️ System Requirements

### Minimum Requirements
- **OS:** Windows 10+, macOS 12+, or Linux (Ubuntu 20.04+)
- **CPU:** Intel i5-8400 / AMD Ryzen 5 2600 or equivalent
- **RAM:** 8GB (16GB recommended)
- **Storage:** 50GB free space
- **Python:** 3.8 or newer

### Recommended Requirements
- **GPU:** NVIDIA GTX 1060 6GB / RTX 3060 or better
- **VRAM:** 8GB+ for optimal performance
- **CUDA:** 11.8 or newer
- **RAM:** 16GB+
- **Storage:** SSD with 100GB+ free space

## 📦 Installation Methods

### Method 1: Local Python Installation

#### Step 1: Install Python Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd image-generation-workspace

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Install CUDA (Optional but Recommended)

=== "Windows"
    
    1. Download CUDA Toolkit from [NVIDIA's website](https://developer.nvidia.com/cuda-downloads)
    2. Install the toolkit following the installer prompts
    3. Verify installation:
    ```cmd
    nvcc --version
    nvidia-smi
    ```

=== "Linux"
    
    ```bash
    # Ubuntu/Debian
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
    sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
    sudo dpkg -i cuda-repo-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
    sudo cp /var/cuda-repo-ubuntu2004-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda
    ```

=== "macOS"
    
    !!! info "macOS Note"
        CUDA is not available on macOS. The system will fall back to CPU processing or Metal Performance Shaders if available.

#### Step 3: Configure the Environment

```bash
# Set up anime wallpaper remaster
cd anime-wallpaper-remaster
python install.py

# Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Method 2: Docker Installation

#### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- NVIDIA Container Toolkit (for GPU support)

#### Step 1: Install Docker

=== "Windows"
    
    1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
    2. Install and restart your computer
    3. Enable WSL 2 integration if prompted

=== "Linux"
    
    ```bash
    # Ubuntu/Debian
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.15.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    ```

=== "macOS"
    
    1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
    2. Install the .dmg file
    3. Start Docker Desktop

#### Step 2: Install NVIDIA Container Toolkit (GPU Support)

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

#### Step 3: Run with Docker

```bash
# Clone and start
git clone <repository-url>
cd image-generation-workspace

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
curl http://localhost:8080/health
```

### Method 3: Pre-built Releases

1. Go to the [Releases page](https://github.com/your-username/image-generation-workspace/releases)
2. Download the latest `image-generation-workspace-vX.X.X-complete.tar.gz`
3. Extract the archive:
   ```bash
   tar -xzf image-generation-workspace-vX.X.X-complete.tar.gz
   cd release-bundle
   ```
4. Follow the README instructions in the bundle

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# GPU Configuration
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST="7.5;8.0;8.6"

# Memory Settings
MAX_GPU_MEMORY=8GB
BATCH_SIZE=1

# Model Configuration
MODEL_CACHE_DIR=./models
HUGGINGFACE_CACHE_DIR=./cache

# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=1

# Security
SECRET_KEY=your-secret-key-here
DEBUG=false
```

### Model Configuration

The system will automatically download required models on first run. To pre-download:

```bash
python -c "
from huggingface_hub import snapshot_download
snapshot_download('runwayml/stable-diffusion-v1-5', cache_dir='./models')
"
```

## 🧪 Verification

### Test Basic Functionality

```bash
# Test Python installation
python -c "import anime_wallpaper_remaster; print('✅ Installation successful')"

# Test GPU availability
python -c "import torch; print(f'✅ CUDA available: {torch.cuda.is_available()}')"

# Test API server
curl http://localhost:8080/health
```

### Test Docker Installation

```bash
# Check containers
docker-compose ps

# Test API
curl http://localhost:8080/health

# Check logs for errors
docker-compose logs app
```

## 🚨 Troubleshooting

### Common Issues

#### "CUDA out of memory"
- Reduce batch size in configuration
- Close other GPU-intensive applications
- Use smaller models for testing

#### "Model download fails"
- Check internet connection
- Verify Hugging Face access
- Set up authentication tokens if needed

#### "Docker permission denied"
- Add user to docker group: `sudo usermod -aG docker $USER`
- Restart terminal session
- On Windows, ensure Docker Desktop is running

#### "Port already in use"
- Change ports in docker-compose.yml
- Stop conflicting services: `sudo lsof -i :8080`

### Getting Help

If you encounter issues:

1. Check the [FAQ](../reference/faq.md)
2. Search [existing issues](https://github.com/your-username/image-generation-workspace/issues)
3. Create a new issue with:
   - System information
   - Error messages
   - Steps to reproduce

## ✅ Next Steps

After successful installation:

1. **[Quick Start Guide](quick-start.md)** - Run your first image enhancement
2. **[Configuration Reference](../reference/configuration.md)** - Customize settings
3. **[Development Setup](../development/setup.md)** - Set up for development
