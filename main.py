import numpy as np
import librosa
from scipy.fft import fft
import os
import sounddevice as sd
import time as pytime
import colorsys
import random
import string
import cv2
from PIL import Image
import threading
import queue
import tkinter as tk
from tkinter import filedialog

# config
TERMINAL_WIDTH = 120
TERMINAL_HEIGHT = 28
COVER_ART_WIDTH = 40
COVER_ART_HEIGHT = TERMINAL_HEIGHT - 3
VISUALIZER_WIDTH = TERMINAL_WIDTH - COVER_ART_WIDTH - 3
FFT_BINS = VISUALIZER_WIDTH - 2
PROGRESS_BAR_WIDTH = TERMINAL_WIDTH - 2
CODE_CHARS = string.ascii_letters + string.digits + "!@#$%^&*(){}[];:<>?/|"
ASCII_CHARS = "@%#*+=-:. "
alpha = 0.5

def rgb_ansi(r, g, b, bg=False):
    return f"\033[48;2;{r};{g};{b}m" if bg else f"\033[38;2;{r};{g};{b}m"

def white_bg_ansi():
    return "\033[48;2;255;255;255m"

def random_code_char():
    return random.choice(CODE_CHARS)

def apply_theme(theme):
    if theme == "vaporwave":
        return lambda i, j: colorsys.hsv_to_rgb(0.85 + (i+j) % 10 * 0.01, 0.7, 1)
    elif theme == "matrix":
        return lambda i, j: colorsys.hsv_to_rgb(0.33, 1, 1)
    elif theme == "neon":
        return lambda i, j: colorsys.hsv_to_rgb((i * 0.03 + pytime.time() * 0.1) % 1.0, 1, 1)
    elif theme == "firestorm":
        return lambda i, j: colorsys.hsv_to_rgb(0.05 + 0.05 * ((i+j)%10), 1, 1)
    elif theme == "icewave":
        return lambda i, j: colorsys.hsv_to_rgb(0.6 + 0.05 * ((i-j)%10), 0.6, 1)
    elif theme == "toxic":
        return lambda i, j: colorsys.hsv_to_rgb(0.2 + 0.02 * ((i*j)%10), 1, 0.9)
    elif theme == "whiteout":
        colors = [(0, 128, 0), (128, 0, 128), (0, 0, 0)]
        return lambda i, j: [x/255 for x in colors[(i+j) % len(colors)]]
    else:
        return lambda i, j: colorsys.hsv_to_rgb((i+j) % 10 * 0.1, 1, 1)

def image_to_ascii(image_path, width, height):
    try:
        img = Image.open(image_path).convert('RGB').resize((width, height))
        pixels = np.array(img)
        ascii_art = []
        for row in pixels:
            ascii_row = ""
            for pixel in row:
                r, g, b = pixel
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                ascii_index = int(gray / 255 * (len(CODE_CHARS) - 1))
                char = CODE_CHARS[ascii_index]
                ascii_row += f"{rgb_ansi(r, g, b)}{char}"
            ascii_art.append(ascii_row)
        return ascii_art
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def video_to_ascii_worker(video_path, frame_queue, stop_event):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_delay = 1.0 / fps if fps > 0 else 1.0/30
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(rgb_frame, (COVER_ART_WIDTH, COVER_ART_HEIGHT))
            ascii_frame = []
            for row in resized:
                ascii_row = ""
                for pixel in row:
                    r, g, b = pixel
                    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                    ascii_index = int(gray / 255 * (len(CODE_CHARS) - 1))
                    char = CODE_CHARS[ascii_index]
                    ascii_row += f"{rgb_ansi(r, g, b)}{char}"
                ascii_frame.append(ascii_row)
            try:
                frame_queue.put(ascii_frame, timeout=0.1)
            except queue.Full:
                pass
            pytime.sleep(frame_delay)
        cap.release()
    except Exception as e:
        print(f"Error processing video: {e}")

class MediaPlayer:
    def __init__(self):
        self.cover_art = None
        self.video_queue = None
        self.video_thread = None
        self.stop_video = None
        self.is_video = False

    def load_cover_art(self, path):
        if not os.path.isfile(path): return False
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            self.cover_art = image_to_ascii(path, COVER_ART_WIDTH, COVER_ART_HEIGHT)
            self.is_video = False
            return True
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
            self.video_queue = queue.Queue(maxsize=5)
            self.stop_video = threading.Event()
            self.video_thread = threading.Thread(target=video_to_ascii_worker, args=(path, self.video_queue, self.stop_video))
            self.video_thread.start()
            self.is_video = True
            return True
        return False

    def get_current_cover_frame(self):
        if self.is_video and self.video_queue:
            try:
                return self.video_queue.get_nowait()
            except queue.Empty:
                return None
        else:
            return self.cover_art

    def cleanup(self):
        if self.stop_video:
            self.stop_video.set()
        if self.video_thread:
            self.video_thread.join()

