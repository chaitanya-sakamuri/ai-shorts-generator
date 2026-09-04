import asyncio
import json
from pathlib import Path

import edge_tts


class TTSGenerator:

    def __init__(
        self,
        voice: str,
    ):
        self.voice = voice

    async def _generate(
        self,
        text: str,
        audio_path: Path,
        timing_path: Path,
    ):

        # IMPORTANT:
        # Explicitly request WORD-level timing.
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="+25%",
            pitch="+1Hz",
            boundary="WordBoundary",
        )

        timings = []

        with open(
            audio_path,
            "wb",
        ) as audio_file:

            async for message in communicate.stream():

                # --------------------------------------
                # Audio data
                # --------------------------------------

                if message["type"] == "audio":

                    audio_file.write(
                        message["data"]
                    )

                # --------------------------------------
                # Word timing
                # --------------------------------------

                elif message["type"] == "WordBoundary":

                    offset = (
                        message["offset"]
                        / 10_000_000
                    )

                    duration = (
                        message["duration"]
                        / 10_000_000
                    )

                    timings.append(
                        {
                            "word": message["text"],
                            "start": offset,
                            "end": offset + duration,
                        }
                    )

        # ----------------------------------------------
        # Save word timings
        # ----------------------------------------------

        with open(
            timing_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                timings,
                f,
                indent=2,
                ensure_ascii=False,
            )

        # ----------------------------------------------
        # Diagnostics
        # ----------------------------------------------

        print(
            f"Generated {len(timings)} word timings."
        )

        if timings:

            print(
                f"First word: "
                f"{timings[0]['word']} "
                f"({timings[0]['start']:.2f}s)"
            )

            print(
                f"Last word: "
                f"{timings[-1]['word']} "
                f"({timings[-1]['end']:.2f}s)"
            )

        else:

            print(
                "WARNING: Edge TTS returned no word timings."
            )

    def generate(
        self,
        text: str,
        audio_path: Path,
        timing_path: Path,
    ):

        # Remove old files
        if audio_path.exists():
            audio_path.unlink()

        if timing_path.exists():
            timing_path.unlink()

        asyncio.run(
            self._generate(
                text,
                audio_path,
                timing_path,
            )
        )