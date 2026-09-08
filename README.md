```
```

````
# LoreLoop AI Shorts Generator

An automated YouTube Shorts generator that creates fictional stories using AI, narrates them with text-to-speech, generates synchronized word-by-word subtitles, and combines everything with Minecraft gameplay.

The goal is to turn a simple story prompt into a complete vertical Short with minimal manual work.

## ✨ Features

- 🤖 AI-generated fictional stories
- 📝 Configurable story length
- 🎙️ Text-to-speech narration using Edge TTS
- ⏱️ Word-level subtitle timing
- 💬 Animated subtitles synchronized with narration
- 🎮 Minecraft gameplay as the background
- 🎲 Random background-video selection
- 📱 Vertical 9:16 video output
- 🏷️ LoreLoop watermark
- ⚡ Fully automated generation pipeline

## 🛠️ Tech Stack

- **Python**
- **Google Gemini** — story generation
- **Edge TTS** — narration
- **Pillow** — subtitle and watermark rendering
- **FFmpeg** — video processing and encoding

## 📁 Project Structure

```text
ai-shorts-generator/
│
├── src/
│   ├── __init__.py
│   ├── story.py          # AI story generation
│   ├── tts.py            # Text-to-speech + word timings
│   ├── subtitles.py      # Subtitle rendering
│   └── video.py          # Video composition
│
├── backgrounds/
│   └── test.mp4          # Minecraft gameplay footage
│
├── output/               # Generated Shorts
├── temp/                 # Temporary files
│
├── main.py               # Main pipeline
├── config.py             # Configuration
├── requirements.txt      # Python dependencies
├── .env                  # API keys and settings
└── .gitignore
````

## 🔄 How It Works

```
```

```
Story Prompt
     │
     ▼
┌─────────────────┐
│  Gemini         │
│  Story Writer   │
└────────┬────────┘
         │
         ▼
     Fictional Story
         │
         ▼
┌─────────────────┐
│    Edge TTS     │
│    Narration    │
└────────┬────────┘
         │
         ├──────────────► Word Timings
         │
         ▼
      Audio
         │
         ▼
┌─────────────────────────┐
│      Video Renderer     │
│                         │
│ Minecraft Background    │
│ + Subtitles             │
│ + LoreLoop Watermark    │
└────────────┬────────────┘
             │
             ▼
       Final Short
```

## 🚀 Setup

### 1. Clone the repository

```
```

```
git clone https://github.com/chaitanya-sakamuri/ai-shorts-generator.git
cd ai-shorts-generator
```

### 2. Install Python dependencies

```
```

```
pip install -r requirements.txt
```

### 3. Install FFmpeg

On Ubuntu/Debian:

```
```

```
sudo apt install ffmpeg
```

Verify the installation:

```
```

```
ffmpeg -version
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
```

```
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-3.5-flash-lite

TTS_VOICE=en-US-BrianNeural

VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
FPS=30

STORY_MIN_WORDS=190
STORY_MAX_WORDS=220

BACKGROUND_DIR=backgrounds
OUTPUT_DIR=output
TEMP_DIR=temp
```

Replace `YOUR_KEY_HERE` with your Gemini API key.

**Never commit your** **`.env`** **file or API keys to GitHub.**

### 5. Add background footage

Place Minecraft gameplay videos inside:

```
```

```
backgrounds/
```

For example:

```
```

```
backgrounds/
├── minecraft1.mp4
├── minecraft2.mp4
└── minecraft3.mp4
```

The generator selects a suitable random section of the gameplay for each Short.

## ▶️ Usage

Run:

```
```

```
python main.py
```

The generator will:

1.  Generate a fictional story. 
2.  Convert the story into narration. 
3.  Generate word-level timing information. 
4.  Select a random section of Minecraft gameplay. 
5.  Render synchronized subtitles. 
6.  Add the LoreLoop watermark. 
7.  Export the final vertical video. 

Generated videos are saved to:

```
```

```
output/
```

## 🎬 Output

The generated videos are designed for YouTube Shorts and use a vertical:

```
```

```
1080 × 1920
```

format.

Each video contains:

-  AI-generated fictional narration 
-  Minecraft gameplay 
-  Synchronized subtitles 
-  LoreLoop branding 

## ⚙️ Customization

Most settings can be changed through `.env`.

### Story length

```
```

```
STORY_MIN_WORDS=190
STORY_MAX_WORDS=220
```

### TTS voice

```
```

```
TTS_VOICE=en-US-BrianNeural
```

### Video resolution

```
```

```
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
```

### Frame rate

```
```

```
FPS=30
```

## 🧠 Story Topics

The generator can be used with different fictional story themes, such as:

-  Mystery 
-  Betrayal 
-  Revenge 
-  Friendship 
-  Love 
-  Jealousy 
-  Suspense 
-  Unexpected twists 
-  Dark stories 
-  Funny situations 
-  Emotional stories 

The project is designed to make experimenting with different story concepts easy.

## 📌 Roadmap

- [x] AI story generation
- [x] Text-to-speech narration
- [x] Word-level timing
- [x] Synchronized subtitles
- [x] Minecraft gameplay backgrounds
- [x] Random background selection
- [x] LoreLoop watermark
- [ ] Automatic topic selection
- [ ] Batch generation
- [ ] Automatic YouTube upload
- [ ] Multiple subtitle styles
- [ ] Background-video library management
- [ ] Analytics-based story/topic selection

## ⚠️ Disclaimer

This project generates fictional stories using AI.

Background gameplay should be footage that you have permission to use or that is otherwise appropriately licensed.

so i shall paste this?
