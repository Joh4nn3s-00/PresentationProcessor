# Service to maintain the centralized metadata
import os
import json
import uuid
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Path to the metadata file
METADATA_FILE = "data/metadata.json"

logger = logging.getLogger(__name__)

class VideoMetadata(BaseModel):
    """Model for video metadata"""
    video_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    original_filename: str
    video_path: str
    audio_path: Optional[str] = None
    transcript_path: Optional[str] = None
    screenshots: List[str] = Field(default_factory=list)
    analyses: Dict[str, str] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class MetadataManager:
    """Manager for handling video metadata"""
    
    def __init__(self, metadata_file: str = METADATA_FILE):
        self.metadata_file = metadata_file
        self._ensure_metadata_file()
    
    def _ensure_metadata_file(self) -> None:
        """Ensure the metadata file exists"""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        if not os.path.exists(self.metadata_file):
            # Initialize with empty videos dictionary
            with open(self.metadata_file, 'w') as f:
                json.dump({"videos": {}}, f, indent=2)
        else:
            # Check if the file has the correct structure
            try:
                with open(self.metadata_file, 'r') as f:
                    data = json.load(f)
                if "videos" not in data:
                    # Fix the structure
                    data["videos"] = {}
                    with open(self.metadata_file, 'w') as f:
                        json.dump(data, f, indent=2)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, recreate it
                with open(self.metadata_file, 'w') as f:
                    json.dump({"videos": {}}, f, indent=2)
    
    def _read_metadata(self) -> Dict[str, Any]:
        """Read the metadata from file"""
        try:
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
                if "videos" not in data:
                    data["videos"] = {}
                return data
        except json.JSONDecodeError:
            logger.error(f"Error reading metadata file. Creating new metadata.")
            return {"videos": {}}
    
    def _write_metadata(self, data: Dict[str, Any]) -> None:
        """Write metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_video(self, user_id: str, video_path: str) -> str:
        """
        Register a new video and return its ID
        
        Args:
            user_id: ID of the user who uploaded the video
            video_path: Path to the video file
            
        Returns:
            The generated video ID
        """
        # Create metadata for the new video
        original_filename = os.path.basename(video_path)
        video_metadata = VideoMetadata(
            user_id=user_id,
            original_filename=original_filename,
            video_path=video_path
        )
        
        # Add to metadata store
        metadata = self._read_metadata()
        metadata["videos"][video_metadata.video_id] = video_metadata.model_dump()
        self._write_metadata(metadata)
        
        logger.info(f"Registered video {original_filename} with ID {video_metadata.video_id}")
        return video_metadata.video_id
    
    def update_metadata(self, video_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update the metadata for a video
        
        Args:
            video_id: ID of the video to update
            data: New data to update
            
        Returns:
            Updated metadata or None if video not found
        """
        metadata = self._read_metadata()
        
        if video_id not in metadata["videos"]:
            logger.error(f"Video with ID {video_id} not found")
            return None
        
        # Update the metadata
        metadata["videos"][video_id].update(data)
        metadata["videos"][video_id]["updated_at"] = datetime.now().isoformat()
        
        # Write back to file
        self._write_metadata(metadata)
        
        logger.info(f"Updated metadata for video {video_id}")
        return metadata["videos"][video_id]
    
    def get_video_metadata(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific video
        
        Args:
            video_id: ID of the video
            
        Returns:
            Video metadata or None if not found
        """
        metadata = self._read_metadata()
        
        if video_id not in metadata["videos"]:
            logger.error(f"Video with ID {video_id} not found")
            return None
        
        return metadata["videos"][video_id]
    
    def get_user_videos(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all videos for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            List of video metadata
        """
        metadata = self._read_metadata()
        
        # Filter videos by user_id
        user_videos = [
            video for video in metadata["videos"].values()
            if video["user_id"] == user_id
        ]
        
        return user_videos