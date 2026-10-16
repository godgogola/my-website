import os
import sys
import shutil
import json
import wave
import subprocess
import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "糖尿病腎病變 uACR 處置"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
INPUT_CLIPS_DIR = os.path.join(PROJECT_DIR, "input_clips")
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe") if os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")) else "ffmpeg"
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

os.makedirs(INPUT_CLIPS_DIR, exist_ok=True)

# Copy the 6 clips
source_clips = [
    (os.path.join(BASE_DIR, "input_clips", f"{PROJECT_NAME}{i}.mp4"), f"part{i}.mp4")
    for i in range(1, 7)
]

for src, dst_name in source_clips:
    dst = os.path.join(INPUT_CLIPS_DIR, dst_name)
    if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
        print(f"複製 {src} -> {dst}")
        shutil.copy2(src, dst)

local_logo = os.path.join(PROJECT_DIR, "turtle_logo.png")
if not os.path.exists(local_logo) and os.path.exists(LOGO_SRC):
    shutil.copy2(LOGO_SRC, local_logo)

# Concat clips
concat_list = os.path.join(PROJECT_DIR, "concat_list.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for i in range(1, 7):
        f.write(f"file 'input_clips/part{i}.mp4'\n")

merged_mp4 = os.path.join(PROJECT_DIR, "merged_raw.mp4")
cmd_concat = [
    FFMPEG_BIN, "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    merged_mp4, "-y"
]
print("無損合併 6 段影片中...")
subprocess.run(cmd_concat, check=True, cwd=PROJECT_DIR)

# Extract audio
audio_wav = os.path.join(PROJECT_DIR, "audio_raw.wav")
cmd_audio = [
    FFMPEG_BIN, "-i", merged_mp4,
    "-vn", "-c:a", "pcm_s16le", "-ar", "16000", "-ac", "1",
    audio_wav, "-y"
]
print("抽取音訊 WAV 16kHz mono...")
subprocess.run(cmd_audio, check=True)

# Transcribe with Whisper
model_path = r"C:\Users\X1 Yoga Gen7\.cache\huggingface\hub\models--Systran--faster-whisper-large-v3\snapshots\edaa852ec7e145841d8ffdb056a99866b5f0a478"
print("載入 Faster-Whisper 模型...")
model = WhisperModel(model_path, device="cpu", compute_type="int8")

initial_prompt = "糖尿病腎病變、uACR、尿液白蛋白與肌酸酐比值、eGFR、腎絲球過濾率、微量白蛋白尿、ACEi、ARB、SGLT2抑制劑、nsMRA、Finerenone、GLP-1受體激動劑、腎臟保護、心腎共病。"

print("讀取音訊數據為 NumPy 陣列...")
with wave.open(audio_wav, "rb") as wf:
    n_channels = wf.getnchannels()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if n_channels > 1:
        audio = audio.reshape(-1, n_channels).mean(axis=1)

print("開始轉錄與時間軸標記...")
segments, info = model.transcribe(
    audio,
    language="zh",
    word_timestamps=True,
    initial_prompt=initial_prompt,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=300)
)

results = []
raw_lines = []

for seg in segments:
    words_data = []
    if seg.words:
        for w in seg.words:
            words_data.append({
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "word": w.word
            })
    seg_data = {
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
        "words": words_data
    }
    results.append(seg_data)
    raw_lines.append(f"[{seg.start:.2f} -> {seg.end:.2f}] {seg.text.strip()}")
    print(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text.strip()}")

with open(os.path.join(PROJECT_DIR, "whisper_segments.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

with open(os.path.join(PROJECT_DIR, "whisper_raw.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(raw_lines))

print("語音轉錄完成！")
