# 🔊 SpeakUp - Audio Device Volume Control

A powerful Python tool to control speaker volume and manage audio devices on Windows with style! 🎵

## ✨ Features

- 🎯 **Precise Volume Control** - Set exact volume levels (0-100%)
- 🎧 **Multi-Device Support** - Control any audio output device
- 🔥 **CRAZE Mode** - Set any volume that works for you!
- 🎨 **Beautiful Interface** - Colorful terminal output with emojis
- ⚡ **Multiple Usage Modes** - Command line, interactive, or CRAZE mode
- 🪟 **Windows Native** - Uses PowerShell and Windows Audio APIs

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.6+
- PowerShell
- `colorama` package

### Installation

1. Clone this repository:
```bash
git clone https://github.com/github4lives/speakup.git
cd speakup
```

2. Install dependencies:
```bash
pip install colorama
```

3. Run SpeakUp:
```bash
python speakup.py
```

## 📖 How to Use

### 🎮 Interactive Mode (Default)

Simply run the script without arguments to enter interactive mode:

```bash
python speakup.py
```

You'll see a beautiful menu with these options:
1. **Set volume for default device** - Quick volume control for your main speakers
2. **Choose device and set volume** - Select specific audio device and set volume
3. **🔥 CRAZE mode** - Set any volume that works for you!
4. **Refresh device list** - Update the list of available audio devices
5. **Exit** - Close the application

### ⚡ Command Line Mode

#### Basic Volume Control
```bash
# Set default device to 50%
python speakup.py -v 50

# Set default device to 75%
python speakup.py --volume 75
```

#### Device-Specific Control
```bash
# List all available audio devices
python speakup.py -l
python speakup.py --list

# Set device 1 to 60%
python speakup.py -d 1 -v 60
python speakup.py --device 1 --volume 60
```

#### 🔥 CRAZE Mode
```bash
# Launch CRAZE mode from command line
python speakup.py -c
python speakup.py --craze
```

### 🎯 Usage Examples

```bash
# Quick volume adjustments
python speakup.py -v 30    # Morning volume
python speakup.py -v 80    # Gaming volume
python speakup.py -v 15    # Late night volume

# Device management
python speakup.py -l       # See what devices you have
python speakup.py -d 2 -v 90  # Blast your headphones

# Interactive exploration
python speakup.py          # Explore all options
python speakup.py -i       # Force interactive mode

# Go crazy! 🔥
python speakup.py -c       # CRAZE mode for maximum flexibility
```

## 🔥 What is CRAZE Mode?

CRAZE mode is a special feature that gives you complete freedom to set any volume level that works for your situation! Instead of being limited by normal volume ranges, CRAZE mode lets you:

- Set any volume from 0-100% without restrictions
- Apply volumes to any device you choose
- Get visual feedback with fire emojis 🔥
- Perfect for finding that "just right" volume level

**When to use CRAZE mode:**
- 🎵 Fine-tuning audio for music production
- 🎮 Getting the perfect game audio balance
- 🎬 Adjusting movie volumes to your preference
- 🎧 Setting up multiple audio devices
- 🔊 Any time you need precise control!

## 🎨 Command Reference

| Command | Short | Description |
|---------|-------|-------------|
| `--volume LEVEL` | `-v LEVEL` | Set volume (0-100) |
| `--device INDEX` | `-d INDEX` | Choose device by number |
| `--list` | `-l` | List all audio devices |
| `--interactive` | `-i` | Launch interactive mode |
| `--craze` | `-c` | 🔥 CRAZE mode - set any volume! |
| `--help` | `-h` | Show help message |

## 🛠️ Troubleshooting

### Common Issues

**"Could not retrieve audio devices"**
- Make sure you're running on Windows
- Try running PowerShell as administrator
- Check if your audio drivers are working

**"Invalid device selection"**
- Run `python speakup.py -l` to see available devices
- Device numbers start from 1, not 0
- Some devices might not support volume control

**"Volume not changing"**
- Try using CRAZE mode for more flexibility
- Check if the device is set as default
- Some applications might override system volume

### Getting Help

```bash
# See all available options
python speakup.py --help

# List your audio devices
python speakup.py --list

# Use interactive mode to explore
python speakup.py
```

## 🤝 Contributing

Feel free to open issues, submit pull requests, or suggest new features!

## 📄 License

This project is open source. Feel free to use, modify, and distribute!

---

**Made with ❤️ for better audio control on Windows**

*Go ahead, crank it up! 🔊*
