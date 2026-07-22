# Atelier AI – Architecture Studio

> **AI-Powered Architectural Design & Visualization**
> 
> Shape a house concept, draft planning studies, then turn the chosen direction into a refined architectural visualization — all in one integrated studio.

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Overview

**Atelier AI** is an innovative web-based architectural design tool powered by artificial intelligence. It combines creative ideation with AI-driven visual generation to help architects, designers, and homeowners explore architectural concepts from initial brief to final visualization.

The application guides users through a three-stage design process:
1. **Brief** – Define the dream home concept with mood, site, and signature spaces
2. **Plan** – Generate multiple floor plan options based on requirements
3. **Render** – Create photorealistic architectural visualizations

---

## ✨ Features

### 🏗️ Three-Stage Design Workflow
- **Stage 1: Project Brief** – Describe overall concepts, site context, and desired spaces
- **Stage 2: Plan Studio** – Input room requirements and generate 3 alternative floor plans
- **Stage 3: Visualization Atelier** – Select architectural style and render final exterior designs

### 🎨 AI-Powered Generation
- Text-to-image generation using **SDXL Turbo** model for high-speed outputs
- Intelligent prompt engineering for architectural-specific outputs
- Support for both floor plans (2D blueprints) and 3D renderings

### ⚡ GPU Acceleration
- Automatic GPU detection and optimization (CUDA, Metal Performance Shaders, or CPU fallback)
- Dynamic precision selection (fp16 on GPU, fp32 on CPU) for optimal performance
- Configurable inference steps for speed vs. quality tradeoff

### 🎭 Sophisticated UI Design
- **Custom Dark Theme** – Architectural blueprint aesthetic with copper accents
- **Responsive Layout** – Optimized for desktop and tablet screens
- **Professional Typography** – Uses Fraunces (serif), Inter (sans-serif), and JetBrains Mono (monospace)
- **Grid Background** – Subtle blueprint grid overlay for design authenticity
- **Interactive Stage Tracking** – Visual progress indicator through the design workflow

### 🔧 Environment Configuration
- Supports `.env` files for secure credential management
- Integration with OpenAI and Hugging Face APIs
- Flexible model selection and parameter tuning

---

