# Python PC nhận audio từ ESP32
# và chuyển speech → text bằng Whisper

# pip install pyserial openai-whisper soundfile numpy scipy

import serial
import wave
import whisper
import time

PORT = "COM5"       # sửa lại COM của bạn
BAUD = 115200
SECONDS = 5
SAMPLE_RATE = 16000

print("Loading Whisper model...")
model = whisper.load_model("base")

ser = serial.Serial(PORT, BAUD)

print("Recording...")

frames = bytearray()

start = time.time()

while time.time() - start < SECONDS:
    if ser.in_waiting:
        frames.extend(
            ser.read(ser.in_waiting)
        )

print("Saving WAV...")

with wave.open("record.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(frames)

print("Transcribing...")

result = model.transcribe("record.wav", language="vi")

print("TEXT:")
print(result["text"])
