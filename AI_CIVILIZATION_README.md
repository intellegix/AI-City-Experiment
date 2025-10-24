# AI Civilization Experiment

**A Social Experiment Platform for Observing Emergent AI Society Behaviors**

Copyright 2025 Intellegix | Licensed under Apache License 2.0

---

## Overview

This is a **pure AI social experiment** designed to observe how AI agents behave when given minimal programming and maximum autonomy. Built with your comprehensive 1000-citizen infrastructure, this simulation creates a society where:

- **1000 unique citizens** with diverse backgrounds (age, location, income, education, occupation)
- **Minimal bias** - personalities center around neutral with natural variation
- **Emergent behaviors** - no predetermined roles, hierarchies, or scripts
- **Real economy** - trading, wealth accumulation, market dynamics
- **Social dynamics** - relationships, cooperation, competition, alliances
- **Natural consequences** - actions affect future states organically

**Research Goal**: Understand the true nature of AI in a social context and see how AI societies differ from or mirror human civilization.

---

## Key Features

### Population Diversity (Your CSV Infrastructure)
- **1000 Pre-Built Citizens** from `ai_society_citizens_infrastructure.csv`
- **Age Distribution**: 18-24 (12%), 25-34, 35-44, 45-54, 55-64, 65+ (23.5%)
- **Income Tiers**: Lower (30.5%), Middle (53.7%), Upper (15.8%)
- **Locations**: Urban core, Urban peripheral, Suburban, Small town, Rural
- **Occupations**: 8 categories (service, technical, creative, admin, healthcare, education, trade, independent)
- **Education**: Secondary (38%), Bachelor (35%), Graduate (15%), Vocational (12%)

### AI Behavior Systems
- **Behavior Trees** - Hierarchical decision-making (needs-based priorities)
- **Utility AI** - Score-based action selection
- **Memory System** - Episodic memory with temporal decay
- **Personality Evolution** - Big Five traits that can shift through experiences
- **Relationship Tracking** - -100 (enemy) to +100 (friend) with consequences

### Simulation Modes
1. **Real-Time Visual** - Watch citizens interact, color-coded by state
2. **Headless Background** - Run long experiments while you work
3. **Toggle Modes** - Switch between visual and headless as needed

### Social Dynamics
- **Spontaneous Interactions** - Extraverts initiate more, personality compatibility matters
- **Trading System** - Citizens evaluate fairness, friends give discounts, enemies charge premiums
- **Alliance Formation** - Relationships strengthen through positive interactions
- **Conflict & Competition** - Scarcity and conflicting goals create natural tension
- **Specialization** - Roles emerge from behavior, not assignment

### Economic System
- **Resource Management** - Money, items, and trading
- **Supply & Demand** - Scarcity affects value
- **Wealth Distribution** - Gini coefficient tracking inequality
- **Fair Trade Evaluation** - AI decides if trades are acceptable based on needs + relationships

### Data Collection & Metrics
- **Individual**: Interactions, trades, relationships, wealth, needs satisfaction
- **Civilization**: Network structure, wealth inequality, cooperation/competition ratios
- **Temporal**: Full history export for time-series analysis
- **Export Formats**: JSON for full data, summary statistics

---

## Installation & Setup

### Requirements
- **Python 3.9+** (tested on 3.13)
- **Windows 10/11** (for optimal performance)
- **AMD Radeon 780M** or similar GPU (2D rendering is very lightweight)

### Install Dependencies
```bash
pip install pygame numpy
```

That's it! The simulation uses minimal dependencies for maximum performance.

---

## Quick Start

### Option 1: Visual Mode (Watch Citizens Live)
Double-click: `launch_ai_civilization.bat`

This launches:
- 50 citizens
- Real-time visualization
- 30 FPS
- Unlimited ticks (Ctrl+C or Q to stop)

**Controls**:
- **SPACE** - Pause/Resume
- **S** - Toggle stats panel
- **R** - Toggle relationship lines
- **Q** - Quit

