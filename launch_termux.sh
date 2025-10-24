#!/data/data/com.termux/files/usr/bin/bash
# AI City Simulation - Termux Headless Launcher
# Text-mode version that works without graphics

echo "======================================"
echo "AI City Simulation - Termux Edition"
echo "Headless/Text Mode"
echo "Crafted by Intellegix"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "main_headless.py" ]; then
    echo "Error: main_headless.py not found. Please run this script from the AI_City_Experiment directory."
    exit 1
fi

# Create a backup of the original config and use Android config
if [ -f "config.py" ] && [ ! -f "config_original.py" ]; then
    echo "Backing up original config..."
    cp config.py config_original.py
fi

if [ -f "config_android.py" ]; then
    echo "Using Android-optimized configuration..."
    cp config_android.py config.py
fi

echo ""
echo "Starting AI City Simulation (Headless Mode)..."
echo "This version runs in terminal without graphics"
echo ""
echo "Controls:"
echo "  - Simulation runs automatically"
echo "  - Press CTRL+C to exit early"
echo ""
echo "Simulation will run for 60 seconds by default"
echo ""

# Run with Android-optimized settings
python main_headless.py --npc-count 10 --grid-size 256 --seed 42 --duration 60

# Restore original config when done
if [ -f "config_original.py" ]; then
    echo ""
    echo "Restoring original config..."
    mv config_original.py config.py
fi

echo ""
echo "Simulation ended. Thank you for using AI City!"
