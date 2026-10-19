import os
import sys
import shutil
import subprocess
import wave
import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_NAME = "十大癌症中屬於消化系癌症的個別分析"
BASE_DIR = os.path.abspath(r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工")
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
INPUT_CLIPS_DIR = os.path.join(PROJECT_DIR, "input_clips")
FFMPEG_BIN = os.path.join(BASE_DIR, "ffmpeg.exe")
LOGO_SRC = os.path.join(BASE_DIR, "turtle_logo.png")

os.makedirs(INPUT_CLIPS_DIR, exist_ok=True)

# Copy the 6 clips from Downloads
downloads_dir = r"c:\Users\X1 Yoga Gen7\Downloads"
for i in range(1, 7):
    src = os.path.join(downloads_dir, f"{PROJECT_NAME}{i}.mp4")
    dst = os.path.join(INPUT_CLIPS_DIR, f"part{i}.mp4")
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

initial_prompt = "十大癌症中屬於消化系癌症的個別分析。大腸癌、肝及肝內膽管癌、胃癌、食道癌、胰臟癌。五癌篩檢、糞便潛血檢查、大腸鏡、幽門螺旋桿菌、B型肝炎、C型肝炎。"

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

raw_lines = []
words_timeline = []

for seg in segments:
    raw_lines.append(f"{seg.start:.2f} -> {seg.end:.2f}: {seg.text.strip()}")
    if seg.words:
        for w in seg.words:
            words_timeline.append(f"{w.start:.2f} -> {w.end:.2f} | {w.word}")

raw_path = os.path.join(PROJECT_DIR, "raw_text.txt")
with open(raw_path, "w", encoding="utf-8") as f:
    f.write("\n".join(raw_lines))

words_path = os.path.join(PROJECT_DIR, "words_timeline.txt")
with open(words_path, "w", encoding="utf-8") as f:
    f.write("\n".join(words_timeline))

print("\n" + "="*50)
print("轉錄完成！音訊內容如下：")
print("="*50)
for line in raw_lines:
    print(line)
