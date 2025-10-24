#!/data/data/com.termux/files/usr/bin/bash
################################################################################
# AI City Experiment - GitHub APK Build Setup
# Quick setup script for GitHub Actions APK building
# Copyright 2025 Intellegix
################################################################################

echo "========================================"
echo "GitHub APK Build - Quick Setup"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "📦 Installing git..."
    pkg install -y git
fi

# Check if gh (GitHub CLI) is available
echo "Would you like to use GitHub CLI for easier setup? (recommended)"
read -p "Install GitHub CLI? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing GitHub CLI..."
    pkg install -y gh
    HAS_GH=true
else
    HAS_GH=false
fi

echo ""
echo "========================================"
echo "Git Configuration"
echo "========================================"
echo ""

# Configure git
read -p "Enter your name: " GIT_NAME
read -p "Enter your email: " GIT_EMAIL

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo "✓ Git configured"
echo ""

# Initialize repository
echo "========================================"
echo "Repository Setup"
echo "========================================"
echo ""

cd ~/AI_City_Experiment

if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Create .gitignore
echo "Creating .gitignore..."
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.buildozer/
bin/
.DS_Store
*.log
.cache/
android-sdk/
*.tar.gz
EOF
echo "✓ .gitignore created"

# Add files
echo ""
echo "Adding files to git..."
git add .
git status
echo ""

read -p "Create initial commit? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Initial commit: AI City Experiment with Tuxemon UI and GitHub Actions APK build"
    echo "✓ Initial commit created"
fi

echo ""
echo "========================================"
echo "GitHub Repository Setup"
echo "========================================"
echo ""

if [ "$HAS_GH" = true ]; then
    echo "Using GitHub CLI for repository creation..."
    echo ""
    echo "First, let's authenticate with GitHub:"
    gh auth login

    echo ""
    read -p "Create public or private repository? (public/private): " REPO_TYPE

    if [ "$REPO_TYPE" = "private" ]; then
        REPO_FLAG="--private"
    else
        REPO_FLAG="--public"
    fi

    echo ""
    echo "Creating GitHub repository..."
    gh repo create AI-City-Experiment $REPO_FLAG --source=. --remote=origin --push

    if [ $? -eq 0 ]; then
        echo "✓ Repository created and code pushed!"
        REPO_URL=$(gh repo view --json url -q .url)
        echo ""
        echo "Your repository: $REPO_URL"
    else
        echo "❌ Failed to create repository"
        echo "You can create it manually on GitHub.com"
    fi
else
    echo "Manual GitHub setup required:"
    echo ""
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: AI-City-Experiment"
    echo "3. Make it Public (free) or Private (Pro)"
    echo "4. Don't initialize with README"
    echo "5. Click 'Create repository'"
    echo ""
    read -p "Press ENTER when repository is created..."
    echo ""

    read -p "Enter your GitHub username: " GH_USERNAME

    REPO_URL="https://github.com/$GH_USERNAME/AI-City-Experiment.git"
    echo ""
    echo "Adding remote repository..."
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

    echo ""
    echo "Pushing to GitHub..."
    echo "You may be prompted for your GitHub username and password/token"
    git branch -M main
    git push -u origin main

    if [ $? -eq 0 ]; then
        echo "✓ Code pushed to GitHub!"
    else
        echo "❌ Push failed. You may need to set up a Personal Access Token"
        echo "See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"
    fi
fi

echo ""
echo "========================================"
echo "🎉 Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Go to: https://github.com/$GH_USERNAME/AI-City-Experiment"
echo "2. Click 'Actions' tab"
echo "3. Enable workflows if prompted"
echo "4. Click 'Build AI City APK' → 'Run workflow'"
echo "5. Wait 10-20 minutes for APK to build"
echo "6. Download from 'Artifacts' section"
echo ""
echo "📚 Full guide: GITHUB_APK_BUILD_GUIDE.md"
echo ""
echo "✨ Your APK will build automatically in the cloud!"
echo ""
