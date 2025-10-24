#!/data/data/com.termux/files/usr/bin/bash
################################################################################
# AI City Experiment - Installer Script for Termux
# Copyright 2025 Intellegix
################################################################################

echo "========================================"
echo "AI City Experiment - Installer"
echo "Crafted by Intellegix"
echo "========================================"
echo ""

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "❌ Error: This installer must be run in Termux"
    exit 1
fi

echo "📦 Installing AI City Experiment..."
echo ""

# Step 1: Install system dependencies
echo "[1/4] Installing system packages..."
pkg install -y python git || {
    echo "❌ Failed to install system packages"
    exit 1
}
echo "✓ System packages installed"
echo ""

# Step 2: Install Python dependencies
echo "[2/4] Installing Python packages..."
pip install --upgrade pip
pip install numpy scipy networkx noise dataclasses-json pygame || {
    echo "❌ Failed to install Python packages"
    exit 1
}
echo "✓ Python packages installed (including Pygame for Tuxemon UI)"
echo ""

# Step 3: Set up project
echo "[3/4] Setting up project..."
INSTALL_DIR="$HOME/AI_City_Experiment"

if [ -d "$INSTALL_DIR" ]; then
    echo "⚠️  AI City Experiment already exists at $INSTALL_DIR"
    read -p "Do you want to reinstall? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    echo "Backing up existing installation..."
    mv "$INSTALL_DIR" "${INSTALL_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

# Make scripts executable
chmod +x launch_termux.sh launch_android.sh run.sh 2>/dev/null
echo "✓ Project configured"
echo ""

# Step 4: Create home screen widget
echo "[4/4] Creating home screen widget..."
mkdir -p "$HOME/.shortcuts"
cat > "$HOME/.shortcuts/AI-City" << 'SHORTCUT'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/AI_City_Experiment
./launch_termux.sh
SHORTCUT
chmod +x "$HOME/.shortcuts/AI-City"
echo "✓ Widget created"
echo ""

# Installation complete
echo "========================================"
echo "✅ Installation Complete!"
echo "========================================"
echo ""
echo "🚀 Quick Start:"
echo ""
echo "Option 1: Run from terminal"
echo "  cd ~/AI_City_Experiment"
echo "  ./launch_termux.sh"
echo ""
echo "Option 2: Add home screen widget"
echo "  1. Install 'Termux:Widget' from Play Store"
echo "  2. Long-press home screen → Widgets"
echo "  3. Add 'Termux:Widget' shortcut"
echo "  4. Select 'AI-City' from the list"
echo ""
echo "📚 Documentation:"
echo "  - README_ANDROID.md - Android guide"
echo "  - SETUP_COMPLETE.md - Configuration info"
echo "  - RUN_ON_ANDROID.md - Usage instructions"
echo ""
echo "🎮 Customize Settings:"
echo "  Edit config_android.py to adjust:"
echo "  - Grid size (64-512)"
echo "  - Max NPCs (5-50)"
echo "  - Performance settings"
echo ""
echo "Happy simulating! 🏙️"
echo ""
