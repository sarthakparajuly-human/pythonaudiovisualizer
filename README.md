# pythonaudiovisualizer
A Simple Minimal Python Program that plays audios in the terminal
This project is a **terminal-based audio visualizer** that plays an audio file while showing a real-time frequency visualizer alongside an image or video rendered as **ASCII art** — all with theme support and animations.

Disclamer : We Do Not Provide Any Songs Or Music , We Do Not Condone Piracy , Just a simple audio player with cover art 

-<img width="1920" height="1080" alt="Untitled(1)" src="https://github.com/user-attachments/assets/e0ebb5cf-1747-48a7-9639-d02eaf9a1f81" />


## ✅ Requirements

### 🔧 System Requirements:

- **Operating System:** Windows, macOS, or Linux
    
- **Python Version:** Python **3.9 or higher** (recommended 3.10+)

---

## 🚀 Setup Instructions

### Step 1: Install Python (if not already installed)

- Download Python from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
    
- During installation, **make sure to check** ✅ **"Add Python to PATH"**
    

---

### Step 2: Use `first_run.py` to install dependencies

1. **Open PowerShell or Command Prompt** in the project folder:
    
    - Shift + Right Click in the folder → “Open PowerShell window here”
        
2. **Run the following command**:
    
    bash
    
    CopyEdit
    
    `python first_run.py`
    
    This script will automatically install all required packages globally.
    
3. ✅ You should see:
    
    python-repl
    
    CopyEdit
    
    `Installing numpy... Installing librosa... ... ✅ All packages installed globally!`
    
4. You can now **delete `first_run.py`** if you want.
    

---

## 🎬 Running the Visualizer

1. In the same folder, run:
    
    bash
    
    CopyEdit
    
    `python main.py`
    
2. You’ll be prompted to:
    
    - Select a **theme** (e.g., Matrix, Vaporwave, Neon, etc.)
        
    - Select an **audio file** (e.g., `.mp3`, `.wav`)
        
    - Select **cover art** (either an image like `.jpg`, `.png` or a video like `.mp4` for ASCII animation)
        
3. The program will then:
    
    - Play the audio
        
    - Show a frequency bar visualizer on the right
        
    - Render your cover art as animated ASCII on the left
        

---

## 🎨 Available Themes

Choose a theme that affects the color palette of the visualizer:

1. **Vaporwave**
    
2. **Matrix**
    
3. **Neon**
    
4. **Firestorm**
    
5. **Icewave**
    
6. **Toxic**
    
7. **Whiteout**
    

---

## 🔁 Cover Art Support

- **Static Images**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`
    
- **Animated Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`  
    _(used only for visuals, not for audio)_
    

---

## 🧼 Cleanup (Optional)

After installation:

- You may remove `first_run.py` if all packages were installed correctly.
    
- All required functionality lives inside `main.py`.
    


---

## ❗ Troubleshooting

### Python not recognized?

Make sure Python is added to PATH. Try closing and reopening PowerShell/Terminal, or reinstall Python with the “Add to PATH” option enabled.

### Missing dependencies?

You can reinstall manually:

bash

CopyEdit

`pip install numpy librosa scipy sounddevice opencv-python Pillow`

### 📦 Python Dependencies:

The following Python packages are required:

- `numpy`
    
- `librosa`
    
- `scipy`
    
- `sounddevice`
    
- `opencv-python`
    
- `Pillow`
    
- `tkinter` (comes preinstalled with standard Python on Windows/macOS)
    
