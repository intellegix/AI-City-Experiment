# Ultra-Realistic 3D City Launcher
# Copyright 2025 Intellegix
# Licensed under the Apache License, Version 2.0

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ULTRA-REALISTIC 3D CITY" -ForegroundColor Cyan
Write-Host "  Photorealistic GTA-Style Simulation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Crafted by Intellegix" -ForegroundColor Yellow
Write-Host "Apache License 2.0" -ForegroundColor Yellow
Write-Host ""
Write-Host "Features:" -ForegroundColor Green
Write-Host "- Detailed buildings with realistic architecture"
Write-Host "- Photorealistic vehicles with proper geometry"
Write-Host "- Animated pedestrians with body parts"
Write-Host "- Environmental props (street lights, trees, etc.)"
Write-Host "- Advanced lighting and shadows"
Write-Host "- Realistic materials (glass, metal, concrete)"
Write-Host "- GTA-style third-person camera"
Write-Host "- Xbox controller support"
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check for command line arguments
$timeOfDay = "afternoon"
if ($args.Length -gt 0) {
    $timeOfDay = $args[0]
}

Write-Host "Launching with time of day: $timeOfDay" -ForegroundColor Green
Write-Host ""

# Launch
python world_ultra_realistic.py --size 64 --time $timeOfDay

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to launch" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Install dependencies: pip install -r requirements.txt"
    Write-Host "2. Check Python version: python --version"
    Write-Host "3. Verify Panda3D: pip show panda3d"
    Write-Host ""
}

Read-Host "Press Enter to exit"
