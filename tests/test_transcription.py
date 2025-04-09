#!/usr/bin/env python
# Test script for audio transcription

import os
import sys
import json
import logging
from pathlib import Path

# Add the project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.transcription import TranscriptionService
from services.metadata import MetadataManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Check if we have an API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment. Please set it in .env file.")
        return 1
    
    # Initialize the metadata manager
    metadata_manager = MetadataManager()
    
    # Get all videos in metadata
    metadata = metadata_manager._read_metadata()
    if not metadata["videos"]:
        logger.error("No videos found in metadata. Please run test_audio_extraction.py first.")
        return 1
    
    # Get the first video from metadata
    video_id = next(iter(metadata["videos"]))
    video_metadata = metadata["videos"][video_id]
    
    logger.info(f"Using video: {video_metadata['original_filename']} (ID: {video_id})")
    
    # Check if the video has an audio path
    if not video_metadata.get("audio_path"):
        logger.error(f"No audio path found for video {video_id}. Please run test_audio_extraction.py first.")
        return 1
    
    audio_path = video_metadata["audio_path"]
    logger.info(f"Using audio file: {audio_path}")
    
    # Create the output path for transcript
    original_filename = video_metadata["original_filename"]
    transcript_filename = f"{os.path.splitext(original_filename)[0]}_transcript.json"
    transcript_path = os.path.join("data/transcripts", transcript_filename)
    
    # Initialize transcription service
    transcription_service = TranscriptionService()
    
    # Transcribe the audio
    logger.info("Starting transcription...")
    transcript = transcription_service.transcribe(
        audio_path=audio_path,
        timestamp_granularities=["segment"]
    )
    
    if not transcript:
        logger.error("Transcription failed.")
        return 1
    
    # Save the transcript
    output_path = transcription_service.save_transcript(transcript, transcript_path)
    
    if not output_path:
        logger.error("Failed to save transcript.")
        return 1
    
    # Update metadata with transcript path
    metadata_manager.update_metadata(video_id, {"transcript_path": transcript_path})
    
    # Show the updated metadata
    updated_metadata = metadata_manager.get_video_metadata(video_id)
    logger.info(f"Updated metadata: {updated_metadata}")
    
    # Sample of transcript content
    try:
        transcript_text = transcript.get("text", "")
        segments_count = len(transcript.get("segments", []))
        logger.info(f"Transcript has {segments_count} segments")
        logger.info(f"First 200 characters: {transcript_text[:200]}...")
    except Exception as e:
        logger.error(f"Error displaying transcript sample: {str(e)}")
    
    logger.info(f"Transcription successful! Saved to {transcript_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())