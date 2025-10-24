# AI City Simulation Launcher
# Crafted by Intellegix

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AI CITY SIMULATION LAUNCHER" -ForegroundColor Cyan
Write-Host "Crafted by Intellegix" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "Starting simulation with optimized settings..." -ForegroundColor Green
Write-Host ""

# Launch simulation
python main.py --size 256 --npcs 50

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
