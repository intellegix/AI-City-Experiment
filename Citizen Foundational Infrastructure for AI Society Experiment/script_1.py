
import csv

# Create comprehensive CSV file with full citizen infrastructure

# Generate complete population of 1000 citizens
full_population = []

random.seed(42)  # For reproducibility

for i in range(1000):
    citizen = generate_citizen_profile(i)
    
    # Flatten for CSV
    flat_citizen = {
        "citizen_id": citizen["id"],
        "age_bracket": citizen["demographics"]["age_bracket"],
        "location_type": citizen["demographics"]["location_type"],
        "income_tier": citizen["socioeconomic"]["income_tier"],
        "education_level": citizen["socioeconomic"]["education_level"],
        "occupation_category": citizen["socioeconomic"]["occupation_category"],
        "starting_resources": citizen["initial_state"]["resources"],
        "initial_connections": citizen["initial_state"]["social_network_size"],
        "personality_openness": citizen["initial_state"]["personality_seed"]["openness"],
        "personality_conscientiousness": citizen["initial_state"]["personality_seed"]["conscientiousness"],
        "personality_extraversion": citizen["initial_state"]["personality_seed"]["extraversion"],
        "personality_agreeableness": citizen["initial_state"]["personality_seed"]["agreeableness"],
        "personality_neuroticism": citizen["initial_state"]["personality_seed"]["neuroticism"]
    }
    
    full_population.append(flat_citizen)

# Save to CSV
csv_filename = "ai_society_citizens_infrastructure.csv"
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = full_population[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for citizen in full_population:
        writer.writerow(citizen)

print(f"✓ Created {csv_filename} with {len(full_population)} citizen profiles")

# Generate statistics
print("\n## FULL POPULATION STATISTICS ##\n")

# Age distribution
age_counts = {}
for c in full_population:
    age = c["age_bracket"]
    age_counts[age] = age_counts.get(age, 0) + 1

print("Age Distribution:")
for age, count in sorted(age_counts.items()):
    print(f"  {age}: {count} citizens ({count/10:.1f}%)")

# Income distribution
income_counts = {}
for c in full_population:
    tier = c["income_tier"]
    income_counts[tier] = income_counts.get(tier, 0) + 1

print("\nIncome Tier Distribution:")
for tier in ["lower", "middle", "upper"]:
    count = income_counts.get(tier, 0)
    print(f"  {tier.capitalize()}: {count} citizens ({count/10:.1f}%)")

# Location distribution
location_counts = {}
for c in full_population:
    loc = c["location_type"]
    location_counts[loc] = location_counts.get(loc, 0) + 1

print("\nLocation Type Distribution:")
for loc, count in sorted(location_counts.items()):
    print(f"  {loc.replace('_', ' ').title()}: {count} citizens ({count/10:.1f}%)")

# Resource statistics by tier
print("\nStarting Resources by Income Tier:")
for tier in ["lower", "middle", "upper"]:
    tier_resources = [c["starting_resources"] for c in full_population if c["income_tier"] == tier]
    avg_resources = sum(tier_resources) / len(tier_resources)
    min_resources = min(tier_resources)
    max_resources = max(tier_resources)
    print(f"  {tier.capitalize()}: avg={avg_resources:.0f}, range=[{min_resources}-{max_resources}]")

# Personality statistics
print("\nPersonality Trait Averages (Scale: 2-8, Neutral: 5):")
traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
for trait in traits:
    values = [c[f"personality_{trait}"] for c in full_population]
    avg = sum(values) / len(values)
    print(f"  {trait.capitalize()}: {avg:.2f}")

print(f"\n✓ Full population infrastructure ready for simulation")
