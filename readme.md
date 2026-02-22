# AI Clip Creator

AI Clip Creator is an AI tool that automatically identifies and creates highlight clips from streams and videos without manual editing.

**Note:** This project is no longer being actively maintained.

## Features

- **Easy setup**: Installer provided for Windows and Docker images for other OSes.
- **Completely local and offline**: No external profiles or internet connection is required.
- **Handles videos of any length**: Choose between short YouTube videos or multi-hour Twitch VODs.
- **Complete web interface**: User-friendly front end for ease of use.

## Installation

### Requirements

- 32GB of free space
- 8GB RAM minimum, 16GB recommended
- NVIDIA GPU with CUDA support (heavily recommended, but not strictly required)

### Windows

1. Download the latest version under releases.
2. Extract the contents of the zip file.
3. Run the `installer.bat` file and wait for the installation to complete.
4. Launch the application with the `run.bat` file.
5. Access the web interface with `http://localhost:5000` or use the link.

### Docker

1. Install [Docker](https://docs.docker.com/engine/install/) if not already installed.
2. Pull the desired [image](https://hub.docker.com/r/vijax0/ai-clip-creator/tags) version from Docker Hub.
3. To run the CPU version, use: `docker run -p 5000:5000 vijax0/ai-clip-creator:<tagname>`.
4. To run the GPU version, use: `docker run --gpus all -p 5000:5000 vijax0/ai-clip-creator:<tagname>`.
5. Access the web interface with `http://localhost:5000` or use the link.

### Manual install

1. Clone the repository with `git clone https://github.com/Vijax0/ai-clip-creator`.
2. Download the models from the latest release.
3. Extract the contents of the downloaded folder into the `models` directory.
4. Install all requirements with `pip install -r requirements.txt`.
5. Install PyTorch. See [PyTorch's](https://pytorch.org/get-started/locally/?ajs_aid=a9037fe1-adf0-408d-a665-080a7a56d61d) installation page for more details, or use `pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu124`.
6. Start the application by running the `main.py` file.
7. Access the web interface with `http://localhost:5000` or use the link.

## License

This project is licensed under the [MIT License](LICENSE).
