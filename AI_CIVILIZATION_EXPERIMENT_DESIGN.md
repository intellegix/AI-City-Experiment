# AI Civilization Experiment - Tuxemon Framework Design

**Project**: AI Social Behavior Simulation using Tuxemon Framework
**Goal**: Create a lightweight 2D world where AI agents form a civilization and exhibit emergent social behaviors
**Date**: October 20, 2025
**Hardware Target**: AMD Radeon 780M (optimized for 2D, low graphics overhead)

---

## Executive Summary

This project pivots from the graphics-intensive 3D city simulation to a **Tuxemon-based AI civilization experiment**. We leverage Tuxemon's lightweight 2D engine while integrating our sophisticated AI behavior systems (behavior trees, utility AI, memory) to create AI "trainers" that form societies, interact, and exhibit emergent behaviors.

---

## 1. Architecture Overview

### 1.1 Core Systems Integration

```
┌─────────────────────────────────────────────────────────┐
│             Tuxemon Framework (Base)                    │
│  - Pygame 2D Rendering (lightweight)                    │
│  - Tiled Map Editor integration                         │
│  - Event/Dialog System                                  │
│  - JSON-based data management                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│          AI Civilization Layer (Custom)                 │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Behavior Trees│  │  Utility AI  │  │ Memory System│ │
│  │ (from current)│  │ (from current)│  │(from current)│ │
│  └───────────────┘  └──────────────┘  └──────────────┘ │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ AI Trainers   │  │Social Dynamics│ │   Economy    │ │
│  │ (NPCs as AI)  │  │ (relationships)│ │(resource mgmt)│ │
│  └───────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│         Experiment & Metrics Layer                      │
│  - Behavior Data Collection                             │
│  - Social Network Analysis                              │
│  - Civilization Metrics (cooperation, conflict, trade)  │
│  - JSON/CSV export for analysis                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Key Components

**From Existing AI City Project (Reuse)**:
- `ai_behavior.py` - Behavior tree framework (465 lines)
- `npc_system.py` - NPC agents with needs/memory (530 lines)
- `pathfinding.py` - A* algorithm (400 lines)
- `config.py` - Configuration system

**New Tuxemon Integration**:
- `tuxemon_ai_trainer.py` - AI agents as trainers
- `civilization_manager.py` - Social dynamics, economy, relationships
- `experiment_metrics.py` - Data collection and analysis
- `tuxemon_adapter.py` - Bridge between Tuxemon events and AI system

---

## 2. AI Agent Design (Trainers as Civilization Members)

### 2.1 AI Trainer Class

AI trainers replace traditional NPCs with intelligent agents that:
- Have **internal needs** (hunger, rest, social, safety, achievement)
- Make **utility-based decisions** using behavior trees
- Form **relationships** with other trainers (friendship, rivalry, alliance)
- Participate in **economy** (trade items, share resources)
- Have **memory** of interactions and events
- **Learn** from experiences (basic reinforcement)

### 2.2 Trainer Types

1. **Explorer** - Seeks new areas, discovers resources, maps territory
2. **Trader** - Focuses on economy, exchanges items, builds wealth
3. **Socialite** - Prioritizes relationships, organizes events, mediates conflicts
4. **Competitor** - Battles frequently, builds strong team, seeks challenges
5. **Builder** - Establishes "bases" (homes), organizes community resources
6. **Scholar** - Researches creatures, optimizes strategies, shares knowledge

### 2.3 Internal Needs & Utility Scoring

```python
# Adapted from existing npc_system.py
class AITrainer:
    def __init__(self, name, trainer_type):
        self.name = name
        self.type = trainer_type

        # Internal needs (0.0 - 1.0)
        self.needs = {
            "hunger": 0.5,      # Need for items (food, potions)
            "rest": 0.5,        # Need to visit Pokemon Center or home
            "social": 0.5,      # Need to interact with others
            "safety": 1.0,      # Avoid danger, heal team
            "achievement": 0.3, # Desire to battle, catch, explore
            "wealth": 0.3       # Desire to acquire items/money
        }

        # Personality modifiers (affects utility calculations)
        self.personality = {
            "aggression": 0.5,   # Likelihood to battle
            "generosity": 0.5,   # Likelihood to share/trade
            "curiosity": 0.5,    # Likelihood to explore
            "caution": 0.5       # Risk aversion
        }

        # Memory system (from existing)
        self.memory = MemorySystem(max_size=50)

        # Relationships (other trainers)
        self.relationships = {}  # {trainer_id: relationship_value}

        # Tuxemon integration
        self.party = []  # Tuxemon creatures
        self.inventory = []
        self.money = 100
        self.location = (0, 0)
