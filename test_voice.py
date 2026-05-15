import os
import wave
import struct
import math
from app.services.voice_assistant import process_voice_query

def generate_beep_wav(filename="test_beep.wav"):
    # Generate a simple 1 second beep
    sample_rate = 44100.0
    duration = 1.0
    frequency = 440.0 # A4
    
    wave_file = wave.open(filename, 'w')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    
    for i in range(int(duration * sample_rate)):
        value = int(32767.0 * math.sin(frequency * math.pi * 2 * i / sample_rate))
        data = struct.pack('<h', value)
        wave_file.writeframesraw(data)
        
    wave_file.close()
    return filename

if __name__ == "__main__":
    print("Generating audio file...")
    filename = generate_beep_wav()
    print(f"Testing voice assistant with {filename}...")
    try:
        response = process_voice_query(filename)
        print(f"SUCCESS. Response:\n{response}")
    except Exception as e:
        print(f"FAILED. Error:\n{e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)
