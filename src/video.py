import json
import random
import subprocess
from pathlib import Path

from PIL import Image

from .subtitles import SubtitleRenderer


class VideoRenderer:

    def __init__(
        self,
        width: int,
        height: int,
        fps: int,
    ):
        self.width = width
        self.height = height
        self.fps = fps

        self.subtitle_renderer = SubtitleRenderer(
            width,
            height,
        )

    # --------------------------------------------------
    # Get media duration
    # --------------------------------------------------

    def get_duration(
        self,
        path: Path,
    ) -> float:

        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())

    # --------------------------------------------------
    # Choose random background starting point
    # --------------------------------------------------

    def choose_random_start(
        self,
        background_duration: float,
        required_duration: float,
    ) -> float:

        if background_duration <= required_duration:
            return 0.0

        max_start = (
            background_duration
            - required_duration
        )

        return random.uniform(
            0.0,
            max_start,
        )

    # --------------------------------------------------
    # Load subtitle timings
    # --------------------------------------------------

    def load_timings(
        self,
        timing_path: Path,
    ) -> list[dict]:

        with open(
            timing_path,
            "r",
            encoding="utf-8",
        ) as f:

            timings = json.load(f)

        if not isinstance(timings, list):
            raise ValueError(
                "Subtitle timing file does not contain a list."
            )

        print(
            f"Loaded {len(timings)} subtitle timings."
        )

        if timings:
            print(
                "First timing:",
                timings[0],
            )

            print(
                "Last timing:",
                timings[-1],
            )

        else:
            print(
                "WARNING: Subtitle timing file is EMPTY."
            )

        return timings

    # --------------------------------------------------
    # Render video
    # --------------------------------------------------

    def render(
        self,
        background_path: Path,
        audio_path: Path,
        timing_path: Path,
        output_path: Path,
    ):

        # ----------------------------------------------
        # Get durations
        # ----------------------------------------------

        audio_duration = self.get_duration(
            audio_path
        )

        background_duration = self.get_duration(
            background_path
        )

        # ----------------------------------------------
        # Choose random background section
        # ----------------------------------------------

        start_time = self.choose_random_start(
            background_duration,
            audio_duration,
        )

        print(
            f"Background duration: "
            f"{background_duration:.2f}s"
        )

        print(
            f"Story duration: "
            f"{audio_duration:.2f}s"
        )

        print(
            f"Random background start: "
            f"{start_time:.2f}s"
        )

        # ----------------------------------------------
        # Load subtitle timings
        # ----------------------------------------------

        timings = self.load_timings(
            timing_path
        )

        # ----------------------------------------------
        # Frame size
        # ----------------------------------------------

        frame_size = (
            self.width
            * self.height
            * 3
        )

        # ----------------------------------------------
        # Decode Minecraft background
        # ----------------------------------------------

        decoder_command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",

            # Random starting position
            "-ss",
            str(start_time),

            "-i",
            str(background_path),

            # Only decode as long as narration
            "-t",
            str(audio_duration),

            # Vertical Shorts format
            "-vf",
            (
                f"scale={self.width}:{self.height}:"
                "force_original_aspect_ratio=increase,"
                f"crop={self.width}:{self.height}"
            ),

            "-r",
            str(self.fps),

            "-f",
            "rawvideo",

            "-pix_fmt",
            "rgb24",

            "pipe:1",
        ]

        decoder = subprocess.Popen(
            decoder_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # ----------------------------------------------
        # Encode final video
        # ----------------------------------------------

        encoder_command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",

            # Input: processed raw frames
            "-f",
            "rawvideo",

            "-pix_fmt",
            "rgb24",

            "-s",
            f"{self.width}x{self.height}",

            "-r",
            str(self.fps),

            "-i",
            "pipe:0",

            # Input: narration
            "-i",
            str(audio_path),

            # Final duration
            "-t",
            str(audio_duration),

            # Video stream
            "-map",
            "0:v:0",

            # Audio stream
            "-map",
            "1:a:0",

            # Video encoding
            "-c:v",
            "libx264",

            "-preset",
            "medium",

            "-crf",
            "20",

            # Audio encoding
            "-c:a",
            "aac",

            "-b:a",
            "192k",

            "-pix_fmt",
            "yuv420p",

            # Stop when shortest input ends
            "-shortest",

            str(output_path),
        ]

        encoder = subprocess.Popen(
            encoder_command,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # ----------------------------------------------
        # Rendering loop
        # ----------------------------------------------

        total_frames = int(
            audio_duration * self.fps
        )

        frame_number = 0

        # Used only for debugging subtitle rendering
        subtitle_was_drawn = False

        try:

            while True:

                raw_frame = decoder.stdout.read(
                    frame_size
                )

                # No more frames
                if len(raw_frame) != frame_size:
                    break

                # --------------------------------------
                # Convert raw frame → PIL image
                # --------------------------------------

                frame = Image.frombytes(
                    "RGB",
                    (
                        self.width,
                        self.height,
                    ),
                    raw_frame,
                )

                # --------------------------------------
                # Current narration time
                # --------------------------------------

                current_time = (
                    frame_number
                    / self.fps
                )

                # --------------------------------------
                # Draw subtitle
                # --------------------------------------

                frame = (
                    self.subtitle_renderer.draw(
                        frame,
                        timings,
                        current_time,
                    )
                )

                # --------------------------------------
                # Check whether subtitle timing exists
                # --------------------------------------

                if (
                    not subtitle_was_drawn
                    and timings
                ):

                    first = timings[0]

                    if (
                        first["start"]
                        <= current_time
                        <= first["end"]
                    ):

                        subtitle_was_drawn = True

                        print(
                            f"\nSubtitle rendering started "
                            f"at {current_time:.2f}s"
                        )

                # --------------------------------------
                # Send frame to FFmpeg encoder
                # --------------------------------------

                encoder.stdin.write(
                    frame.tobytes()
                )

                frame_number += 1

                # --------------------------------------
                # Progress
                # --------------------------------------

                if (
                    frame_number % self.fps == 0
                ):

                    progress = (
                        frame_number
                        / max(total_frames, 1)
                    ) * 100

                    print(
                        f"\rRendering: "
                        f"{progress:5.1f}%",
                        end="",
                        flush=True,
                    )

        finally:

            # ------------------------------------------
            # Close decoder
            # ------------------------------------------

            if decoder.stdout:
                decoder.stdout.close()

            # ------------------------------------------
            # Close encoder input
            # ------------------------------------------

            if encoder.stdin:
                encoder.stdin.close()

            # ------------------------------------------
            # Wait for processes
            # ------------------------------------------

            decoder.wait()
            encoder.wait()

        print()

        # ----------------------------------------------
        # Check encoder
        # ----------------------------------------------

        if encoder.returncode != 0:

            error = (
                encoder.stderr.read()
                .decode(
                    "utf-8",
                    errors="replace",
                )
            )

            raise RuntimeError(
                f"FFmpeg encoding failed:\n{error}"
            )

        # ----------------------------------------------
        # Check decoder
        # ----------------------------------------------

        if decoder.returncode != 0:

            error = (
                decoder.stderr.read()
                .decode(
                    "utf-8",
                    errors="replace",
                )
            )

            raise RuntimeError(
                f"FFmpeg decoding failed:\n{error}"
            )

        # ----------------------------------------------
        # Final diagnostics
        # ----------------------------------------------

        print(
            f"Frames rendered: {frame_number}"
        )

        print(
            f"Random segment used: "
            f"{start_time:.2f}s → "
            f"{start_time + audio_duration:.2f}s"
        )

        if not timings:

            print(
                "WARNING: No subtitle timings were available."
            )

        elif not subtitle_was_drawn:

            print(
                "WARNING: Subtitle timings exist, "
                "but no subtitle was active during rendering."
            )

        else:

            print(
                "Subtitle rendering: OK"
            )

        print(
            f"Output: {output_path}"
        )