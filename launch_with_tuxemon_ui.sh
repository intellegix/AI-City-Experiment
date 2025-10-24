#!/data/data/com.termux/files/usr/bin/bash
################################################################################
# AI City Experiment - Tuxemon UI Launcher
# Launches the AI City with full Tuxemon graphical interface
# Copyright 2025 Intellegix
################################################################################

echo "========================================"
echo "AI City Experiment"
echo "Tuxemon UI Edition"
echo "Crafted by Intellegix"
echo "========================================"
echo ""
echo "🎮 Launching with full graphical interface..."
echo ""
echo "Controls:"
echo "  Arrow Keys - Move around the city"
echo "  SPACE/ENTER - Interact with NPCs"
echo "  ESC - Menu"
echo ""
echo "AI Citizens will spawn automatically when the map loads!"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Launch Tuxemon with AI Civilization
python3 launch_tuxemon_civilization.py --citizens 20

echo ""
echo "✨ Thank you for exploring AI City!"
