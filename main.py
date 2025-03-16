import os
import argparse
import gradio as gr
from datetime import datetime
import sys
import subprocess

# 尝试安装ffmpeg
def ensure_ffmpeg():
    """确保ffmpeg可用"""
    try:
        # 尝试运行ffmpeg命令
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        print("System ffmpeg is available")
        return True
    except:
        print("System ffmpeg not found, trying to install via pip...")
        try:
            # 安装imageio-ffmpeg
            subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"], check=True)
            
            # 设置环境变量
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            os.environ["PATH"] = os.environ["PATH"] + os.pathsep + os.path.dirname(ffmpeg_path)
            print(f"Added ffmpeg to PATH: {ffmpeg_path}")
            
            # 验证安装
            try:
                subprocess.run([ffmpeg_path, "-version"], check=True, capture_output=True)
                print("ffmpeg from imageio_ffmpeg is working")
                return True
            except:
                print(f"Failed to run {ffmpeg_path}")
                return False
        except Exception as e:
            print(f"Failed to install ffmpeg: {str(e)}")
            return False

# 确保ffmpeg可用
ensure_ffmpeg()

# Import our modules
from src.transcription.whisper_transcriber import WhisperTranscriber
from src.summarization.llm_summarizer import MeetingSummarizer
from src.ui.gradio_interface import create_interface

# Import configuration
from config import TOGETHER_API_KEY, DEFAULT_MODEL_SIZE, DEFAULT_SAVE_DIR

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Audio Transcription and Summarizer')
    parser.add_argument('--model_size', default=DEFAULT_MODEL_SIZE, 
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size to use for transcription')
    parser.add_argument('--save_dir', default=DEFAULT_SAVE_DIR,
                        help='Directory to save transcriptions and summaries')
    parser.add_argument('--port', type=int, default=7860,
                        help='Port for the Gradio web interface')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    return parser.parse_args()

def setup_environment(args):
    """Set up the environment for the application."""
    # Create directories if they don't exist
    os.makedirs(args.save_dir, exist_ok=True)
    
    # Set up logging
    if args.debug:
        import logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_args()
    
    # Set up environment
    setup_environment(args)
    
    print(f"Starting Audio Transcription with Whisper model: {args.model_size}")
    
    # Initialize the transcriber
    transcriber = WhisperTranscriber(model_size=args.model_size)
    
    # Initialize the summarizer
    # If API key is available, use the LLM for summarization
    if TOGETHER_API_KEY:
        from together import Together
        client = Together(api_key=TOGETHER_API_KEY)
        summarizer = MeetingSummarizer(client)
        print("Using Together AI for content summarization")
    else:
        # Use a placeholder summarizer that doesn't require API access
        summarizer = MeetingSummarizer(None)
        print("WARNING: No API key found. Using placeholder summarization.")
        print("For full functionality, set TOGETHER_API_KEY in .env file")
    
    # Create and launch the interface
    interface = create_interface(
        transcriber=transcriber,
        summarizer=summarizer,
        save_dir=args.save_dir
    )
    
    print(f"Launching web interface on port {args.port}")
    interface.launch(
        server_name="0.0.0.0",  # Make available on local network
        server_port=args.port,
        share=True              # Create a public link
    )

if __name__ == "__main__":
    main()