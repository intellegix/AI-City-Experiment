# AI City Simulation - 3D GTA Style Launcher
# Crafted by Intellegix

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AI CITY SIMULATION - 3D GTA STYLE" -ForegroundColor Cyan
Write-Host "Crafted by Intellegix" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "Installing 3D dependencies (if needed)..." -ForegroundColor Yellow
pip install -q panda3d panda3d-gltf Pillow 2>$null
Write-Host ""

Write-Host "Starting 3D simulation with GTA-style graphics..." -ForegroundColor Green
Write-Host ""
Write-Host "CONTROLS:" -ForegroundColor Yellow
Write-Host "  WASD        - Move player" -ForegroundColor White
Write-Host "  Q/E         - Rotate camera" -ForegroundColor White
Write-Host "  Mouse Wheel - Zoom" -ForegroundColor White
Write-Host "  ESC         - Exit" -ForegroundColor White
Write-Host ""

# Launch 3D simulation
python world_3d.py --size 64

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
