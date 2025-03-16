"""Transcription module for AI-Wizard."""

from src.transcription.whisper_transcriber import WhisperTranscriber
from src.transcription.whisper_patch import patch_whisper_ffmpeg, install_ffmpeg

__all__ = ['WhisperTranscriber', 'patch_whisper_ffmpeg', 'install_ffmpeg']