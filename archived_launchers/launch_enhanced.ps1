# Enhanced 3D City Launcher - GTA Style with Procedural Systems
# Copyright 2025 Intellegix
# Licensed under the Apache License, Version 2.0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Enhanced 3D AI City Simulation" -ForegroundColor Cyan
Write-Host "  GTA-Style with Modular Systems" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Features:" -ForegroundColor Yellow
Write-Host "- 50 Procedural Buildings (5 styles)"
Write-Host "- 30 Vehicles (11 types)"
Write-Host "- 10 AI NPCs"
Write-Host "- Xbox Controller Support"
Write-Host "- Third-Person Camera"
Write-Host ""
Write-Host "Launching..." -ForegroundColor Green
Write-Host ""

# Launch enhanced 3D world
python world_3d_enhanced.py --size 64

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to launch enhanced 3D world" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Install dependencies: pip install -r requirements.txt"
    Write-Host "2. Check Python version: python --version"
    Write-Host "3. Verify Panda3D: pip show panda3d"
    Write-Host ""
}

Read-Host "Press Enter to exit"