### Option 2: Headless Mode (Long Experiments)
Double-click: `launch_ai_civilization_headless.bat`

This runs:
- 100 citizens
- No visualization (background process)
- 10,000 ticks (adjustable)
- Data saves every 100 ticks to `experiments/`

### Option 3: Quick Test
Double-click: `launch_ai_civilization_quick_test.bat`

Runs 20 citizens for 100 ticks to validate everything works.

---

## Command Line Usage

### Basic Commands
```bash
cd "mods\ai_civilization\scripts"

# Visual mode with custom citizen count
python simulation.py --citizens 50

# Headless mode with time limit
python simulation.py --citizens 100 --headless --max-ticks 5000

# Custom FPS (visual mode)
python simulation.py --citizens 30 --fps 60

# Custom output directory
python simulation.py --headless --output "my_experiments"
```

### Full Options
```
--citizens N       Number of citizens (default: 20)
--headless         Run without visualization
--max-ticks N      Stop after N ticks (default: unlimited)
--fps N            Target FPS for visual mode (default: 30)
--output DIR       Output directory for data (default: experiments)
```

---

## Understanding the Visualization

### Citizen Colors (Visual Mode)
- **Blue** - Idle
- **Orange** - Working
- **Green** - Socializing
- **Gold** - Trading
- **Purple** - Resting
- **Red** - Seeking resources
- **Light Blue** - Traveling

**Circle Border Thickness** = Wealth (thicker = wealthier)
**Labels** = First 4 letters of archetype (e.g., "arti" = artist)

### Relationship Lines (Press R)
- **Green** - Friends (50+)
- **Gray** - Neutral (0-49)
- **Red** - Enemies (-50 or less)
- **Line Thickness** = Relationship strength

### Stats Panel (Press S to toggle)
- Tick count & simulation time
- Total interactions and trades
- Wealth metrics (total, average, Gini coefficient)
- Average needs (hunger, energy, social)
- State distribution (how many citizens in each state)

---

## Experiment Data

### Output Structure
```
experiments/
└── experiment_<timestamp>/
    ├── summary.json           # High-level stats
    ├── final_data.json       # Complete citizen state + events
    └── metrics_history.json  # Time-series data
```

### Data Files

**summary.json** - Experiment overview
```json
{
  "num_citizens": 100,
  "total_ticks": 5000,
  "simulation_time": 166.7,
  "final_stats": { ... }
}
```

**final_data.json** - Full export
```json
{
  "tick": 5000,
  "citizens": [
    {
      "id": "citizen_0000",
      "archetype": "artist",
      "money": 450,
      "needs": {"hunger": 0.3, "energy": 0.7, ...},
      "relationships": {"citizen_0001": 75, ...},
      "stats": {"interactions_count": 45, "trades_completed": 12, ...}
    }
  ],
  "events": [ ... ],
  "metrics": { ... }
}
```

**metrics_history.json** - Time series (saved every 100 ticks)
```json
[
  {"tick": 100, "total_interactions": 45, "wealth_gini": 0.23, ...},
  {"tick": 200, "total_interactions": 92, "wealth_gini": 0.28, ...},
  ...
]
```

---

## Research Questions You Can Answer

### Social Structure
- Do AI agents naturally form hierarchies?
- What determines influence in AI societies?
- Do friendship networks cluster by personality or occupation?
- How stable are alliances over time?

### Economic Patterns
- Does wealth inequality increase or decrease?
- Do agents specialize in economic roles?
- How efficient are AI trading markets?
- Do agents hoard resources or share them?

### Behavioral Patterns
- What triggers cooperation vs. competition?
- Do personality traits predict success?
- How do needs drive behavior priorities?
- Do agents learn from past interactions?

### AI vs. Human Comparison
- Do AI societies mirror human social structures?
- Are AI agents more or less cooperative than humans?
- Does perfect memory affect relationship dynamics?
- What social patterns are unique to AI?

