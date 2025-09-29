# Zoya AI Assistant

A multilingual, voice-based & text-based AI assistant similar to Jarvis, built with Python.

## Features

- **Voice Mode**: Zoya listens via mic and responds aloud
- **Text Mode**: Zoya accepts keyboard input and responds via text + voice
- **Female Voice Output**: All responses are spoken in a clear female voice
- **Interrupt System**: Stop speaking immediately with "stop" command or spacebar
- **AI Integration**: Uses OpenRouter API with x-ai/grok-4-fast:free model
- **Multi-language Support**: English, Hindi, Telugu, Tamil, Spanish, French
- **Internet Search**: Live search using DuckDuckGo
- **Text Cleaning**: Removes special characters before speaking

## Project Structure

```
├── main.py                 # Entry point
├── speech_input.py         # Handles STT
├── speech_output.py        # Handles TTS (with stop control)
├── ai_engine.py            # Handles OpenRouter AI
├── duckduckgo_handler.py   # Handles live web search
├── translator.py           # Manages translation
├── utils.py                # Helper functions
├── .env                    # Environment variables (API keys)
├── requirements.txt        # Dependencies
└── README.md               # This file
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Get your OpenRouter API key from [OpenRouter](https://openrouter.ai/)
2. Update the `.env` file with your API key:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

## Usage

Run the assistant:
```bash
python main.py
```

## Dependencies

- openai
- duckduckgo-search
- pyttsx3
- speechrecognition
- pyaudio
- gtts
- translate
- playsound
- keyboard
- python-dotenv

## Supported Languages

- English (en)
- Hindi (hi)
- Telugu (te)
- Tamil (ta)
- Spanish (es)
- French (fr)

## Future Enhancements

- Wake word: "Hey Zoya"
- GUI with CustomTkinter
- Memory system for user preferences
- Plugin system for additional functionality