```

### 2.4 Behavior Tree Structure

```
Root (Selector)
├── Emergency Behaviors (Sequence)
│   ├── Check if team fainted → Go to Pokemon Center
│   ├── Check if low on money → Seek trading opportunity
│   └── Check if threatened → Flee or battle
├── Need-Based Behaviors (Utility Selector)
│   ├── If hungry > 0.7 → Find/Buy food items
│   ├── If rest > 0.7 → Visit Pokemon Center or home base
│   ├── If social > 0.6 → Seek other trainers to chat/battle
│   ├── If safety < 0.3 → Heal team, avoid battles
│   └── If achievement > 0.6 → Explore new areas, catch creatures
└── Idle Behaviors
    ├── Wander current area
    ├── Check inventory
    └── Rest at current location
```

---

## 3. Social Dynamics System

### 3.1 Relationship Mechanics

**Relationship Values**: -100 (enemy) to +100 (best friend)

**Relationship Modifiers**:
- Successful trade: +5 to +15
- Battle outcome: Winner +2, Loser -3
- Sharing items: +10
- Helping when in need: +20
- Ignoring request for help: -10
- Stealing/betrayal: -50

**Relationship Effects**:
- **Friends (50+)**: Share items freely, team up for exploration, avoid battles
- **Neutral (0-49)**: Normal trading, occasional battles, casual interaction
- **Rivals (-1 to -49)**: Competitive battles, less likely to trade fairly
- **Enemies (-50+)**: Actively seek battles, refuse cooperation

### 3.2 Social Events

AI trainers can initiate social events based on needs:
- **Trading Meetup**: Exchange items based on needs and surplus
- **Battle Tournament**: Multiple trainers compete (social + achievement)
- **Exploration Party**: Group explores new area (safety in numbers)
- **Resource Sharing**: Trainers with surplus help those in need
- **Alliance Formation**: Groups form for mutual benefit

### 3.3 Emergent Social Structures

Expected emergent behaviors:
- **Trading Networks**: Trainers specialize (item collectors, battlers) and trade
- **Alliances**: Groups form based on shared goals (explorers, competitors)
- **Territorial Behavior**: Trainers claim areas as "home base"
- **Conflict Resolution**: Mediators (Socialite types) reduce tensions
- **Knowledge Sharing**: Scholars share creature locations, strategies

---

## 4. Economy System

### 4.1 Resources

**Primary Resources**:
1. **Money** - Earned from battles, trading
2. **Items** - Potions, food, Pokeballs, evolution stones
3. **Creatures** - Can be traded (rare creatures more valuable)
4. **Territory** - Access to spawn areas, resources

### 4.2 Economic Behaviors

**Resource Acquisition**:
- Battle wild creatures for experience/money
- Find items in exploration
- Receive from other trainers (trade/gift)

**Resource Allocation**:
- Spend money on items at "shops" (NPC or AI-run)
- Trade items with other trainers
- Use items to satisfy needs (healing, catching)

**Supply & Demand**:
- Track global item scarcity
- Prices adjust based on demand
- Rare items command higher trade value

### 4.3 Trading Protocol

```python
class TradeOffer:
    def __init__(self, trader_a, trader_b, offer_a, request_b):
        self.trader_a = trainer_a
        self.trader_b = trainer_b
        self.offer = offer_a      # Items/creatures offered
        self.request = request_b   # Items/creatures requested

    def evaluate_fairness(self):
        """Use utility AI to determine if trade is fair"""
        value_offered = self.calculate_value(self.offer, self.trader_b)
        value_requested = self.calculate_value(self.request, self.trader_a)
        return abs(value_offered - value_requested) < threshold

    def apply_relationship_modifier(self):
        """Friends give better deals"""
        relationship = self.trader_a.relationships.get(self.trader_b.id, 0)
        if relationship > 50:
            return 0.8  # Friends offer 20% discount
        elif relationship < -50:
            return 1.3  # Enemies charge 30% premium
        return 1.0
