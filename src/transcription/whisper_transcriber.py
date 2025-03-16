import os
import torch
import whisper
import numpy as np
from datetime import datetime

# 导入我们的修补模块
from src.transcription.whisper_patch import patch_whisper_ffmpeg, install_ffmpeg

# 尝试安装和修补ffmpeg
install_ffmpeg()
WHISPER_PATCHED = patch_whisper_ffmpeg()

class WhisperTranscriber:
    """
    A class for transcribing audio using OpenAI's Whisper model.
    """
    
    def __init__(self, model_size="base"):
        """
        Initialize the Whisper transcriber with a specified model size.
        
        Args:
            model_size (str): Size of the Whisper model to use.
                             Options: "tiny", "base", "small", "medium", "large"
        """
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # 检查是否成功修补了whisper
        if WHISPER_PATCHED:
            print("Whisper has been patched to use the correct ffmpeg path")
        else:
            print("WARNING: Failed to patch Whisper. Transcription may fail.")
        
        print(f"Loading Whisper {model_size} model on {self.device}...")
        self.model = whisper.load_model(model_size, device=self.device)
        print(f"Whisper {model_size} model loaded successfully!")
    
    def transcribe(self, audio_path):
        """
        Transcribe audio from a file path.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            # 直接设置ffmpeg路径
            try:
                import imageio_ffmpeg
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                print(f"Setting ffmpeg path to: {ffmpeg_path}")
                # 设置环境变量
                os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ["PATH"]
                # 直接尝试运行ffmpeg
                import subprocess
                subprocess.run([ffmpeg_path, "-version"], check=True, capture_output=True)
                print("ffmpeg is available and working!")
            except Exception as e:
                print(f"Warning: Could not set ffmpeg path: {e}")
            
            # Transcribe using Whisper
            result = self.model.transcribe(audio_path, fp16=torch.cuda.is_available())
            return result["text"]
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"Error during transcription: {str(e)}"
    
    def get_model_info(self):
        """
        Get information about the current model.
        
        Returns:
            dict: Information about the model
        """
        return {
            "model_size": self.model_size,
            "device": self.device,
            "parameters": f"{self.model.dims.n_text_state:,}"
        }