#!/data/data/com.termux/files/usr/bin/bash
# AI City Experiment - Universal Launcher for Android
# Just run: ./run.sh

clear
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           AI CITY EXPERIMENT - ANDROID EDITION            ║"
echo "║                  Crafted by Intellegix                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "main_headless.py" ]; then
    echo "❌ Error: Please run this from the AI_City_Experiment directory"
    echo ""
    echo "Try: cd ~/AI_City_Experiment && ./run.sh"
    exit 1
fi

# Backup original config if exists
if [ -f "config.py" ] && [ ! -f "config_original.py" ]; then
    cp config.py config_original.py
fi

# Use Android config
if [ -f "config_android.py" ]; then
    cp config_android.py config.py
fi

echo "🎮 AI CITY SIMULATION LAUNCHER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Select simulation mode:"
echo ""
echo "  1) 🚀 Quick Start (10 NPCs, 60s)"
echo "  2) ⚡ Fast Mode (5 NPCs, 30s)"
echo "  3) 🎯 Balanced (15 NPCs, 90s)"
echo "  4) 💪 Maximum (25 NPCs, 120s)"
echo "  5) 🛠️  Custom Settings"
echo "  6) 📖 View Documentation"
echo "  7) ❌ Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Quick Mode..."
        python main_headless.py --npc-count 10 --grid-size 128 --duration 60 --seed 42
        ;;
    2)
        echo ""
        echo "⚡ Starting Fast Mode..."
        python main_headless.py --npc-count 5 --grid-size 64 --duration 30 --seed 42
        ;;
    3)
        echo ""
        echo "🎯 Starting Balanced Mode..."
        python main_headless.py --npc-count 15 --grid-size 192 --duration 90 --seed 42
        ;;
    4)
        echo ""
        echo "💪 Starting Maximum Mode..."
        python main_headless.py --npc-count 25 --grid-size 256 --duration 120 --seed 42
        ;;
    5)
        echo ""
        echo "🛠️  Custom Settings"
        echo ""
        read -p "Number of NPCs (1-50): " npcs
        read -p "Grid size (64-512): " grid
        read -p "Duration in seconds (10-300): " duration
        echo ""
        echo "Starting custom simulation..."
        python main_headless.py --npc-count $npcs --grid-size $grid --duration $duration --seed 42
        ;;
    6)
        echo ""
        echo "📖 Documentation Files:"
        echo ""
        echo "  • RUN_ON_ANDROID.md - This guide"
        echo "  • README_ANDROID.md - Full Android documentation"
        echo "  • SETUP_COMPLETE.md - Setup summary"
        echo "  • AI_MODELS_ON_ANDROID.md - AI/LLM guide"
        echo ""
        read -p "View RUN_ON_ANDROID.md? (y/n): " view
        if [ "$view" = "y" ]; then
            less RUN_ON_ANDROID.md
        fi
        ;;
    7)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Running default..."
        python main_headless.py --npc-count 10 --grid-size 128 --duration 60 --seed 42
        ;;
esac

# Restore original config
if [ -f "config_original.py" ]; then
    mv config_original.py config.py
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              SIMULATION COMPLETE! THANK YOU!              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Run again with: ./run.sh"
echo ""
