import os
import sys
import json
import shutil
import subprocess
import wave
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工"
PROJ_DIR = os.path.join(BASE_DIR, "食道裂孔疝氣的原因")
INPUT_CLIPS = os.path.join(PROJ_DIR, "input_clips")
DOWNLOADS = r"C:\Users\X1 Yoga Gen7\Downloads"
FFMPEG = os.path.join(BASE_DIR, "ffmpeg.exe")

os.makedirs(INPUT_CLIPS, exist_ok=True)

# 1. 複製片段
for i in range(1, 5):
    src = os.path.join(DOWNLOADS, f"食道裂孔疝氣的原因{i}.mp4")
    dst = os.path.join(INPUT_CLIPS, f"part{i}.mp4")
    shutil.copy2(src, dst)
    print(f"Copied: part{i}.mp4 ({os.path.getsize(dst)} bytes)")

# 2. 合併片段
concat_file = os.path.join(PROJ_DIR, "concat_list.txt")
with open(concat_file, "w", encoding="utf-8") as f:
    for i in range(1, 5):
        f.write(f"file 'input_clips/part{i}.mp4'\n")

merged_mp4 = os.path.join(PROJ_DIR, "merged_raw.mp4")
subprocess.run([FFMPEG, "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", merged_mp4, "-y"], check=True)
print(f"Merged: {merged_mp4} ({os.path.getsize(merged_mp4)} bytes)")

# 3. 抽取音訊
audio_wav = os.path.join(PROJ_DIR, "audio_raw.wav")
subprocess.run([FFMPEG, "-i", merged_mp4, "-vn", "-c:a", "pcm_s16le", "-ar", "16000", audio_wav, "-y"], check=True)
print(f"Audio: {audio_wav} ({os.path.getsize(audio_wav)} bytes)")

# 4. Whisper 轉錄
from faster_whisper import WhisperModel

model_path = r"C:\Users\X1 Yoga Gen7\.cache\huggingface\hub\models--Systran--faster-whisper-large-v3\snapshots\edaa852ec7e145841d8ffdb056a99866b5f0a478"
print("載入 Faster-Whisper large-v3...")
model = WhisperModel(model_path, device="cpu", compute_type="int8")

initial_prompt = "食道裂孔疝氣的原因，胃食道逆流，橫膈膜裂孔，食道膈肌韌帶，腹腔內壓力長期增加，肥胖，長期咳嗽便秘，膠原蛋白退化，胃部向上推擠。"

print("讀取音訊進行轉錄...")
with wave.open(audio_wav, "rb") as wf:
    n_channels = wf.getnchannels()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if n_channels > 1:
        audio = audio.reshape(-1, n_channels).mean(axis=1)

segments, info = model.transcribe(
    audio,
    language="zh",
    word_timestamps=True,
    initial_prompt=initial_prompt,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=300)
)

results = []
for seg in segments:
    print(f"[{seg.start:.2f} -> {seg.end:.2f}] {seg.text.strip()}", flush=True)
    results.append({
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
        "words": [{"word": w.word, "start": round(w.start, 3), "end": round(w.end, 3)} for w in (seg.words or [])]
    })

with open(os.path.join(PROJ_DIR, "whisper_segments.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n轉錄完成！已存入 whisper_segments.json")
