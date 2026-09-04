import random
import shutil
from pathlib import Path

from config import load_config
from src.story import StoryGenerator
from src.tts import TTSGenerator
from src.video import VideoRenderer


def clean_temp(temp_dir: Path):
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


def find_backgrounds(
    background_dir: Path,
) -> list[Path]:

    extensions = {
        ".mp4",
        ".mov",
        ".mkv",
        ".webm",
    }

    videos = []

    for path in background_dir.rglob("*"):

        if (
            path.is_file()
            and path.suffix.lower() in extensions
        ):
            videos.append(path)

    return videos


def main():

    config = load_config()

    print()
    print("====================================")
    print("       AI SHORTS GENERATOR")
    print("====================================")
    print()

    topic = input(
        "What should the story be about? "
    ).strip()

    if not topic:
        raise ValueError(
            "You must enter a topic."
        )

    clean_temp(config.temp_dir)

    # --------------------------------
    # 1. Generate story
    # --------------------------------

    print()
    print("[1/4] Generating story...")

    story_generator = StoryGenerator(
        config.gemini_api_key,
        config.gemini_model,
    )

    story = story_generator.generate(
        topic,
        config.story_min_words,
        config.story_max_words,
    )

    print()
    print("STORY:")
    print("------------------------------------")
    print(story)
    print("------------------------------------")

    # --------------------------------
    # 2. Generate voice
    # --------------------------------

    print()
    print("[2/4] Generating narration...")

    audio_path = (
        config.temp_dir
        / "narration.mp3"
    )

    timing_path = (
        config.temp_dir
        / "timings.json"
    )

    tts = TTSGenerator(
        config.tts_voice
    )

    tts.generate(
        story,
        audio_path,
        timing_path,
    )

    print("Narration complete.")

    # --------------------------------
    # 3. Pick background
    # --------------------------------

    print()
    print("[3/4] Selecting background...")

    backgrounds = find_backgrounds(
        config.background_dir
    )

    if not backgrounds:
        raise FileNotFoundError(
            "No background videos found.\n"
            "Put an MP4/MOV/WebM video inside "
            "backgrounds/."
        )

    background = random.choice(
        backgrounds
    )

    print(
        f"Using background: {background}"
    )

    # --------------------------------
    # 4. Render
    # --------------------------------

    print()
    print("[4/4] Rendering video...")

    output_path = (
        config.output_dir
        / "short.mp4"
    )

    renderer = VideoRenderer(
        config.video_width,
        config.video_height,
        config.fps,
    )

    renderer.render(
        background,
        audio_path,
        timing_path,
        output_path,
    )

    print()
    print("====================================")
    print("VIDEO COMPLETE")
    print("====================================")
    print()
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()