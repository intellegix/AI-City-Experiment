# 🚀 Build AI City APK using GitHub Actions

## Complete Step-by-Step Guide

This guide shows you how to build a **professional Android APK** using GitHub Actions - **no phone resources needed!**

---

## 📋 Prerequisites

1. **GitHub Account** (free) - [Sign up here](https://github.com/signup)
2. **Your AI City project files** (already on your device)
3. **10-20 minutes** of your time

---

## 🎯 Step 1: Create GitHub Repository

### Option A: Using GitHub Website

1. **Go to GitHub.com** and log in
2. **Click the "+" icon** (top right) → "New repository"
3. **Fill in details:**
   - Repository name: `AI-City-Experiment`
   - Description: `AI-powered city simulation for Android`
   - Make it **Public** (free) or **Private** (if you have Pro)
   - **Don't** initialize with README (we have our own files)
4. **Click "Create repository"**

### Option B: Using Termux (GitHub CLI)

```bash
# Install GitHub CLI
pkg install gh

# Login to GitHub
gh auth login

# Create repository
cd ~/AI_City_Experiment
gh repo create AI-City-Experiment --public --source=. --remote=origin
```

---

## 🎯 Step 2: Initialize Git in Your Project

```bash
# Navigate to project
cd ~/AI_City_Experiment

# Initialize git (if not already done)
git init

# Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.buildozer/
bin/
.DS_Store
*.log
.cache/
EOF

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AI City Experiment with Tuxemon UI"
```

---

## 🎯 Step 3: Push to GitHub

### If you created repo on website:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AI-City-Experiment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### If you used GitHub CLI:

```bash
# Already connected! Just push
git push origin main
```

---

## 🎯 Step 4: Enable GitHub Actions

1. **Go to your repository** on GitHub.com
2. **Click "Actions" tab** (top of page)
3. You'll see the workflow file is already there!
4. **Click "I understand my workflows, go ahead and enable them"**

---

## 🎯 Step 5: Trigger the Build

### Automatic Build:
Every time you push code, APK builds automatically!

### Manual Build:
1. **Go to Actions tab**
2. **Click "Build AI City APK"** (left sidebar)
3. **Click "Run workflow"** (right side)
4. **Click green "Run workflow" button**
5. **Watch the magic happen!** 🎉

---

## 🎯 Step 6: Download Your APK

After 10-20 minutes (build time):

1. **Go to Actions tab**
2. **Click the completed workflow** (green checkmark ✓)
3. **Scroll down to "Artifacts"**
4. **Click "ai-city-experiment-apk"** to download
5. **Extract the ZIP** - your APK is inside!

---

## 📱 Step 7: Install APK on Your Device

### Method 1: Direct Download

1. **On your Android device**, go to your GitHub repo
2. **Navigate to Actions** → Latest successful build
3. **Download the artifact** directly to your phone
4. **Extract and install**

### Method 2: USB Transfer

1. **Download APK** to your computer
2. **Connect phone via USB**
3. **Copy APK** to phone
4. **Enable "Install from Unknown Sources"** in Settings
5. **Tap APK** to install

### Method 3: Cloud Storage

1. **Upload APK** to Google Drive/Dropbox
2. **Download on phone**
3. **Install**

---

## ⚙️ Configuration Options

### Customize Your Build

Edit `.github/workflows/build_apk.yml` to customize:

```yaml
# Change Python version
python-version: '3.11'  # or '3.10', '3.9'

# Change Java version
java-version: '17'  # or '11'

# Add build parameters
buildozer android debug --ndk-version 25b
```

### Customize buildozer.spec

Edit `buildozer.spec` for app settings:
- App name
- Package name
- Version
- Permissions
- Icon/splash screen

---

## 🔄 Updating Your APK

Whenever you make changes:

```bash
cd ~/AI_City_Experiment

# Make your changes to code
# ...

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# GitHub Actions automatically builds new APK!
```

---

## 📊 Build Status

Check build progress:

1. **Actions tab** shows all builds
2. **Green ✓** = Success
3. **Red ✗** = Failed (click to see logs)
4. **Yellow ⚪** = In progress

---

## 🐛 Troubleshooting

### Build Failed

**Check the logs:**
1. Click on the failed build
2. Click on "build" job
3. Expand failed step
4. Read error message

**Common issues:**

**Missing dependencies:**
```yaml
# Add to build_apk.yml under "Install system dependencies"
sudo apt-get install -y package-name
```

**Python version mismatch:**
```yaml
# Change in build_apk.yml
python-version: '3.10'  # Try different version
```

**Buildozer timeout:**
```yaml
# Increase timeout in build_apk.yml
timeout-minutes: 90  # Default is 60
```

### Git Push Rejected

```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Large Files

GitHub has a 100MB file limit. For large files:

```bash
# Install Git LFS
pkg install git-lfs
git lfs install

# Track large files
git lfs track "*.apk"
git lfs track "Tuxemon/mods/**"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

---

## 💡 Advanced: Automatic Releases

Create tagged releases for version control:

```bash
# Tag a version
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0

# GitHub Actions automatically creates a Release with APK!
```

Users can then download from:
```
https://github.com/YOUR_USERNAME/AI-City-Experiment/releases
```

---

## 🎨 Adding App Icon

1. **Create icon** (512x512 PNG)
2. **Save as** `icon.png` in project root
3. **Update buildozer.spec:**
   ```ini
   icon.filename = %(source.dir)s/icon.png
   ```
4. **Commit and push** - rebuilt APK has your icon!

---

## 📦 What Gets Built

The APK includes:
- ✅ All Python code
- ✅ Tuxemon game engine
- ✅ AI civilization mods
- ✅ All assets and data
- ✅ Required libraries (NumPy, Pygame, etc.)
- ✅ Android-optimized configuration

**Total APK size:** ~150-200MB

---

## 🚀 Quick Command Reference

```bash
# Initial setup
cd ~/AI_City_Experiment
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# After making changes
git add .
git commit -m "Description of changes"
git push origin main

# Create new release
git tag -a v1.0.1 -m "Version 1.0.1"
git push origin v1.0.1

# Check status
git status
git log --oneline
```

---

## 🎯 Pro Tips

1. **Use descriptive commit messages** - helps track changes
2. **Tag versions** - easy to download specific versions
3. **Enable branch protection** - prevents accidental overwrites
4. **Watch build logs** - learn how the build process works
5. **Cache dependencies** - speeds up subsequent builds (already configured!)

---

## 📚 Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python-for-Android](https://python-for-android.readthedocs.io/)

---

## ✅ Summary

1. **Create GitHub repository**
2. **Push your code**
3. **Enable GitHub Actions**
4. **Wait 10-20 minutes**
5. **Download APK from Artifacts**
6. **Install on your device**
7. **Enjoy!**

---

## 🎉 Benefits of This Approach

✅ **No phone resources used** - builds in the cloud
✅ **Free for public repos** - GitHub Actions is free
✅ **Professional builds** - same tools used by big apps
✅ **Automatic updates** - push code, get new APK
✅ **Version control** - track all changes
✅ **Shareable** - anyone can download your APK
✅ **Fast** - parallel builds, caching enabled

---

**Your AI City APK will be built professionally in the cloud!** 🏙️📱✨

**Questions? Check the troubleshooting section or GitHub Actions logs!**

---

Crafted by Intellegix
