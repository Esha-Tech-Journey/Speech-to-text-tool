#!/usr/bin/env python3
"""
Create a sample audio file for testing the speech-to-text tool.
This creates a simple WAV file that can be used for demonstration.
"""

import wave
import struct
import math
import tempfile
import os

def create_sample_wav(filename="sample_audio.wav", duration=3, frequency=440):
    """
    Create a sample WAV file with a simple tone.
    
    Args:
        filename (str): Output filename
        duration (int): Duration in seconds
        frequency (int): Tone frequency in Hz
    """
    sample_rate = 44100
    
    # Generate a simple sine wave
    num_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(num_samples):
        # Create a sine wave that fades in and out
        t = float(i) / sample_rate
        amplitude = 0.3 * math.sin(2 * math.pi * frequency * t)
        
        # Add fade in/out effect
        fade_samples = sample_rate // 4  # 0.25 second fade
        if i < fade_samples:
            amplitude *= i / fade_samples
        elif i > num_samples - fade_samples:
            amplitude *= (num_samples - i) / fade_samples
        
        # Convert to 16-bit integer
        sample = int(amplitude * 32767)
        samples.append(sample)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Pack samples as 16-bit signed integers
        packed_samples = b''.join(struct.pack('<h', sample) for sample in samples)
        wav_file.writeframes(packed_samples)
    
    print(f"Created sample audio file: {filename}")
    print(f"Duration: {duration} seconds")
    print(f"Frequency: {frequency} Hz")
    print("Note: This is a tone, not speech, so speech recognition will likely fail.")
    print("For real testing, use an actual speech recording.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a sample WAV file for testing")
    parser.add_argument("--output", "-o", default="sample_audio.wav", help="Output filename")
    parser.add_argument("--duration", "-d", type=int, default=3, help="Duration in seconds")
    parser.add_argument("--frequency", "-f", type=int, default=440, help="Frequency in Hz")
    
    args = parser.parse_args()
    
    create_sample_wav(args.output, args.duration, args.frequency)