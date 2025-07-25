# Speech-to-Text Tool

A simple Python tool that converts audio recordings into text using the SpeechRecognition library with Google's speech recognition API.

## Features

- Convert audio files to text (supports WAV, MP3, and other common formats)
- Real-time transcription from microphone
- Support for multiple languages
- Command-line interface for easy usage
- Error handling for various audio formats and network issues

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Esha-Tech-Journey/Speech-to-text-tool.git
cd Speech-to-text-tool
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

**Note:** On some systems, you may need to install additional dependencies:
- **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **macOS**: `brew install portaudio`
- **Windows**: PyAudio should install automatically via pip

## Usage

### Transcribe Audio Files

```bash
# Basic usage
python speech_to_text.py audio_file.wav

# Specify language (e.g., Spanish)
python speech_to_text.py audio_file.mp3 --language es-ES

# Save output to file
python speech_to_text.py audio_file.wav --output transcription.txt
```

### Real-time Microphone Transcription

```bash
# Basic microphone transcription
python speech_to_text.py --microphone

# With custom timeout and language
python speech_to_text.py --microphone --timeout 10 --language fr-FR
```

### Command-line Options

- `audio_file`: Path to audio file to transcribe
- `--microphone, -m`: Use microphone for real-time transcription
- `--language, -l`: Language code for recognition (default: en-US)
- `--timeout, -t`: Timeout in seconds for microphone input (default: 5)
- `--output, -o`: Output file to save transcribed text

### Supported Languages

Common language codes include:
- `en-US`: English (US)
- `en-GB`: English (UK)
- `es-ES`: Spanish (Spain)
- `fr-FR`: French (France)
- `de-DE`: German (Germany)
- `it-IT`: Italian (Italy)
- `pt-BR`: Portuguese (Brazil)
- `ja-JP`: Japanese
- `ko-KR`: Korean
- `zh-CN`: Chinese (Simplified)

## Examples

```bash
# Transcribe a WAV file
python speech_to_text.py recording.wav

# Transcribe an MP3 file in Spanish
python speech_to_text.py podcast.mp3 --language es-ES

# Real-time transcription with 15-second timeout
python speech_to_text.py --microphone --timeout 15

# Save transcription to a text file
python speech_to_text.py interview.wav --output transcript.txt
```

## Testing

Run the test script to verify the installation:

```bash
python test_speech_to_text.py
```

## Dependencies

- **SpeechRecognition**: Core speech recognition functionality
- **PyAudio**: For microphone access
- **pydub**: For audio format conversion

## Requirements

- Python 3.6+
- Internet connection (for Google Speech Recognition API)
- Microphone (for real-time transcription)

## Limitations

- Requires internet connection for Google's speech recognition service
- Audio quality affects transcription accuracy
- Long audio files may take some time to process
- Free Google API has usage limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Feel free to use and modify as needed.

## Troubleshooting

### Common Issues

1. **PyAudio installation fails**: Install system dependencies first (see Installation section)
2. **"No module named 'speech_recognition'"**: Run `pip install -r requirements.txt`
3. **Microphone not working**: Check system permissions and microphone access
4. **Network errors**: Ensure internet connection for Google's API

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your audio file format is supported
3. Test with a simple WAV file first
4. Check internet connectivity for online recognition