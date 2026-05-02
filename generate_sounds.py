import wave
import math
import struct
import os

os.makedirs('assets/sounds', exist_ok=True)

def generate_bloop(filename, duration=0.1, start_freq=900, end_freq=400, sample_rate=44100):
    """Tạo âm thanh 'bloop' dạng bọt nước vỡ."""
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2) # 16-bit
        f.setframerate(sample_rate)
        
        frames = []
        num_samples = int(sample_rate * duration)
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Tần số giảm dần tạo cảm giác giọt nước/bong bóng
            freq = start_freq * ((end_freq / start_freq) ** (t / duration))
            # Sóng Sine
            value = 32767.0 * 0.4 * math.sin(2.0 * math.pi * freq * t)
            # Fade out mượt mà (Envelope)
            envelope = 1.0 - (t / duration)
            value = int(value * envelope)
            
            frames.append(struct.pack('<h', value))
            
        f.writeframes(b''.join(frames))

def generate_chime(filename, duration=0.6, base_freq=523.25, sample_rate=44100):
    """Tạo âm thanh Ting Ting (Level Up - C Major Arpeggio)."""
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        
        frames = []
        num_samples = int(sample_rate * duration)
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            # C4 -> E4 -> G4 -> C5
            if t < 0.15: freq = base_freq
            elif t < 0.3: freq = base_freq * 1.25 
            elif t < 0.45: freq = base_freq * 1.5 
            else: freq = base_freq * 2.0 
            
            value = 32767.0 * 0.3 * math.sin(2.0 * math.pi * freq * t)
            # Fade out
            envelope = 1.0 - (t / duration)**2
            value = int(value * envelope)
            
            frames.append(struct.pack('<h', value))
            
        f.writeframes(b''.join(frames))

generate_bloop('assets/sounds/pop.wav')
generate_chime('assets/sounds/levelup.wav')
print("Generated custom sound effects successfully!")
