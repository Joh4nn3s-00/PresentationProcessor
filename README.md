# Sales Pitch Analyzer

A tool for processing, transcribing, and analyzing sales pitch videos.

## Project Structure

```
sales-pitch-analyzer/
├── app/                 # Main application
│   ├── __init__.py
│   ├── main.py          # Entry point
│   └── config.py        # Configuration settings
├── services/            # Core services for different functionalities
│   ├── __init__.py
│   ├── transcription.py # Handles video-to-transcript using Whisper
│   ├── screenshot.py    # Extracts screenshots at key moments
│   ├── analysis/        # Different analysis modules
│   │   ├── __init__.py
│   │   ├── base.py      # Base analyzer class
│   │   ├── pace.py      # Pace analysis
│   │   ├── terminology.py # Terminology analysis
│   │   └── visual.py    # Visual presentation analysis
│   ├── comparison.py    # For comparing multiple video submissions
│   └── metadata.py      # Service to maintain the centralized metadata
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── ai_clients.py    # OpenAI, Together, Gemini client wrappers
│   ├── video.py         # Video processing utilities
│   ├── audio.py         # Audio extraction and processing
│   └── storage.py       # Temporary storage solutions
├── data/                # For storing temporary data
│   ├── videos/          # Original uploaded videos
│   ├── audio/           # Extracted audio files
│   ├── transcripts/     # Generated transcripts
│   ├── screenshots/     # Extracted screenshots
│   ├── analyses/        # Analysis results
│   └── metadata.json    # Centralized metadata tracking all relationships
├── tests/               # Tests for modules
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

## Setup

1. Create the conda environment:
```bash
conda create -n PresentationProcessor python=3.10
conda activate PresentationProcessor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

## Current Functionality

- Audio extraction from video files
- Transcript generation using OpenAI's Whisper API
- Metadata management for tracking processing steps

## Development

The project is structured with clear separation of concerns between data, application code, and utilities.