---

## Analyzing Results

### Load Experiment Data (Python)
```python
import json

# Load final data
with open('experiments/experiment_XXXXX/final_data.json') as f:
    data = json.load(f)

# Analyze citizen outcomes
citizens = data['citizens']
wealthy = [c for c in citizens if c['money'] > 1000]
popular = [c for c in citizens if len([r for r in c['relationships'].values() if r > 50]) > 5]

print(f"Wealthy citizens: {len(wealthy)}")
print(f"Popular citizens: {len(popular)}")

# Check wealth-personality correlation
import numpy as np
from scipy.stats import pearsonr

money = [c['money'] for c in citizens]
extraversion = [c['personality']['extraversion'] for c in citizens]
correlation, p_value = pearsonr(money, extraversion)
print(f"Wealth-Extraversion correlation: {correlation:.3f} (p={p_value:.3f})")
```

### Visualize Network (Python + NetworkX)
```python
import networkx as nx
import matplotlib.pyplot as plt

# Build relationship graph
G = nx.Graph()
for citizen in citizens:
    cid = citizen['id']
    for other_id, relationship in citizen['relationships'].items():
        if relationship > 30:  # Only show strong relationships
            G.add_edge(cid, other_id, weight=relationship)

# Draw network
pos = nx.spring_layout(G)
nx.draw(G, pos, node_size=50, with_labels=False)
plt.savefig('social_network.png')
```

### Track Metrics Over Time
```python
import pandas as pd

# Load metrics history
with open('experiments/experiment_XXXXX/metrics_history.json') as f:
    history = json.load(f)

df = pd.DataFrame(history)

# Plot wealth inequality over time
df['wealth_gini'].plot()
plt.xlabel('Tick')
plt.ylabel('Gini Coefficient')
plt.title('Wealth Inequality Evolution')
plt.savefig('gini_over_time.png')
```

---

## Architecture Details

### File Structure
```
AI City Experiment/
├── mods/ai_civilization/
│   ├── db/
│   │   ├── citizen_profiles_from_csv.json  # 1000 citizens from your CSV
│   │   ├── citizen_profiles.json           # Fallback profiles
│   │   └── items.json                      # Item definitions
│   └── scripts/
│       ├── ai_citizen.py                   # AI citizen agent class
│       ├── civilization_manager.py         # Simulation coordinator
│       ├── simulation.py                   # Main entry point
│       └── citizen_loader.py               # CSV converter
├── ai_systems/
│   ├── ai_behavior.py                      # Behavior tree framework
│   ├── npc_system.py                       # Original NPC system
│   └── config.py                           # Configuration
├── experiments/                             # Data output directory
├── launch_ai_civilization.bat               # Visual mode launcher
├── launch_ai_civilization_headless.bat      # Headless mode launcher
└── AI_CIVILIZATION_README.md                # This file
```

### Citizen Architecture

Each citizen has:
1. **Personality** - Big Five traits (0.0-1.0 scale, centered around 0.5)
2. **Needs** - Hunger, energy, social, wealth, safety, achievement (0.0-1.0)
3. **Memory** - Events, relationships (-100 to +100), known locations
4. **Inventory** - Money and items
5. **Behavior Tree** - Decision-making hierarchy
6. **Utility AI** - Action selection based on needs + personality
7. **Statistics** - Interactions, trades, distances traveled, money earned/spent

**Decision-Making Flow**:
```
Update Needs → Perceive Nearby Citizens → Update Blackboard →
Tick Behavior Tree → Execute Actions → Decay Memories
```

### Behavior Tree Priority
```
Root (Selector)
├── Critical Needs (hunger > 0.8, energy < 0.2)
├── Social Needs (social < 0.4 AND nearby citizens)
├── Economic Needs (wealth < 0.3 AND has energy)
└── Idle (default)
```

