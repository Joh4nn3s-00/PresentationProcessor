# Transcription service using OpenAI's Whisper API
import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TranscriptionService:
    """Service for transcribing audio files using OpenAI's Whisper API"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or load from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OpenAI API key not found. Set OPENAI_API_KEY in .env file or pass it to the constructor.")
        
        self.base_url = "https://api.openai.com/v1/audio/transcriptions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def transcribe(
        self, 
        audio_path: str, 
        model: str = "whisper-1", 
        response_format: str = "verbose_json",
        timestamp_granularities: Optional[list] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Transcribe an audio file using OpenAI's Whisper API
        
        Args:
            audio_path: Path to the audio file
            model: Model to use for transcription
            response_format: Format of the response
            timestamp_granularities: Granularity of timestamps
            
        Returns:
            Transcription data or None if transcription failed
        """
        if not self.api_key:
            logger.error("Cannot transcribe: No API key provided")
            return None
        
        # Ensure the audio file exists
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None
        
        try:
            # Prepare the data for the API request
            data = {
                "model": model,
                "response_format": response_format
            }
            
            if timestamp_granularities:
                for granularity in timestamp_granularities:
                    data[f"timestamp_granularities[]"] = granularity
            
            # Prepare the files for the API request
            files = {
                "file": (os.path.basename(audio_path), open(audio_path, "rb"))
            }
            
            # Make the API request
            logger.info(f"Sending transcription request for {audio_path}")
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=data,
                files=files
            )
            
            # Close the file
            files["file"][1].close()
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info(f"Transcription successful for {audio_path}")
                return response.json()
            else:
                logger.error(f"Transcription failed with status code {response.status_code}: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return None
    
    def save_transcript(self, transcript: Dict[str, Any], output_path: str) -> str:
        """
        Save a transcript to a file
        
        Args:
            transcript: Transcript data
            output_path: Path where to save the transcript
            
        Returns:
            Path to the saved transcript
        """
        try:
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write transcript to file
            with open(output_path, "w") as f:
                json.dump(transcript, f, indent=2)
            
            logger.info(f"Transcript saved to {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error saving transcript: {str(e)}")
            return ""