"""
Citizen Loader - Loads citizen infrastructure from CSV

Converts the pre-built citizen infrastructure into our simulation format.
Supports 1000+ citizens with diverse backgrounds from CSV data.

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import csv
import json
from pathlib import Path
from typing import List, Dict, Any


class CitizenLoader:
    """Loads and converts citizen data from CSV infrastructure"""

    # Mapping from CSV values to our system
    LOCATION_MAPPING = {
        'urban_core': 'urban_core',
        'urban_peripheral': 'urban_peripheral',
        'suburban': 'suburban',
        'small_town': 'small_town',
        'rural': 'rural'
    }

    INCOME_MAPPING = {
        'lower': 'low',
        'middle': 'mid',
        'upper': 'high'
    }

    @staticmethod
    def load_from_csv(csv_path: str, max_citizens: int = None) -> List[Dict[str, Any]]:
        """
        Load citizen profiles from CSV file.

        Args:
            csv_path: Path to CSV file
            max_citizens: Maximum number of citizens to load (None = all)

        Returns:
            List of citizen profile dictionaries
        """
        citizens = []

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                if max_citizens and i >= max_citizens:
                    break

                # Convert CSV row to citizen profile
                profile = CitizenLoader._convert_row_to_profile(row)
                citizens.append(profile)

        print(f"Loaded {len(citizens)} citizens from {csv_path}")
        return citizens

    @staticmethod
    def _convert_row_to_profile(row: Dict[str, str]) -> Dict[str, Any]:
        """Convert CSV row to citizen profile format"""

        # Normalize personality traits (CSV: 0-10, System: 0.0-1.0)
        personality = {
            'openness': float(row['personality_openness']) / 10.0,
            'conscientiousness': float(row['personality_conscientiousness']) / 10.0,
            'extraversion': float(row['personality_extraversion']) / 10.0,
            'agreeableness': float(row['personality_agreeableness']) / 10.0,
            'neuroticism': float(row['personality_neuroticism']) / 10.0
        }

        # Determine archetype from occupation
        archetype = CitizenLoader._occupation_to_archetype(
            row['occupation_category']
        )

        # Starting resources (money)
        starting_money = int(float(row['starting_resources']))

        # Determine starting items based on occupation and income
        starting_items = CitizenLoader._generate_starting_items(
            row['occupation_category'],
            row['income_tier'],
            row['education_level']
        )

        # Location type for starting position
        location_type = CitizenLoader.LOCATION_MAPPING.get(
            row['location_type'],
            'urban_core'
        )

        # Build profile
        profile = {
            'id': row['citizen_id'],
            'archetype': archetype,
            'age_bracket': row['age_bracket'],
            'location_type': location_type,
            'income_tier': row['income_tier'],
            'education_level': row['education_level'],
            'occupation_category': row['occupation_category'],
            'initial_connections': int(row['initial_connections']),

            'starting_resources': {
                'money': starting_money,
                'items': starting_items
            },

            'personality_seed': personality,

            # Additional metadata
            'metadata': {
                'source': 'csv_infrastructure',
                'original_id': row['citizen_id']
            }
        }

        return profile

    @staticmethod
    def _occupation_to_archetype(occupation: str) -> str:
        """Map occupation to archetype"""
        occupation_mapping = {
            'service': 'service_worker',
            'administrative': 'office_worker',
            'technical': 'tech_worker',
            'healthcare': 'healthcare_worker',
            'education': 'teacher',
            'trade': 'tradesperson',
            'creative': 'artist',
            'independent': 'entrepreneur'
        }
        return occupation_mapping.get(occupation, 'civilian')

    @staticmethod
    def _generate_starting_items(occupation: str, income: str, education: str) -> List[str]:
        """Generate starting items based on background"""
        items = []

        # Container based on income
        if income == 'lower':
            items.append('basic_backpack')
        elif income == 'middle':
            items.append('backpack')
        else:  # upper
            items.append('laptop_bag' if occupation == 'technical' else 'backpack')

        # Occupation-specific items
        occupation_items = {
            'service': ['water_bottle'],
            'administrative': ['smartphone', 'coffee'],
            'technical': ['laptop', 'smartphone'] if income == 'upper' else ['smartphone'],
            'healthcare': ['medical_supplies' if income != 'lower' else 'first_aid', 'id_badge'],
            'education': ['books', 'coffee'],
            'trade': ['work_gloves', 'lunch_box'],
            'creative': ['sketchbook', 'phone'],
            'independent': ['smartphone', 'business_supplies'] if income == 'upper' else ['phone', 'notebook']
        }

        items.extend(occupation_items.get(occupation, ['water_bottle']))

        # Education-based items
        if education in ['bachelor', 'graduate']:
            if 'smartphone' not in items and 'phone' not in items:
                items.append('smartphone' if income != 'lower' else 'phone')

        return items

    @staticmethod
    def save_profiles_to_json(citizens: List[Dict], output_path: str):
        """Save citizen profiles to JSON format"""
        data = {
            'description': 'Citizen profiles loaded from CSV infrastructure',
            'version': '2.0',
            'source': 'ai_society_citizens_infrastructure.csv',
            'count': len(citizens),
            'profiles': citizens
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(citizens)} profiles to {output_path}")


def main():
    """Convert CSV to JSON profiles"""
    import os

    # Paths
    csv_path = os.path.join(
        os.path.dirname(__file__),
        '../../../Citizen Foundational Infrastructure for AI Society Experiment',
        'ai_society_citizens_infrastructure.csv'
    )

    json_path = os.path.join(
        os.path.dirname(__file__),
        '../db/citizen_profiles_from_csv.json'
    )

    # Load citizens
    citizens = CitizenLoader.load_from_csv(csv_path)

    # Save to JSON
    CitizenLoader.save_profiles_to_json(citizens, json_path)

    # Print sample
    if citizens:
        print("\nSample citizen profile:")
        print(json.dumps(citizens[0], indent=2))

        # Print statistics
        print(f"\nStatistics:")
        print(f"Total citizens: {len(citizens)}")
        print(f"Archetypes: {len(set(c['archetype'] for c in citizens))}")
        print(f"Income tiers: {set(c['income_tier'] for c in citizens)}")
        print(f"Age brackets: {set(c['age_bracket'] for c in citizens)}")


if __name__ == "__main__":
    main()