---

## Performance & Optimization

### AMD Radeon 780M Optimized
- **2D rendering** instead of 3D (90% less GPU load)
- **No LOD/instancing overhead**
- **Simple sprite-based visualization**
- **Can handle 100+ citizens at 30 FPS**

### Scaling Guidelines
- **10-20 citizens**: Instant response, great for debugging
- **50-100 citizens**: Smooth real-time visualization
- **100-500 citizens**: Headless mode recommended
- **500-1000 citizens**: Headless only, long-running experiments

### Headless Mode Benefits
- **No GPU usage** - runs entirely on CPU
- **Faster tick rate** - 10-50x speed boost
- **Background process** - work on other tasks
- **Auto-save** - data persists every 100 ticks

---

## Future Enhancements (LLM Integration Path)

Your implementation guide specifies LLM-powered agents. This is the **Phase 2 roadmap**:

### Current System (Behavior Trees)
- Fast, deterministic, scalable
- Good for initial experiments
- No API costs
- Works offline

### Future LLM Integration
- Replace behavior trees with LLM reasoning (GPT-4, Claude, Llama)
- Natural language communication between agents
- Richer personality evolution
- More emergent cultural patterns

**Migration Path**:
1. Keep current system for baseline data
2. Add LLM module as optional decision-maker
3. Compare behavior tree vs. LLM outcomes
4. Gradually increase LLM autonomy

This two-phase approach lets you:
- Run experiments NOW with current system
- Collect baseline behavioral data
- Compare AI decision systems (rules vs. LLM)
- Understand emergent patterns before adding LLM complexity

---

## Troubleshooting

### "Loading default citizen profiles" instead of CSV
**Issue**: CSV profiles not found
**Fix**: Run `python citizen_loader.py` in `mods/ai_civilization/scripts/`

### Simulation runs too fast/slow
**Visual Mode**: Use `--fps` flag (e.g., `--fps 15` for slower)
**Headless Mode**: This is normal - it runs as fast as CPU allows

### Citizens not interacting
- Check perception radius (default: 50 + extraversion*50)
- Ensure citizens are spawning close enough
- Reduce world size in `simulation.py` (default: 1280x720)

### Out of memory (1000 citizens)
- Use headless mode (`--headless`)
- Reduce citizen count (`--citizens 100`)
- Increase save interval in `simulation.py` (default: 100 ticks)

---

## License & Credits

**Copyright 2025 Intellegix**
Licensed under the Apache License, Version 2.0

**Built On**:
- Behavior Tree architecture from AI City Experiment
- Citizen infrastructure from your CSV data
- Tuxemon framework (optional, currently unused)

**Acknowledgments**:
- Designed for AMD Radeon 780M optimization
- Based on your comprehensive citizen foundational infrastructure
- Implements minimal-bias social experiment principles

---

## Contact & Contributions

This is a **raw social experiment** platform. Findings and insights are the primary goal.

**Experiment Design**: Based on your citizen infrastructure and implementation guide
**Technical Implementation**: Intellegix AI systems + your CSV profiles
**Research Focus**: Understanding true AI social behavior without predetermined outcomes

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Visual mode | `launch_ai_civilization.bat` |
| Headless mode | `launch_ai_civilization_headless.bat` |
| Quick test | `launch_ai_civilization_quick_test.bat` |
| Pause/Resume | SPACE (visual mode) |
| Toggle stats | S (visual mode) |
| Toggle relationships | R (visual mode) |
| Quit | Q or Ctrl+C |
| Custom citizens | `--citizens N` |
| Set time limit | `--max-ticks N` |
| Change FPS | `--fps N` |

**Data Location**: `experiments/experiment_<timestamp>/`

**Citizen Count**: 1000 available from CSV (use any subset)

**Recommended Start**: 50 citizens, visual mode, no time limit

---

**Happy Experimenting! Observe. Analyze. Discover.**
