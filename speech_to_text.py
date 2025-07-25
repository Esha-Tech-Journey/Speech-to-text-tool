#!/usr/bin/env python3
"""
Simple Speech-to-Text Tool
Converts audio recordings into text using the SpeechRecognition library.
"""

import argparse
import os
import sys
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

# Try to import pyaudio for microphone functionality
try:
    import pyaudio
    MICROPHONE_AVAILABLE = True
except ImportError:
    MICROPHONE_AVAILABLE = False


class SpeechToTextConverter:
    """A simple speech-to-text converter using Google's speech recognition API."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def convert_audio_to_wav(self, audio_file_path):
        """Convert audio file to WAV format if needed."""
        if audio_file_path.lower().endswith('.wav'):
            return audio_file_path
        
        try:
            # Load audio file and convert to WAV
            audio = AudioSegment.from_file(audio_file_path)
            
            # Create temporary WAV file
            temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            audio.export(temp_wav.name, format='wav')
            return temp_wav.name
        except Exception as e:
            raise Exception(f"Error converting audio file: {str(e)}")
    
    def transcribe_audio_file(self, audio_file_path, language='en-US'):
        """
        Transcribe audio file to text.
        
        Args:
            audio_file_path (str): Path to the audio file
            language (str): Language code for recognition (default: 'en-US')
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Convert to WAV if necessary
        wav_file_path = self.convert_audio_to_wav(audio_file_path)
        temp_file_created = wav_file_path != audio_file_path
        
        try:
            # Load audio file
            with sr.AudioFile(wav_file_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record the audio data
                audio_data = self.recognizer.record(source)
            
            # Perform speech recognition
            try:
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text
            except sr.UnknownValueError:
                return "Speech recognition could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results from speech recognition service: {e}"
                
        finally:
            # Clean up temporary file if created
            if temp_file_created and os.path.exists(wav_file_path):
                os.unlink(wav_file_path)
    
    def transcribe_microphone(self, timeout=5, phrase_time_limit=None, language='en-US'):
        """
        Transcribe speech from microphone.
        
        Args:
            timeout (int): Maximum time to wait for speech to start
            phrase_time_limit (int): Maximum time for a phrase
            language (str): Language code for recognition
            
        Returns:
            str: Transcribed text
        """
        if not MICROPHONE_AVAILABLE:
            return "Error: PyAudio is not installed. Install it with: pip install pyaudio"
        
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening... Speak now!")
                
                # Listen for audio with specified timeout
                audio_data = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processing speech...")
                
                # Perform speech recognition
                try:
                    text = self.recognizer.recognize_google(audio_data, language=language)
                    return text
                except sr.UnknownValueError:
                    return "Speech recognition could not understand the audio"
                except sr.RequestError as e:
                    return f"Could not request results from speech recognition service: {e}"
                    
        except sr.WaitTimeoutError:
            return "No speech detected within the timeout period"
        except Exception as e:
            return f"Error accessing microphone: {str(e)}"


def main():
    """Main function to handle command line arguments and run the speech-to-text tool."""
    parser = argparse.ArgumentParser(
        description="Simple Speech-to-Text Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python speech_to_text.py audio.wav
  python speech_to_text.py audio.mp3 --language es-ES
  python speech_to_text.py --microphone
  python speech_to_text.py --microphone --timeout 10
        """
    )
    
    # Add arguments
    parser.add_argument(
        'audio_file', 
        nargs='?', 
        help='Path to audio file to transcribe'
    )
    parser.add_argument(
        '--microphone', '-m',
        action='store_true',
        help='Transcribe from microphone instead of file'
    )
    parser.add_argument(
        '--language', '-l',
        default='en-US',
        help='Language code for speech recognition (default: en-US)'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=5,
        help='Timeout in seconds for microphone input (default: 5)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file to save transcribed text'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.microphone and not args.audio_file:
        parser.error("Either provide an audio file or use --microphone option")
    
    if args.microphone and args.audio_file:
        parser.error("Cannot use both audio file and microphone simultaneously")
    
    if args.microphone and not MICROPHONE_AVAILABLE:
        parser.error("Microphone functionality requires PyAudio. Install it with: pip install pyaudio")
    
    # Initialize converter
    converter = SpeechToTextConverter()
    
    try:
        # Perform transcription
        if args.microphone:
            print(f"Using microphone with {args.timeout}s timeout...")
            text = converter.transcribe_microphone(
                timeout=args.timeout,
                language=args.language
            )
        else:
            print(f"Transcribing audio file: {args.audio_file}")
            text = converter.transcribe_audio_file(
                args.audio_file,
                language=args.language
            )
        
        # Output results
        print("\n" + "="*50)
        print("TRANSCRIPTION RESULT:")
        print("="*50)
        print(text)
        print("="*50)
        
        # Save to file if specified
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nTranscription saved to: {args.output}")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()