import os
import pvporcupine
import pyaudio
import struct

# Your API key for Picovoice

# RASP ACCESS_KEY = '+cs716sY8uf8TNQLnIRV4oh58560fYNC1pOFgcf8rbP0FpVYGg4lEw==' 'Ai-Nex_en_raspberry-pi_v3_0_0.ppn'
# Windows
ACCESSW_KEY = 'I1IKvHNkLoisoo2Pb2CLMMkG7JEV5T9CZxS2uYvG1wVj7LqmoetQwA=='

# Paths to your .ppn files (keyword files)
KEYWORD_PATHS = [
    'Ai-Nex_en_windows_v3_0_0.ppn'
]


try:
    # Create Porcupine instance
    porcupine = pvporcupine.create(
        access_key=ACCESSW_KEY,
        keyword_paths=KEYWORD_PATHS
    )

    # Audio stream setup
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        format=pyaudio.paInt16,
        channels=1,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🎧 Listening to microphone...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print(f"\n✅ Keyword detected: Ai Nex")
            # Call the required action here
            # For example: start_assistant(), send_notification(), etc.

except KeyboardInterrupt:
    print("\n Stopped by user.")

finally:
    # Resource cleanup
    if 'porcupine' in locals():
        porcupine.delete()
    if 'audio_stream' in locals():
        audio_stream.close()
    if 'pa' in locals():
        pa.terminate()