## 🏛️ Architecture

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | [Streamlit](https://streamlit.io/) | Interactive web interface |
| **AI Model** | [SDXL Turbo](https://huggingface.co/stabilityai/sdxl-turbo) | Fast text-to-image generation |
| **Deep Learning** | [PyTorch](https://pytorch.org/) | ML framework and GPU support |
| **Model Hub** | [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/) | Pre-trained model access |
| **LLM Integration** | [OpenAI](https://openai.com/) | Optional: Advanced text generation |
| **Environment** | [python-dotenv](https://github.com/theskumar/python-dotenv) | Secure configuration |

### System Architecture

```
┌─────────────────────────────────────┐
│     Streamlit Web Interface         │
│  (Responsive UI with Custom CSS)    │
├─────────────────────────────────────┤
│   Application Logic (app.py)        │
│  - Stage Management                 │
│  - Prompt Engineering               │
│  - Session State Handling           │
├─────────────────────────────────────┤
│   AI Pipeline                       │
│  - Model Loading (SDXL Turbo)       │
│  - Image Generation (Diffusers)     │
│  - GPU Optimization (PyTorch)       │
├─────────────────────────────────────┤
│   External APIs                     │
│  - Hugging Face Hub                 │
│  - OpenAI (optional)                │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.10 or higher
- **GPU** (recommended): NVIDIA CUDA 11.8+ or Apple Silicon (Mac M1+)
- **Disk Space**: ~10-15GB (for model downloads)
- **RAM**: 8GB minimum (16GB+ recommended for optimal performance)
- **Internet**: Required for initial model downloads from Hugging Face

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Gen AI/AI AGENT"
```

#### 2. Create Virtual Environment
```bash
# Using venv (included with Python)
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
```bash
# Create .env file in project root
cp .env.example .env  # if available, or create manually

# Add your API keys (if using OpenAI integration)
echo "OPENAI_API_KEY=your_key_here" >> .env
echo "HUGGINGFACE_TOKEN=your_token_here" >> .env
```

#### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📖 Usage Guide

### Basic Workflow

#### **Stage 1: Project Brief**
1. Enter your dream home concept in the "House concept" text area
   - Example: *"A calm modern home with two floors, a roof pool, warm stone, open living spaces, and a small garden court."*
2. Click **"Start Planning →"** to proceed to Stage 2

#### **Stage 2: Plan Studio**
1. Define specific floor plan requirements
   - Specify rooms: bedrooms, bathrooms, kitchen, etc.
   - Describe relationships and flow between spaces
   - Example: *"5 bedrooms, 2 master suites, spacious dining room, open kitchen, family lounge"*
2. Click **"Draft 3 Plans →"** to generate three floor plan options
3. Review the generated 2D blueprint plans

#### **Stage 3: Visualization Atelier**
1. Describe your preferred architectural style
   - Include materials, aesthetic, and mood
   - Example: *"Minimal modern villa with warm natural materials, clean facade, elegant lighting, refined landscaping"*
2. Click **"Render Design →"** to generate photorealistic visualizations
3. Download or share the final renders

### Advanced Usage

#### Performance Tuning
```python
# In app.py, adjust generation parameters:
image = pipe(
    prompt=prompt,
    num_inference_steps=2,      # Lower = faster (1-4), Higher = better quality (5-20)
    guidance_scale=0.0,          # 0.0 = faster, 7-15 = more coherent
    height=512,                  # 256/512/768/1024 (requires more VRAM for larger)
    width=512,
    generator=generator,
).images[0]
```

#### GPU Selection
```python
# The app automatically selects:
# CUDA (NVIDIA GPUs) > MPS (Apple Silicon) > CPU
# To force CPU mode (for debugging):
device = "cpu"
```

#### Batch Processing
For generating multiple designs, modify the app to save prompts and outputs to a database or file system rather than displaying in Streamlit.

---

## ⚙️ Configuration

### Environment Variables (.env)

```ini
# Optional: OpenAI API Key
OPENAI_API_KEY=sk-...

# Optional: Hugging Face Token (for private models)
HUGGINGFACE_TOKEN=hf_...

# Optional: Model configuration
DIFFUSERS_CACHE=/path/to/models  # Model cache directory
```

### Streamlit Configuration (.streamlit/config.toml)

```toml
[client]
showErrorDetails = true

[logger]
level = "info"

[server]
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

---

## 📊 System Requirements

### Minimum Requirements
| Spec | Requirement |
|------|-------------|
| **CPU** | 4-core processor |
| **RAM** | 8GB |
| **Storage** | 15GB free space |
| **Python** | 3.10+ |
| **OS** | macOS, Linux, Windows 10+ |

### Recommended Requirements (GPU)
| Component | Recommendation |
|-----------|----------------|
| **GPU** | NVIDIA RTX 3060+ or Apple M1+ |
| **VRAM** | 6GB+ |
| **RAM** | 16GB+ |
| **Storage** | SSD with 20GB+ free |
| **Network** | High-speed internet (initial model download) |

### First Run Download Size
- SDXL Turbo model: ~8GB
- Other dependencies: ~2-3GB
- **Total**: ~10-15GB

---

## 🔧 Troubleshooting

### Common Issues

#### **Issue: CUDA out of memory**
```bash
# Solution 1: Reduce image resolution
# In app.py, change height/width to 256 or 384

# Solution 2: Reduce inference steps
num_inference_steps=1  # Fastest, lower quality

# Solution 3: Use CPU instead
device = "cpu"
```

#### **Issue: Model download fails**
```bash
# Clear model cache and re-download
rm -rf ~/.cache/huggingface
streamlit run app.py
```

#### **Issue: Streamlit port already in use**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

#### **Issue: Poor image quality**
- Increase `num_inference_steps` (up to 20)
- Increase `guidance_scale` (7-15)
- Be more specific in prompt descriptions
- Use high-quality reference terms: "professional," "realistic," "architectural photography"

#### **Issue: Apple Silicon not detected**
```bash
# Ensure PyTorch is built for ARM64
python -c "import torch; print(torch.backends.mps.is_available())"
# Should return True
```

### Debug Mode

```bash
# Run with verbose logging
streamlit run app.py --logger.level=debug
```

---

## 🎓 How It Works

### Image Generation Pipeline

```python
1. Text Input → User provides design brief/requirements
2. Prompt Engineering → App structures specific architectural prompt
3. Model Loading → SDXL Turbo loads on selected device (GPU/CPU)
4. Diffusion Process → 2-step diffusion for fast generation
5. Image Output → Generated image returned and displayed
```

### Prompt Engineering Strategy

The app uses specialized architectural prompts:
- **Floor Plans**: Blueprint style, top-down, white/black, technical accuracy
- **Renderings**: Photorealistic, 24mm photography, professional materials, lighting

### Performance Characteristics

| GPU | SDXL Turbo (512x512) | Speed |
|-----|----------------------|-------|
| NVIDIA RTX 4080 | ~0.5-1s | Very Fast |
| NVIDIA RTX 3060 | ~1-2s | Fast |
| Apple M1/M2 Max | ~2-3s | Fast |
| Apple M1/M2 | ~5-8s | Moderate |
| CPU (16-core) | ~30-60s | Slow |

---

## 📦 Project Structure

```
AI AGENT/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── env/                  # Python virtual environment
│   ├── bin/              # Executables and python
│   ├── lib/              # Python packages
│   └── pyvenv.cfg        # venv configuration
└── README.md             # This file
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and commit (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request** with a clear description

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black pylint pytest

# Format code
black app.py

# Lint code
pylint app.py
```

---

## 📝 License

This project is licensed under the **MIT License** – see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Stability AI** for the SDXL Turbo model
- **Hugging Face** for the Diffusers library and model hub
- **Streamlit** for the excellent web framework
- **PyTorch** and the deep learning community

---

## 📞 Support & Feedback

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Ask questions in Discussions
- **Documentation**: See [Streamlit Docs](https://docs.streamlit.io/)
- **Model Info**: [SDXL Turbo on Hugging Face](https://huggingface.co/stabilityai/sdxl-turbo)

---

## 🗺️ Roadmap

### Planned Features
- [ ] Multi-model support (Stable Diffusion 3, DALL-E 3)
- [ ] Design history and project management
- [ ] Collaborative design workspace
- [ ] Export to CAD formats (DWG, SKP)
- [ ] Interactive 3D model viewer
- [ ] Cost estimation and material suggestions
- [ ] Mobile app version
- [ ] Custom model fine-tuning

### Future Enhancements
- Real-time collaborative editing
- Integration with architectural software (Revit, SketchUp)
- AI-powered architectural analysis
- Sustainability and energy efficiency assessments

---

**Last Updated**: July 2026  
**Version**: 1.0.0  
**Maintained by**: AI Architecture Studio Team

---

*Transform your architectural dreams into reality with AI-powered design. Start building your perfect home today with Atelier AI.*
