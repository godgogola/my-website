import os
import sys
import shutil
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
downloads = os.path.expanduser('~/Downloads')
base_dir = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\影片加工"
proj_name = "高血壓藥物在一般族群及共病族群的選擇"
proj_dir = os.path.join(base_dir, proj_name)
input_clips_dir = os.path.join(proj_dir, "input_clips")
ffmpeg_bin = os.path.join(base_dir, "ffmpeg.exe")

os.makedirs(input_clips_dir, exist_ok=True)

for i in range(1, 7):
    src = os.path.join(downloads, f"{proj_name}{i}.mp4")
    dst = os.path.join(input_clips_dir, f"part{i}.mp4")
    shutil.copy2(src, dst)
    print(f"Copied part{i}.mp4 ({os.path.getsize(dst)} bytes)")

# Create concat list
concat_list = os.path.join(proj_dir, "concat_list.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for i in range(1, 7):
        f.write(f"file 'input_clips/part{i}.mp4'\n")

# Concat
merged_mp4 = os.path.join(proj_dir, "merged_raw.mp4")
cmd_concat = [ffmpeg_bin, "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", merged_mp4, "-y"]
subprocess.run(cmd_concat, check=True)
print(f"Merged: {merged_mp4} ({os.path.getsize(merged_mp4)} bytes)")

# Extract audio
audio_wav = os.path.join(proj_dir, "audio_raw.wav")
cmd_audio = [ffmpeg_bin, "-i", merged_mp4, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", audio_wav, "-y"]
subprocess.run(cmd_audio, check=True)
print(f"Audio extracted: {audio_wav} ({os.path.getsize(audio_wav)} bytes)")
