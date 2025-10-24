#!/data/data/com.termux/files/usr/bin/bash
# AI City Simulation - Android/Termux Launcher
# Optimized for mobile devices

echo "======================================"
echo "AI City Simulation - Android Edition"
echo "Crafted by Intellegix"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the AI_City_Experiment directory."
    exit 1
fi

# Create a backup of the original config and use Android config
if [ -f "config.py" ] && [ ! -f "config_original.py" ]; then
    echo "Backing up original config..."
    cp config.py config_original.py
fi

echo "Using Android-optimized configuration..."
cp config_android.py config.py

# Set environment variables for better performance
export SDL_VIDEODRIVER=x11
export DISPLAY=:0

echo ""
echo "Starting AI City Simulation..."
echo "Touch controls:"
echo "  - Tap and drag to move camera"
echo "  - Pinch to zoom"
echo "  - Press CTRL+C to exit"
echo ""

# Run with Android-optimized settings
python main.py --npc-count 5 --grid-size 256 --seed 42

# Restore original config when done
if [ -f "config_original.py" ]; then
    echo ""
    echo "Restoring original config..."
    mv config_original.py config.py
fi

echo ""
echo "Simulation ended. Thank you for using AI City!"
