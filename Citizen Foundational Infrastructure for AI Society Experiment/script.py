
import json
import random

# Define foundational citizen infrastructure for AI society experiment
# Goal: Minimal but sufficient seed data for diverse socioeconomic representation
# Avoid pre-programming biases - let AI agents develop naturally through interaction

# Define demographic distributions based on real-world data
age_brackets = [
    {"range": "18-24", "percentage": 0.12},
    {"range": "25-34", "percentage": 0.18},
    {"range": "35-44", "percentage": 0.16},
    {"range": "45-54", "percentage": 0.15},
    {"range": "55-64", "percentage": 0.16},
    {"range": "65+", "percentage": 0.23}
]

# Simplified socioeconomic tiers without prescriptive characteristics
income_tiers = [
    {"tier": "lower", "percentage": 0.32},
    {"tier": "middle", "percentage": 0.52},
    {"tier": "upper", "percentage": 0.16}
]

# Minimal education levels as foundation
education_levels = [
    {"level": "secondary", "percentage": 0.38},
    {"level": "bachelor", "percentage": 0.35},
    {"level": "graduate", "percentage": 0.15},
    {"level": "vocational", "percentage": 0.12}
]

# Broad occupation categories without stereotyping
occupation_categories = [
    "service",
    "technical",
    "creative",
    "administrative",
    "healthcare",
    "education",
    "trade",
    "independent"
]

# Basic personality trait ranges (Big Five) - neutral starting points
personality_dimensions = {
    "openness": {"min": 2, "max": 8, "neutral": 5},
    "conscientiousness": {"min": 2, "max": 8, "neutral": 5},
    "extraversion": {"min": 2, "max": 8, "neutral": 5},
    "agreeableness": {"min": 2, "max": 8, "neutral": 5},
    "neuroticism": {"min": 2, "max": 8, "neutral": 5}
}

# Location types for diversity
location_types = [
    "urban_core",
    "urban_peripheral",
    "suburban",
    "small_town",
    "rural"
]

print("=" * 80)
print("CITIZEN FOUNDATIONAL INFRASTRUCTURE - AI SOCIETY EXPERIMENT")
print("=" * 80)
print("\n## DESIGN PHILOSOPHY ##")
print("- Minimal seed data: Only essential demographic markers")
print("- No predetermined biases or behavioral programming")
print("- Agents develop through natural interaction and emergence")
print("- Representative of diverse socioeconomic backgrounds")
print("- Raw experimentation for authentic AI social dynamics")
print("\n" + "=" * 80)

# Create citizen template structure
citizen_template = {
    "demographics": {
        "age_bracket": None,
        "location_type": None
    },
    "socioeconomic": {
        "income_tier": None,
        "education_level": None,
        "occupation_category": None
    },
    "initial_state": {
        "personality_seed": {},  # Minimal seed, will develop naturally
        "resources": None,  # Basic starting resources based on tier
        "social_network_size": None  # Initial connections
    },
    "memory_system": {
        "type": "episodic_semantic",  # Stores experiences and learned knowledge
        "capacity": "unlimited",
        "decay": "natural"  # Memories fade without reinforcement
    },
    "decision_framework": {
        "model": "needs_based",  # Based on Maslow hierarchy
        "autonomy": "high",  # Agents make own choices
        "influenced_by": ["environment", "interactions", "experiences"]
    }
}

print("\n## CITIZEN TEMPLATE STRUCTURE ##")
print(json.dumps(citizen_template, indent=2))
print("\n" + "=" * 80)

# Generate sample population distribution for 1000 citizens
print("\n## SAMPLE POPULATION DISTRIBUTION (n=1000) ##\n")

population_size = 1000
citizens_data = []

# Age distribution
print("AGE DISTRIBUTION:")
for bracket in age_brackets:
    count = int(population_size * bracket["percentage"])
    print(f"  {bracket['range']}: {count} citizens ({bracket['percentage']*100:.0f}%)")

# Income distribution
print("\nINCOME TIER DISTRIBUTION:")
for tier in income_tiers:
    count = int(population_size * tier["percentage"])
    print(f"  {tier['tier'].capitalize()}: {count} citizens ({tier['percentage']*100:.0f}%)")

# Education distribution
print("\nEDUCATION LEVEL DISTRIBUTION:")
for edu in education_levels:
    count = int(population_size * edu["percentage"])
    print(f"  {edu['level'].capitalize()}: {count} citizens ({edu['percentage']*100:.0f}%)")

# Location distribution (equal for simplicity)
print("\nLOCATION TYPE DISTRIBUTION:")
location_dist = population_size / len(location_types)
for loc in location_types:
    print(f"  {loc.replace('_', ' ').title()}: {int(location_dist)} citizens (~{(1/len(location_types))*100:.0f}%)")

print("\nOCCUPATION CATEGORIES (Evenly distributed):")
for occ in occupation_categories:
    print(f"  - {occ.capitalize()}")

print("\n" + "=" * 80)

