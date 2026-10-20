import os
import sys
import json
import wave
import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工"
PROJECT_DIR = os.path.join(BASE_DIR, "112年臺灣癌症登記報告")
audio_wav = os.path.join(PROJECT_DIR, "audio_raw.wav")

model_path = r"C:\Users\X1 Yoga Gen7\.cache\huggingface\hub\models--Systran--faster-whisper-large-v3\snapshots\edaa852ec7e145841d8ffdb056a99866b5f0a478"
print("載入 Faster-Whisper int8 模型...")
model = WhisperModel(model_path, device="cpu", compute_type="int8")

initial_prompt = "112年臺灣癌症登記報告。衛福部最新公布國人癌症登記報告，十大癌症排名。肺癌、大腸癌、乳癌、肝癌、攝護腺癌、口腔癌、甲狀腺癌、皮膚癌、胃癌、子宮體癌。男性大腸癌榜首14年，女性乳癌榜首21年。50歲以上罹癌佔八成四，年齡中位數65歲。"

print("讀取音訊數據為 NumPy 陣列...")
with wave.open(audio_wav, "rb") as wf:
    n_channels = wf.getnchannels()
    n_frames = wf.getnframes()
    frames = wf.readframes(n_frames)
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if n_channels > 1:
        audio = audio.reshape(-1, n_channels).mean(axis=1)

print("開始高速轉錄與時間軸標記...")
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
words_timeline = []

for seg in segments:
    seg_data = {
        "start": round(seg.start, 3),
        "end": round(seg.end, 3),
        "text": seg.text.strip(),
        "words": []
    }
    line = f"{seg.start:.2f} -> {seg.end:.2f}: {seg.text.strip()}"
    raw_lines.append(line)
    print(line, flush=True)
    if seg.words:
        for w in seg.words:
            seg_data["words"].append({
                "word": w.word,
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "probability": round(w.probability, 3)
            })
            words_timeline.append(f"{w.start:.2f} -> {w.end:.2f} | {w.word}")
    results.append(seg_data)

json_path = os.path.join(PROJECT_DIR, "whisper_segments.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

raw_path = os.path.join(PROJECT_DIR, "raw_text.txt")
with open(raw_path, "w", encoding="utf-8") as f:
    f.write("\n".join(raw_lines))

words_path = os.path.join(PROJECT_DIR, "words_timeline.txt")
with open(words_path, "w", encoding="utf-8") as f:
    f.write("\n".join(words_timeline))

print("\n" + "="*50)
print("轉錄完成！已存至 whisper_segments.json")
print("="*50)
