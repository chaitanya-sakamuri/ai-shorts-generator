import re
from google import genai


class StoryGenerator:

    def __init__(
        self,
        api_key: str,
        model: str,
    ):
        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

    # --------------------------------------------------
    # Generate story
    # --------------------------------------------------

    def generate(
        self,
        topic: str,
        min_words: int = 110,
        max_words: int = 140,
    ) -> str:

        prompt = f"""
Write a fictional story for a YouTube Short.

TOPIC:
{topic}

IMPORTANT:
The story MUST be between {min_words} and {max_words} words.

Aim for approximately 120 words.
DO NOT exceed {max_words} words.

STYLE:
- emotionally engaging
- conversational
- easy to understand
- fast-moving
- realistic
- dramatic
- curiosity-driven
- suitable for spoken narration

The first sentence MUST immediately create curiosity.

The story should involve some combination of:
- friendship
- betrayal
- love
- jealousy
- misunderstanding
- sacrifice
- revenge
- regret
- a surprising reveal

The story should feel like something a real person would tell someone.

Do NOT:
- use headings
- use bullet points
- add a title
- say "here's a story"
- explain the story afterward
- mention that you are an AI
- add commentary

The ending should create an emotional payoff or twist.

RETURN ONLY THE STORY.
"""

        # Try a few times because LLMs sometimes ignore
        # exact word-count instructions.
        for attempt in range(3):

            print(
                f"Generating story "
                f"(attempt {attempt + 1}/3)..."
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if not response.text:
                continue

            story = self._clean(
                response.text
            )

            word_count = len(
                story.split()
            )

            print(
                f"Generated {word_count} words."
            )

            # Good length
            if (
                min_words
                <= word_count
                <= max_words
            ):
                return story

            # If too long, ask Gemini to shorten it
            if word_count > max_words:

                prompt = f"""
Rewrite the following story.

IMPORTANT:
Make it between {min_words} and {max_words} words.
Aim for approximately 210 words.

Keep:
- the main plot
- the emotional tension
- the important details
- the twist
- the ending

Remove:
- unnecessary descriptions
- repetitive sentences
- unnecessary dialogue
- filler

Do NOT explain what you changed.

RETURN ONLY THE REWRITTEN STORY.

STORY:
{story}
"""

            # If somehow too short, ask it to expand
            elif word_count < min_words:

                prompt = f"""
Expand the following story to between
{min_words} and {max_words} words.

Keep the same plot, tone, and ending.

Add meaningful details rather than filler.

RETURN ONLY THE REWRITTEN STORY.

STORY:
{story}
"""

        # --------------------------------------------------
        # Final fallback
        # --------------------------------------------------

        raise ValueError(
            "Gemini could not produce a story within "
            f"the required {min_words}-{max_words} word range."
        )

    # --------------------------------------------------
    # Clean Gemini response
    # --------------------------------------------------

    @staticmethod
    def _clean(
        text: str,
    ) -> str:

        text = text.strip()

        # Remove markdown bold
        text = re.sub(
            r"\*\*(.*?)\*\*",
            r"\1",
            text,
        )

        # Remove markdown italics
        text = re.sub(
            r"\*(.*?)\*",
            r"\1",
            text,
        )

        # Remove accidental surrounding quotes
        if (
            text.startswith('"')
            and text.endswith('"')
        ):
            text = text[1:-1]

        # Collapse whitespace
        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()