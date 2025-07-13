import subprocess
import sys

# List of required packages
packages = [
    'numpy',
    'librosa',
    'scipy',
    'sounddevice',
    'opencv-python',
    'Pillow'
]

# Install each package globally
for package in packages:
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
print("✅ All packages installed globally!")
