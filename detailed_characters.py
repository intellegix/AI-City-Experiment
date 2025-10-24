"""
Detailed Character System - Realistic NPCs
Creates detailed pedestrians with body parts and variations

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from typing import Tuple, List, Dict
from enum import Enum


class CharacterType(Enum):
    """Character categories"""
    BUSINESS_PERSON = 0
    CASUAL_PEDESTRIAN = 1
    WORKER = 2
    ELDERLY = 3
    STUDENT = 4
    JOGGER = 5
    SHOPPER = 6


class Gender(Enum):
    """Gender options"""
    MALE = 0
    FEMALE = 1


class DetailedCharacter:
    """
    Detailed pedestrian character with realistic proportions.

    Features:
    - Body parts (head, torso, arms, legs)
    - Clothing variations by character type
    - Accessories (bags, hats, glasses)
    - Realistic proportions
    - Gender variations
    - Walking animation support
    """

    # Clothing colors
    SHIRT_COLORS = [
        (0.15, 0.25, 0.55, 1.0),   # Dark blue
        (0.85, 0.85, 0.90, 1.0),   # White
        (0.12, 0.12, 0.15, 1.0),   # Black
        (0.70, 0.15, 0.15, 1.0),   # Red
        (0.25, 0.55, 0.30, 1.0),   # Green
        (0.65, 0.55, 0.45, 1.0),   # Tan
        (0.55, 0.55, 0.60, 1.0),   # Gray
        (0.75, 0.60, 0.40, 1.0),   # Brown
    ]

    PANTS_COLORS = [
        (0.20, 0.25, 0.45, 1.0),   # Navy blue
        (0.15, 0.15, 0.18, 1.0),   # Black
        (0.40, 0.45, 0.55, 1.0),   # Gray
        (0.30, 0.35, 0.55, 1.0),   # Blue jeans
        (0.55, 0.45, 0.35, 1.0),   # Khaki
    ]

    SKIN_TONES = [
        (0.98, 0.85, 0.75, 1.0),   # Light
        (0.92, 0.75, 0.62, 1.0),   # Light-medium
        (0.85, 0.68, 0.52, 1.0),   # Medium
        (0.72, 0.55, 0.42, 1.0),   # Medium-dark
        (0.60, 0.45, 0.35, 1.0),   # Dark
        (0.45, 0.32, 0.25, 1.0),   # Deep
    ]

    HAIR_COLORS = [
        (0.12, 0.10, 0.08, 1.0),   # Black
        (0.35, 0.25, 0.18, 1.0),   # Dark brown
        (0.55, 0.42, 0.28, 1.0),   # Brown
        (0.72, 0.55, 0.38, 1.0),   # Light brown
        (0.85, 0.72, 0.45, 1.0),   # Blonde
        (0.65, 0.38, 0.28, 1.0),   # Auburn
        (0.60, 0.60, 0.62, 1.0),   # Gray
    ]

    def __init__(self, character_type: CharacterType = None, seed: int = None):
        """Initialize detailed character"""
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

        # Character attributes
        self.character_type = character_type or self._random_type()
        self.gender = self._random_gender()

        # Physical attributes
        self.height = self._determine_height()
        self.skin_tone = self._random_choice(self.SKIN_TONES)
        self.hair_color = self._random_choice(self.HAIR_COLORS)
        self.shirt_color = self._determine_shirt_color()
        self.pants_color = self._determine_pants_color()

        # Accessories
        self.has_bag = self._should_have_bag()
        self.has_hat = self._should_have_hat()
        self.has_glasses = np.random.random() > 0.7

        # Body proportions (based on height)
        self._calculate_proportions()

        # Animation state
        self.walk_cycle = 0.0

    def _random_type(self) -> CharacterType:
        """Random character type"""
        types = list(CharacterType)
        weights = [0.25, 0.30, 0.15, 0.10, 0.10, 0.05, 0.05]
        return np.random.choice(types, p=weights)

    def _random_gender(self) -> Gender:
        """Random gender"""
        return np.random.choice(list(Gender))

    def _determine_height(self) -> float:
        """Determine character height"""
        if self.character_type == CharacterType.ELDERLY:
            return np.random.uniform(1.55, 1.72)
        elif self.character_type == CharacterType.STUDENT:
            return np.random.uniform(1.60, 1.75)
        elif self.gender == Gender.FEMALE:
            return np.random.uniform(1.58, 1.72)
        else:  # Male
            return np.random.uniform(1.68, 1.85)

    def _determine_shirt_color(self) -> Tuple[float, float, float, float]:
        """Determine shirt color based on character type"""
        if self.character_type == CharacterType.BUSINESS_PERSON:
            # Business clothes - whites, light blues
            colors = [
                (0.88, 0.88, 0.92, 1.0),   # White
                (0.75, 0.82, 0.92, 1.0),   # Light blue
                (0.82, 0.78, 0.85, 1.0),   # Light purple
            ]
            return self._random_choice(colors)
        elif self.character_type == CharacterType.WORKER:
            # Work clothes - oranges, yellows, hi-vis
            colors = [
                (0.95, 0.55, 0.12, 1.0),   # Orange
                (0.95, 0.88, 0.18, 1.0),   # Yellow
                (0.25, 0.45, 0.65, 1.0),   # Blue
            ]
            return self._random_choice(colors)
        elif self.character_type == CharacterType.JOGGER:
            # Athletic wear - bright colors
            colors = [
                (0.85, 0.15, 0.15, 1.0),   # Red
                (0.15, 0.75, 0.25, 1.0),   # Green
                (0.15, 0.35, 0.85, 1.0),   # Blue
                (0.85, 0.45, 0.15, 1.0),   # Orange
            ]
            return self._random_choice(colors)
        else:
            return self._random_choice(self.SHIRT_COLORS)

    def _determine_pants_color(self) -> Tuple[float, float, float, float]:
        """Determine pants color"""
        if self.character_type == CharacterType.BUSINESS_PERSON:
            # Business pants - dark colors
            colors = [
                (0.12, 0.12, 0.15, 1.0),   # Black
                (0.25, 0.28, 0.35, 1.0),   # Charcoal
                (0.20, 0.25, 0.42, 1.0),   # Navy
            ]
            return self._random_choice(colors)
        elif self.character_type == CharacterType.JOGGER:
            # Athletic pants - dark or matching shirt
            return (0.15, 0.15, 0.18, 1.0)  # Black athletic
        else:
            return self._random_choice(self.PANTS_COLORS)

    def _should_have_bag(self) -> bool:
        """Determine if character has bag"""
        if self.character_type == CharacterType.BUSINESS_PERSON:
            return np.random.random() > 0.3  # 70% have bags
        elif self.character_type == CharacterType.SHOPPER:
            return np.random.random() > 0.1  # 90% have bags
        elif self.character_type == CharacterType.STUDENT:
            return np.random.random() > 0.2  # 80% have bags
        else:
            return np.random.random() > 0.7  # 30% have bags

    def _should_have_hat(self) -> bool:
        """Determine if character has hat"""
        if self.character_type == CharacterType.WORKER:
            return np.random.random() > 0.4  # 60% have hard hats
        elif self.character_type == CharacterType.ELDERLY:
            return np.random.random() > 0.6  # 40% have hats
        else:
            return np.random.random() > 0.8  # 20% have hats

    def _calculate_proportions(self):
        """Calculate body part proportions based on height"""
        # Standard human proportions
        self.head_height = self.height * 0.13
        self.neck_height = self.height * 0.05
        self.torso_height = self.height * 0.32
        self.leg_length = self.height * 0.50

        # Widths
        self.shoulder_width = self.height * 0.25
        self.waist_width = self.height * 0.18
        self.head_width = self.head_height * 0.75

        # Arm proportions
        self.upper_arm_length = self.height * 0.18
        self.forearm_length = self.height * 0.16
        self.arm_thickness = 0.08

        # Leg proportions
        self.upper_leg_length = self.leg_length * 0.52
        self.lower_leg_length = self.leg_length * 0.48
        self.leg_thickness = 0.12

    def _random_choice(self, choices: List) -> Tuple:
        """Random choice from list"""
        return choices[np.random.randint(0, len(choices))]

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float],
                       heading: float = 0, walk_progress: float = 0.0) -> NodePath:
        """Create detailed 3D character"""
        char_node = parent_node.attachNewNode(f"character_{self.character_type.name}_{self.seed}")
        char_node.setPos(*position)
        char_node.setH(heading)

        self.walk_cycle = walk_progress

        # Build character from bottom up
        # 1. Legs
        self._create_legs(char_node)

        # 2. Torso
        self._create_torso(char_node)

        # 3. Arms
        self._create_arms(char_node)

        # 4. Head and neck
        self._create_head(char_node)

        # 5. Accessories
        if self.has_bag:
            self._create_bag(char_node)
        if self.has_hat:
            self._create_hat(char_node)
        if self.has_glasses:
            self._create_glasses(char_node)

        return char_node

    def _create_legs(self, parent: NodePath):
        """Create legs with walking animation"""
        card_maker = CardMaker("leg")

        # Walking animation - swing legs
        left_swing = np.sin(self.walk_cycle * np.pi * 2) * 15  # degrees
        right_swing = -left_swing

        # Left leg
        # Upper leg
        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, self.upper_leg_length)
        left_upper = parent.attachNewNode(card_maker.generate())
        left_upper.setPos(-self.waist_width/4, 0, 0)
        left_upper.setP(left_swing)
        left_upper.setColor(self.pants_color)

        # Lower leg
        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, self.lower_leg_length)
        left_lower = left_upper.attachNewNode(card_maker.generate())
        left_lower.setZ(self.upper_leg_length)
        left_lower.setP(-abs(left_swing) * 0.5)  # Knee bends
        left_lower.setColor(self.pants_color)

        # Foot
        shoe_color = (0.12, 0.12, 0.15, 1.0)  # Black shoes
        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, 0.25)
        left_foot = left_lower.attachNewNode(card_maker.generate())
        left_foot.setZ(self.lower_leg_length)
        left_foot.setP(-90)
        left_foot.setColor(shoe_color)

        # Right leg (mirror of left)
        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, self.upper_leg_length)
        right_upper = parent.attachNewNode(card_maker.generate())
        right_upper.setPos(self.waist_width/4, 0, 0)
        right_upper.setP(right_swing)
        right_upper.setColor(self.pants_color)

        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, self.lower_leg_length)
        right_lower = right_upper.attachNewNode(card_maker.generate())
        right_lower.setZ(self.upper_leg_length)
        right_lower.setP(-abs(right_swing) * 0.5)
        right_lower.setColor(self.pants_color)

        card_maker.setFrame(-self.leg_thickness/2, self.leg_thickness/2,
                           0, 0.25)
        right_foot = right_lower.attachNewNode(card_maker.generate())
        right_foot.setZ(self.lower_leg_length)
        right_foot.setP(-90)
        right_foot.setColor(shoe_color)

    def _create_torso(self, parent: NodePath):
        """Create torso"""
        card_maker = CardMaker("torso")
        torso_z = self.leg_length

        # Main torso body
        card_maker.setFrame(-self.shoulder_width/2, self.shoulder_width/2,
                           0, self.torso_height)

        # Front
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -self.shoulder_width/4, torso_z)
        front.setColor(self.shirt_color)

        # Back
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, self.shoulder_width/4, torso_z)
        back.setH(180)
        back.setColor(self.shirt_color)

        # Sides
        card_maker.setFrame(-self.shoulder_width/4, self.shoulder_width/4,
                           0, self.torso_height)

        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-self.shoulder_width/2, 0, torso_z)
        left.setH(90)
        left.setColor(self.shirt_color)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(self.shoulder_width/2, 0, torso_z)
        right.setH(-90)
        right.setColor(self.shirt_color)

    def _create_arms(self, parent: NodePath):
        """Create arms with walking animation"""
        card_maker = CardMaker("arm")
        shoulder_z = self.leg_length + self.torso_height * 0.85

        # Arms swing opposite to legs
        left_arm_swing = -np.sin(self.walk_cycle * np.pi * 2) * 25
        right_arm_swing = -left_arm_swing

        # Left arm
        # Upper arm
        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -self.upper_arm_length, 0)
        left_upper = parent.attachNewNode(card_maker.generate())
        left_upper.setPos(-self.shoulder_width/2 - self.arm_thickness/2, 0, shoulder_z)
        left_upper.setP(-left_arm_swing)
        left_upper.setColor(self.shirt_color)

        # Forearm
        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -self.forearm_length, 0)
        left_forearm = left_upper.attachNewNode(card_maker.generate())
        left_forearm.setZ(-self.upper_arm_length)
        left_forearm.setColor(self.skin_tone)  # Exposed forearm

        # Hand
        hand_color = self.skin_tone
        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -0.12, 0)
        left_hand = left_forearm.attachNewNode(card_maker.generate())
        left_hand.setZ(-self.forearm_length)
        left_hand.setColor(hand_color)

        # Right arm
        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -self.upper_arm_length, 0)
        right_upper = parent.attachNewNode(card_maker.generate())
        right_upper.setPos(self.shoulder_width/2 + self.arm_thickness/2, 0, shoulder_z)
        right_upper.setP(-right_arm_swing)
        right_upper.setColor(self.shirt_color)

        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -self.forearm_length, 0)
        right_forearm = right_upper.attachNewNode(card_maker.generate())
        right_forearm.setZ(-self.upper_arm_length)
        right_forearm.setColor(self.skin_tone)

        card_maker.setFrame(-self.arm_thickness/2, self.arm_thickness/2,
                           -0.12, 0)
        right_hand = right_forearm.attachNewNode(card_maker.generate())
        right_hand.setZ(-self.forearm_length)
        right_hand.setColor(hand_color)

    def _create_head(self, parent: NodePath):
        """Create head and neck"""
        card_maker = CardMaker("head")
        neck_z = self.leg_length + self.torso_height

        # Neck
        card_maker.setFrame(-self.neck_height/2, self.neck_height/2,
                           0, self.neck_height)
        neck = parent.attachNewNode(card_maker.generate())
        neck.setZ(neck_z)
        neck.setColor(self.skin_tone)

        # Head (simplified as box)
        head_z = neck_z + self.neck_height

        # Front face
        card_maker.setFrame(-self.head_width/2, self.head_width/2,
                           0, self.head_height)
        face = parent.attachNewNode(card_maker.generate())
        face.setPos(0, -self.head_width/2, head_z)
        face.setColor(self.skin_tone)

        # Back of head
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, self.head_width/2, head_z)
        back.setH(180)
        back.setColor(self.skin_tone)

        # Sides
        card_maker.setFrame(-self.head_width/2, self.head_width/2,
                           0, self.head_height)

        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-self.head_width/2, 0, head_z)
        left.setH(90)
        left.setColor(self.skin_tone)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(self.head_width/2, 0, head_z)
        right.setH(-90)
        right.setColor(self.skin_tone)

        # Top of head (hair)
        card_maker.setFrame(-self.head_width/2, self.head_width/2,
                           -self.head_width/2, self.head_width/2)
        top = parent.attachNewNode(card_maker.generate())
        top.setZ(head_z + self.head_height)
        top.setP(-90)
        top.setColor(self.hair_color)

    def _create_bag(self, parent: NodePath):
        """Create bag/briefcase/backpack"""
        card_maker = CardMaker("bag")

        if self.character_type == CharacterType.BUSINESS_PERSON:
            # Briefcase (in hand)
            bag_color = (0.15, 0.12, 0.10, 1.0)  # Dark brown
            bag_size = 0.35
            bag_z = self.leg_length + self.torso_height * 0.5

            card_maker.setFrame(-bag_size/2, bag_size/2, -bag_size, 0)
            bag = parent.attachNewNode(card_maker.generate())
            bag.setPos(self.shoulder_width/2 + 0.15, 0, bag_z)
            bag.setColor(bag_color)

        elif self.character_type == CharacterType.STUDENT:
            # Backpack (on back)
            bag_color = (0.25, 0.35, 0.65, 1.0)  # Blue
            bag_width = self.shoulder_width * 0.7
            bag_height = self.torso_height * 0.6
            bag_z = self.leg_length + self.torso_height * 0.3

            card_maker.setFrame(-bag_width/2, bag_width/2, 0, bag_height)
            bag = parent.attachNewNode(card_maker.generate())
            bag.setPos(0, self.shoulder_width/4 + 0.15, bag_z)
            bag.setH(180)
            bag.setColor(bag_color)

        else:
            # Shoulder bag
            bag_color = (0.55, 0.45, 0.35, 1.0)  # Brown
            bag_size = 0.30
            bag_z = self.leg_length + self.torso_height * 0.4

            card_maker.setFrame(-bag_size, bag_size, -bag_size/2, bag_size/2)
            bag = parent.attachNewNode(card_maker.generate())
            bag.setPos(-self.shoulder_width/2 - 0.1, 0, bag_z)
            bag.setH(90)
            bag.setColor(bag_color)

    def _create_hat(self, parent: NodePath):
        """Create hat"""
        card_maker = CardMaker("hat")
        hat_z = self.leg_length + self.torso_height + self.neck_height + self.head_height

        if self.character_type == CharacterType.WORKER:
            # Hard hat
            hat_color = (0.95, 0.75, 0.15, 1.0)  # Yellow
            hat_height = 0.15

            card_maker.setFrame(-self.head_width/2, self.head_width/2,
                               -self.head_width/2, self.head_width/2)
            hat_top = parent.attachNewNode(card_maker.generate())
            hat_top.setZ(hat_z + hat_height)
            hat_top.setP(-90)
            hat_top.setColor(hat_color)

            # Brim
            card_maker.setFrame(-self.head_width/2 - 0.08, self.head_width/2 + 0.08,
                               -self.head_width/2 - 0.08, self.head_width/2 + 0.08)
            brim = parent.attachNewNode(card_maker.generate())
            brim.setZ(hat_z + 0.02)
            brim.setP(-90)
            brim.setColor(hat_color)

        else:
            # Regular hat/cap
            hat_color = self._random_choice([
                (0.12, 0.12, 0.15, 1.0),   # Black
                (0.25, 0.35, 0.55, 1.0),   # Blue
                (0.55, 0.45, 0.35, 1.0),   # Brown
            ])
            hat_height = 0.12

            card_maker.setFrame(-self.head_width/2, self.head_width/2,
                               -self.head_width/2, self.head_width/2)
            hat = parent.attachNewNode(card_maker.generate())
            hat.setZ(hat_z + hat_height)
            hat.setP(-90)
            hat.setColor(hat_color)

    def _create_glasses(self, parent: NodePath):
        """Create glasses"""
        card_maker = CardMaker("glasses")
        glasses_z = self.leg_length + self.torso_height + self.neck_height + self.head_height * 0.65
        glasses_color = (0.15, 0.15, 0.15, 1.0)  # Black frames

        lens_size = 0.06

        # Left lens
        card_maker.setFrame(-lens_size, lens_size, -lens_size/1.5, lens_size/1.5)
        left_lens = parent.attachNewNode(card_maker.generate())
        left_lens.setPos(-self.head_width/4, -self.head_width/2 - 0.02, glasses_z)
        left_lens.setColor(glasses_color)

        # Right lens
        right_lens = parent.attachNewNode(card_maker.generate())
        right_lens.setPos(self.head_width/4, -self.head_width/2 - 0.02, glasses_z)
        right_lens.setColor(glasses_color)

        # Bridge
        card_maker.setFrame(-self.head_width/8, self.head_width/8, -0.01, 0.01)
        bridge = parent.attachNewNode(card_maker.generate())
        bridge.setPos(0, -self.head_width/2 - 0.02, glasses_z)
        bridge.setColor(glasses_color)

    def get_specs(self) -> Dict:
        """Get character specifications"""
        return {
            'type': self.character_type.name,
            'gender': self.gender.name,
            'height': self.height,
            'has_bag': self.has_bag,
            'has_hat': self.has_hat,
            'has_glasses': self.has_glasses,
        }


if __name__ == "__main__":
    """Test detailed character system"""
    print("Detailed Character System Test")
    print("=" * 70)

    for char_type in CharacterType:
        char = DetailedCharacter(char_type, seed=42 + char_type.value)
        specs = char.get_specs()

        print(f"\n{char_type.name}:")
        print(f"  Gender: {specs['gender']}")
        print(f"  Height: {specs['height']:.2f}m")
        print(f"  Accessories: Bag={specs['has_bag']}, "
              f"Hat={specs['has_hat']}, Glasses={specs['has_glasses']}")

    print("\n" + "=" * 70)
    print("Detailed characters with realistic proportions and clothing!")