```

---

## 5. Experiment Metrics & Data Collection

### 5.1 Individual Metrics (Per Trainer)

**Behavior Metrics**:
- Total battles initiated vs. accepted
- Items traded vs. shared (generosity)
- Time spent exploring vs. socializing vs. battling
- Number of alliances formed/broken
- Wealth accumulation over time
- Creature team diversity

**Social Metrics**:
- Relationship network (graph structure)
- Average relationship value
- Number of friends, neutrals, enemies
- Social events participated in
- Times helped vs. ignored requests

**Efficiency Metrics**:
- Needs satisfaction rate (how often needs met)
- Resource utilization efficiency
- Survival rate (team health maintenance)
- Goal achievement rate

### 5.2 Civilization-Level Metrics

**Social Structure**:
- Network clustering coefficient (tight-knit groups)
- Centrality measures (influential trainers)
- Alliance sizes and stability
- Conflict frequency and resolution

**Economic Health**:
- Wealth distribution (Gini coefficient)
- Trade volume over time
- Resource scarcity/abundance
- Market efficiency (fair trades vs. exploitation)

**Emergent Behaviors**:
- Specialization (role differentiation)
- Cooperation vs. competition ratio
- Territory establishment and disputes
- Knowledge propagation (strategies spread)

### 5.3 Data Export Format

**JSON Export** (per simulation tick):
```json
{
  "timestamp": 1234567890,
  "tick": 5000,
  "trainers": [
    {
      "id": "trainer_001",
      "name": "Explorer Alice",
      "type": "explorer",
      "location": [45, 67],
      "needs": {"hunger": 0.3, "rest": 0.5, ...},
      "relationships": {"trainer_002": 75, "trainer_003": -20},
      "wealth": 450,
      "party_count": 4,
      "actions_taken": ["explore", "catch", "trade"]
    }
  ],
  "events": [
    {"type": "trade", "participants": ["trainer_001", "trainer_002"], "outcome": "success"},
    {"type": "battle", "participants": ["trainer_003", "trainer_004"], "winner": "trainer_003"}
  ],
  "metrics": {
    "total_trades": 45,
    "total_battles": 23,
    "avg_relationship": 12.5,
    "wealth_gini": 0.34
  }
}
```

---

## 6. Technical Implementation Plan

### 6.1 Phase 1: Setup & Integration (Days 1-2)
1. Clone Tuxemon repository
2. Set up Python environment (3.9+)
3. Create custom mod structure for AI experiment
4. Extract AI systems from current project (behavior trees, utility AI, memory)
5. Test Tuxemon baseline (ensure it runs on AMD 780M)

### 6.2 Phase 2: Core AI Trainer System (Days 3-5)
1. Implement `AITrainer` class with needs/personality
2. Adapt behavior tree system to Tuxemon actions
3. Integrate memory system
4. Create basic utility-based decision making
5. Test single AI trainer in Tuxemon world

### 6.3 Phase 3: Social Dynamics (Days 6-8)
1. Implement relationship system
2. Create social interaction events (chat, trade, battle)
3. Build alliance/rivalry mechanics
4. Test multi-trainer interactions (5-10 trainers)

### 6.4 Phase 4: Economy & Trading (Days 9-11)
1. Implement trading protocol
2. Create supply/demand system
3. Build resource acquisition behaviors
4. Test economic emergent behaviors (market formation)

### 6.5 Phase 5: Metrics & Analysis (Days 12-14)
1. Implement data collection system
2. Create JSON/CSV export
3. Build visualization tools (network graphs, charts)
4. Run controlled experiments (different trainer mixes)

### 6.6 Phase 6: Optimization & Scaling (Days 15-16)
1. Performance profiling (AMD 780M target)
2. Optimize AI update frequency (tick-based)
3. Scale up to 20-50 trainers
4. Test long-running simulations (1000+ ticks)

---

## 7. Advantages Over 3D City Simulation

### 7.1 Performance Benefits
- **2D rendering**: ~90% less GPU load compared to 3D
- **No LOD system needed**: Simple sprite rendering
- **Lower memory footprint**: No 3D models/textures
- **Better scalability**: Can run 50+ AI agents smoothly

### 7.2 Development Benefits
- **Established framework**: Tuxemon handles rendering, input, maps
- **JSON-based content**: Easy to modify world, creatures, items
- **Tiled integration**: Visual map editor, no procedural generation complexity
- **Focus on AI**: More time for behavior complexity, less on graphics

### 7.3 Experimental Benefits
- **Clearer observations**: 2D top-down view easier to analyze
- **Controlled environment**: Tuxemon's game rules provide structure
- **Quantifiable interactions**: Battles, trades, catches are discrete events
- **Rich behavior space**: Creature collection adds another dimension to AI goals

---

## 8. Success Criteria

### 8.1 Minimum Viable Experiment (MVP)
- 10 AI trainers running simultaneously
- Trainers exhibit need-based behaviors (hunger → find food)
- Trainers form relationships (positive and negative)
- At least 5 trades occur naturally
- At least 10 battles occur (competitive + friendly)
- Simulation runs at 30+ FPS on AMD 780M
- Data export captures all interactions

### 8.2 Desired Outcomes
- 25-50 AI trainers with diverse behaviors
- Emergent social structures (alliances, rivalries)
- Functioning economy (market for items/creatures)
- Specialization (trainers adopt roles)
- Measurable cooperation and conflict
- Long-running stability (10,000+ ticks without crashes)

### 8.3 Research Questions to Answer
1. **Do AI agents naturally specialize?** (Explorers, Traders, Battlers)
2. **How do relationships affect cooperation?** (Friends share, enemies compete)
3. **What economic patterns emerge?** (Wealth inequality, trade networks)
4. **Can AI agents form stable alliances?** (Groups persist over time)
5. **How does personality affect civilization?** (Aggressive vs. Cooperative societies)

---

## 9. File Structure (Proposed)

```
AI_City_Experiment/
├── tuxemon/                      # Cloned Tuxemon framework
│   └── (Tuxemon core files)
├── mods/
│   └── ai_civilization/          # Custom mod for experiment
│       ├── maps/                 # Tiled maps
│       ├── db/
│       │   ├── creatures.json
│       │   ├── items.json
│       │   └── ai_trainers.json  # AI trainer definitions
│       └── scripts/
│           ├── ai_trainer.py
│           ├── civilization_manager.py
│           ├── experiment_metrics.py
│           └── tuxemon_adapter.py
├── ai_systems/                   # Extracted from current project
│   ├── ai_behavior.py            # Behavior tree framework
│   ├── npc_system.py             # Adapted for trainers
│   ├── pathfinding.py            # A* (if needed)
│   └── config.py                 # AI configuration
├── experiments/                  # Experiment results
│   ├── experiment_001/
│   │   ├── config.json
│   │   ├── data_export.json
│   │   └── analysis.ipynb        # Jupyter notebook for analysis
│   └── experiment_002/
├── analysis_tools/
│   ├── visualize_network.py      # Social network graphs
│   ├── plot_metrics.py           # Charts and statistics
│   └── export_csv.py             # CSV conversion
├── docs/
│   ├── AI_CIVILIZATION_EXPERIMENT_DESIGN.md  # This document
│   ├── EXPERIMENT_RESULTS.md
│   └── TUXEMON_INTEGRATION_GUIDE.md
└── README.md
```

---

## 10. Next Steps

1. **Get user approval** on this design
2. **Clone Tuxemon** and verify it runs
3. **Extract AI systems** from current project into reusable modules
4. **Create custom Tuxemon mod** structure
5. **Implement AITrainer** class with basic behaviors
6. **Test with 5 trainers** to validate concept
7. **Iterate based on findings**

---

**Questions for Discussion**:
1. Should we clone Tuxemon into this directory or keep it separate?
2. What specific experiment scenarios would you like to test first?
3. Should we visualize the simulation in real-time or run headless for speed?
4. Any specific metrics or behaviors you're most interested in observing?
