# AI Clip Creator

AI Clip Creator is an AI tool that automatically identifies and creates highlight clips from streams and videos without manual editing.

**Note:** This is an early prototype and may not function as intended.

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
3. Run the `install-windows.bat` file and wait for the installation to complete.
4. Launch the application with the `run.bat` file.
5. Access the front end with `http://localhost:5000` or use the link.

### Docker

1. Install [Docker](https://docs.docker.com/engine/install/) if not already installed.
2. Pull the [latest](https://hub.docker.com/r/vijax0/ai-clip-creator/tags) image from Docker hub.
3. Run with port 5000 exposed: `docker run -p 5000:5000 vijax0/ai-clip-creator:tagname`.
4. Access the web interface with `http://localhost:5000` or use the link.

## Contributing

Contributions of all kinds are welcome. If you encounter any issues or have any feedback, do not be afraid to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
