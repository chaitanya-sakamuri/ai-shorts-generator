from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Config:
    gemini_api_key: str
    gemini_model: str

    tts_voice: str

    video_width: int
    video_height: int
    fps: int

    story_min_words: int
    story_max_words: int

    background_dir: Path
    output_dir: Path
    temp_dir: Path


def load_config() -> Config:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "YOUR_KEY_HERE":
        raise ValueError(
            "GEMINI_API_KEY is missing. Add your Gemini API key to .env"
        )

    config = Config(
        gemini_api_key=api_key,
        gemini_model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        ),

        tts_voice=os.getenv(
            "TTS_VOICE",
            "en-US-BrianNeural"
        ),

        video_width=int(
            os.getenv("VIDEO_WIDTH", "1080")
        ),

        video_height=int(
            os.getenv("VIDEO_HEIGHT", "1920")
        ),

        fps=int(
            os.getenv("FPS", "30")
        ),

        story_min_words=int(
            os.getenv("STORY_MIN_WORDS", "110")
        ),

        story_max_words=int(
            os.getenv("STORY_MAX_WORDS", "140")
        ),

        background_dir=Path(
            os.getenv("BACKGROUND_DIR", "backgrounds")
        ),

        output_dir=Path(
            os.getenv("OUTPUT_DIR", "output")
        ),

        temp_dir=Path(
            os.getenv("TEMP_DIR", "temp")
        ),
    )

    config.background_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    config.output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    config.temp_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return config