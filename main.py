import os
import argparse
from src.transcription.whisper_transcriber import WhisperTranscriber
from src.summarization.llm_summarizer import MeetingSummarizer
from src.ui.gradio_interface import create_interface

def parse_args():
    parser = argparse.ArgumentParser(description='Meeting Recorder and Summarizer')
    parser.add_argument('--model_size', default='base', choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size to use for transcription')
    parser.add_argument('--save_dir', default='./data/saved_meetings',
                        help='Directory to save meeting recordings and summaries')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # 确保存储目录存在
    os.makedirs(args.save_dir, exist_ok=True)
    
    # 初始化转录器
    transcriber = WhisperTranscriber(model_size=args.model_size)
    
    # 初始化摘要生成器
    # 当你的队友实现了Together API部分，可以解除下面代码的注释
    # from config import TOGETHER_API_KEY
    # from together import Together
    # client = Together(api_key=TOGETHER_API_KEY)
    # summarizer = MeetingSummarizer(client)
    
    # 使用占位符摘要生成器进行测试
    summarizer = MeetingSummarizer(None)  # 传入None表示使用占位符实现
    
    # 创建并启动界面
    interface = create_interface(transcriber, summarizer, save_dir=args.save_dir)
    interface.launch()

if __name__ == "__main__":
    main()