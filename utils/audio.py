# Audio extraction and processing
import os
import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)

def extract_audio(video_path: str, output_path: str) -> Optional[str]:
    """
    Extract audio from a video file using ffmpeg
    
    Args:
        video_path: Path to the source video file
        output_path: Path where the audio should be saved
        
    Returns:
        Path to the extracted audio file or None if extraction failed
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Use ffmpeg to extract audio
        cmd = [
            'ffmpeg',
            '-i', video_path,  # Input file
            '-q:a', '0',       # Best quality
            '-map', 'a',       # Extract audio only
            '-y',              # Overwrite output file
            output_path        # Output file
        ]
        
        # Run the command
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        logger.info(f"Audio extracted from {video_path} to {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting audio from {video_path}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None