# Define minimal initialization parameters
initialization_params = {
    "population_size": 1000,
    "initial_resources": {
        "lower": {"range": [100, 500], "unit": "currency"},
        "middle": {"range": [501, 2000], "unit": "currency"},
        "upper": {"range": [2001, 10000], "unit": "currency"}
    },
    "initial_social_connections": {
        "lower": {"range": [2, 8]},
        "middle": {"range": [5, 15]},
        "upper": {"range": [8, 25]}
    },
    "personality_initialization": "random_normal",  # Random normal distribution around neutral (5)
    "environmental_conditions": {
        "shared_resources": ["public_spaces", "infrastructure", "information"],
        "scarcity_level": "moderate",
        "opportunity_distribution": "varied"  # Not uniform, creates realistic competition
    },
    "interaction_rules": {
        "frequency": "agent_determined",  # Agents decide when to interact
        "communication": "open",  # No restrictions on communication
        "cooperation_mechanics": "emergent",  # Not pre-programmed
        "conflict_resolution": "negotiated"  # Agents must resolve conflicts
    },
    "observation_metrics": [
        "social_network_evolution",
        "resource_distribution_changes",
        "cooperation_vs_competition_ratios",
        "norm_formation",
        "personality_trait_shifts",
        "inequality_measures",
        "collective_decision_patterns",
        "innovation_emergence",
        "cultural_formation"
    ]
}

print("\n## INITIALIZATION PARAMETERS ##")
print(json.dumps(initialization_params, indent=2))

print("\n" + "=" * 80)
print("\n## KEY PRINCIPLES FOR UNBIASED EXPERIMENTATION ##\n")

principles = [
    {
        "principle": "Minimal Intervention",
        "description": "Provide only essential demographic markers without behavioral prescriptions"
    },
    {
        "principle": "Natural Emergence",
        "description": "Allow social structures, norms, and behaviors to emerge from agent interactions"
    },
    {
        "principle": "Diverse Starting Conditions",
        "description": "Ensure population represents realistic socioeconomic diversity"
    },
    {
        "principle": "Equal Agency",
        "description": "All agents have equal decision-making autonomy regardless of tier"
    },
    {
        "principle": "Transparent Memory",
        "description": "Agents learn from experiences without hidden biases in memory retrieval"
    },
    {
        "principle": "Environmental Realism",
        "description": "Create realistic constraints (resources, opportunities) without deterministic outcomes"
    },
    {
        "principle": "Observable Dynamics",
        "description": "Track measurable outcomes to understand AI social behavior vs human society"
    }
]

for i, p in enumerate(principles, 1):
    print(f"{i}. {p['principle']}")
    print(f"   → {p['description']}\n")

print("=" * 80)

# Create a sample citizen profile generator
def generate_citizen_profile(citizen_id):
    """Generate a single citizen profile with minimal seed data"""
    
    # Randomly assign based on distributions
    age = random.choices([b["range"] for b in age_brackets], 
                         weights=[b["percentage"] for b in age_brackets])[0]
    
    income = random.choices([t["tier"] for t in income_tiers],
                           weights=[t["percentage"] for t in income_tiers])[0]
    
    education = random.choices([e["level"] for e in education_levels],
                              weights=[e["percentage"] for e in education_levels])[0]
    
    location = random.choice(location_types)
    occupation = random.choice(occupation_categories)
    
    # Generate neutral personality traits with slight variation
    personality = {}
    for trait, params in personality_dimensions.items():
        # Normal distribution around neutral point with some variance
        value = random.gauss(params["neutral"], 1.5)
        value = max(params["min"], min(params["max"], value))
        personality[trait] = round(value, 1)
    
    # Assign resources based on tier
    resource_range = initialization_params["initial_resources"][income]
    resources = random.randint(resource_range["range"][0], resource_range["range"][1])
    
    # Assign initial social connections
    connection_range = initialization_params["initial_social_connections"][income]
    connections = random.randint(connection_range["range"][0], connection_range["range"][1])
    
    return {
        "id": f"citizen_{citizen_id:04d}",
        "demographics": {
            "age_bracket": age,
            "location_type": location
        },
        "socioeconomic": {
            "income_tier": income,
            "education_level": education,
            "occupation_category": occupation
        },
        "initial_state": {
            "personality_seed": personality,
            "resources": resources,
            "social_network_size": connections
        }
    }

# Generate sample citizens
print("\n## SAMPLE CITIZEN PROFILES ##\n")

sample_citizens = []
for i in range(5):
    citizen = generate_citizen_profile(i)
    sample_citizens.append(citizen)
    print(f"Citizen ID: {citizen['id']}")
    print(f"  Age: {citizen['demographics']['age_bracket']}, Location: {citizen['demographics']['location_type']}")
    print(f"  Income Tier: {citizen['socioeconomic']['income_tier']}, Education: {citizen['socioeconomic']['education_level']}")
    print(f"  Occupation: {citizen['socioeconomic']['occupation_category']}")
    print(f"  Starting Resources: {citizen['initial_state']['resources']} currency")
    print(f"  Initial Connections: {citizen['initial_state']['social_network_size']}")
    print(f"  Personality Traits: O={citizen['initial_state']['personality_seed']['openness']}, "
          f"C={citizen['initial_state']['personality_seed']['conscientiousness']}, "
          f"E={citizen['initial_state']['personality_seed']['extraversion']}, "
          f"A={citizen['initial_state']['personality_seed']['agreeableness']}, "
          f"N={citizen['initial_state']['personality_seed']['neuroticism']}")
    print()

print("=" * 80)
print("\nInfrastructure complete. Ready for AI society simulation experiment.")
print("=" * 80)
