#!/usr/bin/env python
# Test script for audio extraction

import os
import sys
import logging
import argparse
from pathlib import Path

# Add the project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.audio import extract_audio
from services.metadata import MetadataManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Sample user ID
    user_id = "test_user"
    
    # Get the first video file in the videos directory
    videos_dir = Path("data/videos")
    video_files = list(videos_dir.glob("*"))
    
    if not video_files:
        logger.error("No video files found in data/videos directory")
        return 1
    
    # Use the first video file
    video_path = str(video_files[0])
    logger.info(f"Using video file: {video_path}")
    
    # Initialize metadata manager
    metadata_manager = MetadataManager()
    
    # Register the video
    video_id = metadata_manager.register_video(user_id, video_path)
    logger.info(f"Video registered with ID: {video_id}")
    
    # Create the output path for audio
    original_filename = os.path.basename(video_path)
    audio_filename = f"{os.path.splitext(original_filename)[0]}.mp3"
    audio_path = os.path.join("data/audio", audio_filename)
    
    # Extract audio
    result = extract_audio(video_path, audio_path)
    
    if result:
        logger.info(f"Audio extracted successfully to: {audio_path}")
        
        # Update metadata with audio path
        metadata_manager.update_metadata(video_id, {"audio_path": audio_path})
        
        # Show the updated metadata
        updated_metadata = metadata_manager.get_video_metadata(video_id)
        logger.info(f"Updated metadata: {updated_metadata}")
        
        return 0
    else:
        logger.error("Audio extraction failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())