# ui theme
print("Select a theme:")
print("1. Vaporwave\n2. Matrix\n3. Neon\n4. Firestorm\n5. Icewave\n6. Toxic\n7. Whiteout")
theme_choice = input("Enter number: ").strip()
theme_map = {"1": "vaporwave", "2": "matrix", "3": "neon", "4": "firestorm", "5": "icewave", "6": "toxic", "7": "whiteout"}
theme = theme_map.get(theme_choice, "neon")
get_color = apply_theme(theme)
is_white_theme = theme == "whiteout"

# -dialog functions
def select_audio_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac *.wma")])
    root.destroy()
    return file_path

def select_media_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Cover Art (Image or Video)",
        filetypes=[("Media Files", "*.jpg *.jpeg *.png *.bmp *.gif *.mp4 *.avi *.mov *.mkv *.wmv")])
    root.destroy()
    return file_path

#file 
print("\U0001F3B5 Audio Visualizer Media Player \U0001F3B5")
print("=" * 40)
file_path = select_audio_file()
if not file_path or not os.path.isfile(file_path):
    print("No file selected. Exiting.")
    exit()
print(f"Selected: {os.path.basename(file_path)}")

player = MediaPlayer()
print("\nSelect cover art (image or video)...")
cover_path = select_media_file()
has_cover = False
if cover_path and os.path.isfile(cover_path):
    has_cover = player.load_cover_art(cover_path)

print(f"Loading {os.path.basename(file_path)}...")
y, sr = librosa.load(file_path, mono=True)

duration = librosa.get_duration(y=y, sr=sr)
FFT_WINDOW = 4096
sample_size = FFT_WINDOW

def log_bins(n_bins, fft_size, sr):
    freqs = np.fft.rfftfreq(fft_size, 1/sr)
    log_freqs = np.logspace(np.log10(freqs[1]), np.log10(freqs[-1]), n_bins+1)
    return np.searchsorted(freqs, log_freqs)

log_bin_indices = log_bins(FFT_BINS, sample_size, sr)
smoothing = np.zeros(FFT_BINS)

sd.play(y, sr)
print("\033[?25l", end="")
start_time = pytime.time()

try:
    while True:
        frame_start = pytime.time()
        elapsed = pytime.time() - start_time
        progress = min(elapsed / duration, 1.0)
        current_sample = int(progress * len(y))
        if progress >= 1.0:
            break

        chunk = y[current_sample:current_sample + sample_size]
        if len(chunk) < sample_size:
            chunk = np.pad(chunk, (0, sample_size - len(chunk)), mode='constant')
        fft_data = np.abs(fft(chunk)[:sample_size // 2 + 1])

        spectrum = np.zeros(FFT_BINS)
        for i in range(FFT_BINS):
            start = log_bin_indices[i]
            end = log_bin_indices[i+1]
            spectrum[i] = np.mean(fft_data[start:end]) if end > start else fft_data[start]

        smoothing = alpha * spectrum + (1 - alpha) * smoothing
        norm = np.max(smoothing) + 1e-6
        spectrum_norm = (smoothing / norm) * COVER_ART_HEIGHT
        spectrum_norm = spectrum_norm.astype(int)

        current_cover = player.get_current_cover_frame() if has_cover else None
        print("\033[H\033[J", end="")
        if is_white_theme: print(white_bg_ansi(), end="")

        for row in range(TERMINAL_HEIGHT - 1):
            line = ""
            if has_cover and current_cover and row < len(current_cover):
                line += f"│{current_cover[row]}\033[0m"
                if is_white_theme: line += white_bg_ansi()
            else:
                line += f"│{' ' * COVER_ART_WIDTH}"
            line += "│"
            if row < COVER_ART_HEIGHT:
                spectrum_line = ""
                for col in range(FFT_BINS):
                    if spectrum_norm[col] >= (COVER_ART_HEIGHT - 1 - row):
                        r, g, b = [int(x * 255) for x in get_color(col, row)]
                        char = random_code_char()
                        spectrum_line += f"{white_bg_ansi() if is_white_theme else ''}{rgb_ansi(r, g, b)}{char}"
                    else:
                        spectrum_line += f"{white_bg_ansi() if is_white_theme else ''} "
                line += f"{spectrum_line}\033[0m{white_bg_ansi() if is_white_theme else ''}│"
            else:
                empty_space = f"{white_bg_ansi() if is_white_theme else ''}{' ' * FFT_BINS}"
                line += f"{empty_space}│"
            print(line)

        bar_len = int(progress * PROGRESS_BAR_WIDTH)
        bar = f"{white_bg_ansi() if is_white_theme else ''}{rgb_ansi(80,255,80)}{'█' * bar_len}{rgb_ansi(128,128,128)}{'-' * (PROGRESS_BAR_WIDTH - bar_len)}"
        time_str = f"{int(progress*duration)//60:02}:{int(progress*duration)%60:02}/{int(duration)//60:02}:{int(duration)%60:02}"
        print(f"{white_bg_ansi() if is_white_theme else ''}└{bar} {rgb_ansi(0,0,0) if is_white_theme else ''}{time_str}\033[0m")

        pytime.sleep(max(0, (1/60) - (pytime.time() - frame_start)))

    print("\033[0mDone.")
    sd.wait()

finally:
    print("\033[?25h", end="")
    player.cleanup()
