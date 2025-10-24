# 📱 How to Build AI City Experiment APK

## Option 1: GitHub Actions (Recommended - Easiest)

### Steps:
1. **Create a GitHub repository** for this project
2. **Upload all files** from `AI_City_Experiment/` folder
3. **Create `.github/workflows/build_apk.yml`** with this content:

```yaml
name: Build APK

on: [push, workflow_dispatch]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install buildozer
        run: |
          sudo apt-get update
          sudo apt-get install -y git zip unzip openjdk-11-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
          pip3 install --upgrade buildozer cython

      - name: Build APK with Buildozer
        run: buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: ai-city-experiment-apk
          path: bin/*.apk
```

4. **Push to GitHub** - the APK will build automatically
5. **Download APK** from Actions tab → Artifacts

---

## Option 2: Use Pydroid 3 (On Your Phone)

### Steps:
1. **Install Pydroid 3** from Google Play Store
2. **Copy project folder** to `/storage/emulated/0/`
3. **Install dependencies** in Pydroid 3:
   ```
   pip install numpy scipy networkx noise dataclasses-json
   ```
4. **Run `main_headless_backup.py`** directly in Pydroid 3
5. **Use Pydroid 3's APK builder** (Premium feature)

---

## Option 3: Build on a Desktop/Laptop

### Requirements:
- Ubuntu/Linux machine OR Windows with WSL2
- 8GB+ RAM
- 20GB+ free space

### Steps:
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-11-jdk autoconf libtool \\
  pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \\
  cmake libffi-dev libssl-dev

# Install Python tools
pip3 install --upgrade buildozer cython

# Navigate to project
cd AI_City_Experiment/

# Build APK
buildozer android debug

# APK will be in bin/ folder
```

---

## 📦 Alternative: Pre-Packaged Version

I've prepared:
- `buildozer.spec` - APK configuration
- Project files ready for building

**Files needed:**
- All `.py` files
- `buildozer.spec`
- Any assets/images (if you add them)

---

## 🚀 Quick Start (No APK Building)

**For immediate use without APK:**

### Method 1: Termux (Current)
```bash
cd ~/AI_City_Experiment
./launch_termux.sh
```

### Method 2: Pydroid 3
1. Install Pydroid 3
2. Copy files to phone storage
3. Open and run `main_headless_backup.py`

---

## 📝 Why Termux Can't Build APKs Easily

- **Memory limitations** on mobile devices
- **Missing Android SDK/NDK** full tools
- **Kivy compilation** requires significant resources
- **Better alternatives** exist (GitHub Actions, desktop builds)

---

## 🎯 Recommended Path

**For maximum compatibility:**
1. ✅ Use Termux for development/testing (what you're doing now)
2. ✅ Use GitHub Actions for APK building (free, automated)
3. ✅ Share built APK with others

---

## 💡 Need Help?

- GitHub Actions builds take 10-20 minutes
- Free for public repositories
- No local resource usage
- Professional CI/CD pipeline

**Next Steps:**
1. Create GitHub account (if you don't have one)
2. Create new repository
3. Upload your AI_City_Experiment folder
4. Add the workflow file
5. Push changes → APK builds automatically!

---

Crafted by Intellegix
