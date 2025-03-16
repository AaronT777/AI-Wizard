# AI-Wizard: Audio Transcription and Summarizer

An AI-powered application that allows you to upload audio files, transcribe them using OpenAI's Whisper model, and generate summaries of the transcribed content.

## Features

- **Audio File Upload**: Upload audio files in various formats (MP3, WAV, M4A, etc.)
- **Transcription**: Transcribe audio files using OpenAI's Whisper model
- **Summarization**: Generate concise summaries of the transcribed content
- **Save Results**: Save transcriptions and summaries to text files

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AI-Wizard.git
   cd AI-Wizard
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   TOGETHER_API_KEY=your_together_api_key
   ```

## Usage

1. Start the application:
   ```
   python main.py
   ```

2. Open the web interface in your browser (default: http://localhost:7860)

3. Upload an audio file, transcribe it, and generate a summary

## Configuration

You can customize the application by modifying the following parameters:

- `--model_size`: Whisper model size (tiny, base, small, medium, large)
- `--save_dir`: Directory to save transcriptions and summaries
- `--port`: Port for the web interface
- `--debug`: Enable debug mode

Example:
```
python main.py --model_size medium --port 8080
```

## Requirements

- Python 3.8+
- FFmpeg (automatically installed if not present)
- GPU with CUDA support (optional, for faster transcription)

## License

[MIT License](LICENSE)