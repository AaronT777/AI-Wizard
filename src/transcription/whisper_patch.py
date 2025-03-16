"""
修补whisper库以使用指定的ffmpeg路径
"""
import os
import sys
import subprocess
from pathlib import Path

def patch_whisper_ffmpeg():
    """
    修补whisper库以使用我们指定的ffmpeg路径
    """
    try:
        # 尝试从imageio_ffmpeg获取ffmpeg路径
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        if os.path.exists(ffmpeg_path):
            print(f"Found ffmpeg at: {ffmpeg_path}")
            
            # 直接修改whisper库中的ffmpeg路径
            import whisper
            import whisper.audio
            
            # 保存原始函数
            original_run_cmd = whisper.audio._run_cmd
            
            # 创建一个新函数，替换命令中的ffmpeg
            def patched_run_cmd(cmd, **kwargs):
                if cmd[0] == "ffmpeg":
                    cmd[0] = ffmpeg_path
                    print(f"Patched ffmpeg command: {cmd}")
                return original_run_cmd(cmd, **kwargs)
            
            # 替换函数
            whisper.audio._run_cmd = patched_run_cmd
            
            print("Successfully patched whisper to use imageio_ffmpeg")
            return True
        else:
            print(f"ffmpeg not found at {ffmpeg_path}")
            return False
    except ImportError:
        print("imageio_ffmpeg not installed, cannot patch whisper")
        return False
    except Exception as e:
        print(f"Error patching whisper: {str(e)}")
        return False

# 尝试安装ffmpeg
def install_ffmpeg():
    """
    尝试安装ffmpeg
    """
    try:
        # 检查系统是否有pip
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
        
        # 安装ffmpeg-python
        print("Installing ffmpeg-python...")
        subprocess.run([sys.executable, "-m", "pip", "install", "ffmpeg-python"], check=True)
        
        # 安装imageio-ffmpeg
        print("Installing imageio-ffmpeg...")
        subprocess.run([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"], check=True)
        
        print("ffmpeg packages installed successfully")
        return True
    except Exception as e:
        print(f"Error installing ffmpeg: {str(e)}")
        return False 