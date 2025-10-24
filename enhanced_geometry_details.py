"""
Enhanced Geometry Details - GTA 5 Level Precision
Adds intricate details to buildings, vehicles, and environmental objects

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from typing import Tuple, List


class BuildingDetailEnhancer:
    """
    Adds ultra-detailed features to buildings.

    Enhancements:
    - Window shutters and blinds
    - Detailed AC units with vents and fans
    - Satellite dishes
    - Rooftop antennas with guy-wires
    - Drain pipes and gutters
    - Window sills with planters
    - Fire escape handrails
    - Building damage (cracks, wear)
    - Graffiti decals
    - Security cameras
    """

    @staticmethod
    def add_window_shutters(parent: NodePath, window_pos: Tuple[float, float, float],
                           window_size: Tuple[float, float], color: Tuple[float, float, float, float]):
        """Add detailed window shutters"""
        card = CardMaker("shutter")
        x, y, z = window_pos
        w, h = window_size

        shutter_width = w * 0.55
        shutter_offset = w * 0.60

        # Left shutter
        card.setFrame(-shutter_width/2, shutter_width/2, 0, h)
        left_shutter = parent.attachNewNode(card.generate())
        left_shutter.setPos(x - shutter_offset, y - 0.02, z)
        left_shutter.setP(-90)
        left_shutter.setColor(*color)

        # Add slats (horizontal lines)
        for i in range(5):
            slat_y = h * (i / 5.0 + 0.1)
            slat = CardMaker(f"slat_{i}")
            slat.setFrame(-shutter_width/2, shutter_width/2, 0, 0.02)
            slat_node = left_shutter.attachNewNode(slat.generate())
            slat_node.setPos(0, 0, slat_y)
            slat_node.setColor(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8, 1.0)

        # Right shutter (mirror)
        card.setFrame(-shutter_width/2, shutter_width/2, 0, h)
        right_shutter = parent.attachNewNode(card.generate())
        right_shutter.setPos(x + shutter_offset, y - 0.02, z)
        right_shutter.setP(-90)
        right_shutter.setColor(*color)

        # Add slats to right shutter
        for i in range(5):
            slat_y = h * (i / 5.0 + 0.1)
            slat = CardMaker(f"slat_{i}")
            slat.setFrame(-shutter_width/2, shutter_width/2, 0, 0.02)
            slat_node = right_shutter.attachNewNode(slat.generate())
            slat_node.setPos(0, 0, slat_y)
            slat_node.setColor(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8, 1.0)

    @staticmethod
    def add_detailed_ac_unit(parent: NodePath, position: Tuple[float, float, float],
                            heading: float = 0):
        """Add detailed rooftop AC unit"""
        x, y, z = position

        # Main AC body
        card = CardMaker("ac_body")
        card.setFrame(-1.2, 1.2, 0, 0.8)
        ac_body = parent.attachNewNode(card.generate())
        ac_body.setPos(x, y, z)
        ac_body.setP(-90)
        ac_body.setH(heading)
        ac_body.setColor(0.75, 0.75, 0.78, 1.0)

        # Vents (front grille)
        for i in range(8):
            vent = CardMaker(f"vent_{i}")
            vent_y = 0.1 * i + 0.05
            vent.setFrame(-1.0, 1.0, 0, 0.02)
            vent_node = ac_body.attachNewNode(vent.generate())
            vent_node.setPos(0, 0, vent_y)
            vent_node.setColor(0.25, 0.25, 0.28, 1.0)

        # Fan housing (cylindrical section)
        fan_housing = CardMaker("fan_housing")
        fan_housing.setFrame(-0.4, 0.4, 0, 0.4)
        fan_node = ac_body.attachNewNode(fan_housing.generate())
        fan_node.setPos(0, -0.15, 0.4)
        fan_node.setP(-90)
        fan_node.setColor(0.20, 0.20, 0.22, 1.0)

        # Support legs
        for offset in [(-0.9, -0.9), (0.9, -0.9), (-0.9, 0.9), (0.9, 0.9)]:
            leg = CardMaker("leg")
            leg.setFrame(-0.05, 0.05, -0.3, 0)
            leg_node = parent.attachNewNode(leg.generate())
            leg_node.setPos(x + offset[0], y + offset[1], z)
            leg_node.setP(-90)
            leg_node.setColor(0.45, 0.45, 0.48, 1.0)

    @staticmethod
    def add_satellite_dish(parent: NodePath, position: Tuple[float, float, float],
                          heading: float = 45):
        """Add satellite dish"""
        x, y, z = position

        # Dish mounting pole
        pole = CardMaker("dish_pole")
        pole.setFrame(-0.05, 0.05, 0, 1.5)
        pole_node = parent.attachNewNode(pole.generate())
        pole_node.setPos(x, y, z)
        pole_node.setColor(0.50, 0.50, 0.52, 1.0)

        # Dish (circular approximation with card)
        dish = CardMaker("dish")
        dish_radius = 0.6
        dish.setFrame(-dish_radius, dish_radius, -dish_radius, dish_radius)
        dish_node = pole_node.attachNewNode(dish.generate())
        dish_node.setPos(0, 0, 1.2)
        dish_node.setP(45)  # Angled up
        dish_node.setH(heading)
        dish_node.setColor(0.88, 0.88, 0.90, 1.0)

        # LNB (feed horn)
        lnb = CardMaker("lnb")
        lnb.setFrame(-0.08, 0.08, 0, 0.3)
        lnb_node = dish_node.attachNewNode(lnb.generate())
        lnb_node.setPos(0, 0.4, 0)
        lnb_node.setP(-45)
        lnb_node.setColor(0.25, 0.25, 0.28, 1.0)

    @staticmethod
    def add_antenna_array(parent: NodePath, position: Tuple[float, float, float]):
        """Add communication antenna array"""
        x, y, z = position

        # Main tower
        tower = CardMaker("antenna_tower")
        tower.setFrame(-0.15, 0.15, 0, 4.0)
        tower_node = parent.attachNewNode(tower.generate())
        tower_node.setPos(x, y, z)
        tower_node.setColor(0.75, 0.25, 0.20, 1.0)  # Red/white tower

        # Crossbars
        for height in [1.0, 2.0, 3.0]:
            crossbar = CardMaker(f"crossbar_{height}")
            crossbar.setFrame(-0.8, 0.8, -0.05, 0.05)
            cross_node = tower_node.attachNewNode(crossbar.generate())
            cross_node.setPos(0, 0, height)
            cross_node.setP(-90)
            cross_node.setColor(0.85, 0.85, 0.88, 1.0)

            # Antennas on crossbar
            for antenna_pos in [-0.6, -0.2, 0.2, 0.6]:
                antenna = CardMaker("antenna")
                antenna.setFrame(-0.02, 0.02, 0, 0.4)
                ant_node = cross_node.attachNewNode(antenna.generate())
                ant_node.setPos(antenna_pos, 0, 0)
                ant_node.setColor(0.60, 0.60, 0.62, 1.0)

        # Blinking light on top
        light_top = CardMaker("warning_light")
        light_top.setFrame(-0.1, 0.1, -0.1, 0.1)
        light_node = tower_node.attachNewNode(light_top.generate())
        light_node.setPos(0, 0, 4.2)
        light_node.setP(-90)
        light_node.setColor(1.0, 0.1, 0.1, 1.0)

    @staticmethod
    def add_drain_pipes(parent: NodePath, building_height: float,
                       pipe_positions: List[Tuple[float, float]]):
        """Add building drain pipes"""
        for x, y in pipe_positions:
            # Main vertical pipe
            pipe = CardMaker("drain_pipe")
            pipe.setFrame(-0.08, 0.08, 0, building_height)
            pipe_node = parent.attachNewNode(pipe.generate())
            pipe_node.setPos(x, y, 0)
            pipe_node.setColor(0.45, 0.45, 0.48, 1.0)

            # Pipe brackets every few meters
            for bracket_z in np.arange(2.0, building_height, 3.0):
                bracket = CardMaker("bracket")
                bracket.setFrame(-0.12, 0.12, -0.05, 0.05)
                bracket_node = pipe_node.attachNewNode(bracket.generate())
                bracket_node.setPos(0, -0.05, bracket_z)
                bracket_node.setP(-90)
                bracket_node.setColor(0.35, 0.35, 0.38, 1.0)

    @staticmethod
    def add_window_planter(parent: NodePath, window_pos: Tuple[float, float, float],
                          window_width: float):
        """Add window planter box with flowers"""
        x, y, z = window_pos

        # Planter box
        planter = CardMaker("planter")
        planter_width = window_width * 0.9
        planter.setFrame(-planter_width/2, planter_width/2, 0, 0.25)
        planter_node = parent.attachNewNode(planter.generate())
        planter_node.setPos(x, y - 0.05, z - 0.15)
        planter_node.setP(-90)
        planter_node.setColor(0.45, 0.30, 0.25, 1.0)  # Brown/terracotta

        # Add simple flowers (colored squares)
        for i in range(4):
            flower_x = (i - 1.5) * (planter_width / 5)
            flower = CardMaker(f"flower_{i}")
            flower.setFrame(-0.05, 0.05, 0, 0.15)
            flower_node = planter_node.attachNewNode(flower.generate())
            flower_node.setPos(flower_x, 0, 0.10)
            # Random flower colors
            colors = [(1.0, 0.2, 0.2, 1.0), (1.0, 0.8, 0.2, 1.0),
                     (0.8, 0.2, 1.0, 1.0), (1.0, 0.4, 0.6, 1.0)]
            flower_node.setColor(*colors[i % len(colors)])


class VehicleDetailEnhancer:
    """
    Adds ultra-detailed features to vehicles.

    Enhancements:
    - Door handles with keyholes
    - Side mirrors with adjustment details
    - Windshield wipers with arms
    - Gas cap
    - License plate with text
    - Tire treads
    - Brake calipers visible through rims
    - Exhaust tips
    - Antenna
    - Badges and emblems
    """

    @staticmethod
    def add_door_handle(parent: NodePath, position: Tuple[float, float, float],
                       facing: str = "left"):
        """Add detailed door handle"""
        x, y, z = position

        # Handle base
        handle_base = CardMaker("handle_base")
        handle_base.setFrame(-0.08, 0.08, 0, 0.03)
        handle_node = parent.attachNewNode(handle_base.generate())
        handle_node.setPos(x, y, z)
        handle_node.setP(-90)
        handle_node.setColor(0.20, 0.20, 0.22, 1.0)

        # Handle grip
        grip = CardMaker("handle_grip")
        grip.setFrame(-0.05, 0.05, 0, 0.15)
        grip_node = handle_node.attachNewNode(grip.generate())
        grip_node.setPos(0, 0.05, 0)
        grip_node.setColor(0.25, 0.25, 0.28, 1.0)

        # Keyhole
        keyhole = CardMaker("keyhole")
        keyhole.setFrame(-0.01, 0.01, -0.01, 0.01)
        keyhole_node = handle_node.attachNewNode(keyhole.generate())
        keyhole_node.setPos(0, 0, -0.05)
        keyhole_node.setColor(0.05, 0.05, 0.08, 1.0)

    @staticmethod
    def add_detailed_side_mirror(parent: NodePath, position: Tuple[float, float, float],
                                side: str = "left"):
        """Add highly detailed side mirror"""
        x, y, z = position

        # Mirror mount arm
        arm = CardMaker("mirror_arm")
        arm.setFrame(-0.03, 0.03, 0, 0.15)
        arm_node = parent.attachNewNode(arm.generate())
        arm_node.setPos(x, y, z)
        arm_node.setH(45 if side == "left" else -45)
        arm_node.setP(-90)
        arm_node.setColor(0.20, 0.20, 0.22, 1.0)

        # Mirror housing
        housing = CardMaker("mirror_housing")
        housing.setFrame(-0.15, 0.15, -0.10, 0.10)
        housing_node = arm_node.attachNewNode(housing.generate())
        housing_node.setPos(0, 0.15, 0)
        housing_node.setColor(0.25, 0.25, 0.28, 1.0)

        # Mirror glass (reflective)
        glass = CardMaker("mirror_glass")
        glass.setFrame(-0.12, 0.12, -0.08, 0.08)
        glass_node = housing_node.attachNewNode(glass.generate())
        glass_node.setPos(0, 0.02, 0)
        glass_node.setColor(0.70, 0.75, 0.80, 1.0)  # Slightly blue reflective

        # Turn signal indicator (LED)
        led = CardMaker("turn_signal")
        led.setFrame(-0.03, 0.03, -0.02, 0.02)
        led_node = housing_node.attachNewNode(led.generate())
        led_node.setPos(0, -0.08, 0)
        led_node.setColor(1.0, 0.6, 0.1, 1.0)  # Amber

    @staticmethod
    def add_windshield_wiper(parent: NodePath, position: Tuple[float, float, float],
                            length: float = 0.8):
        """Add windshield wiper with arm"""
        x, y, z = position

        # Wiper arm (metal)
        arm = CardMaker("wiper_arm")
        arm.setFrame(-0.02, 0.02, 0, length)
        arm_node = parent.attachNewNode(arm.generate())
        arm_node.setPos(x, y, z)
        arm_node.setH(15)  # Slight angle
        arm_node.setColor(0.20, 0.20, 0.22, 1.0)

        # Rubber blade
        blade = CardMaker("wiper_blade")
        blade.setFrame(-0.01, 0.01, 0, length * 0.9)
        blade_node = arm_node.attachNewNode(blade.generate())
        blade_node.setPos(0, 0, length * 0.05)
        blade_node.setColor(0.10, 0.10, 0.12, 1.0)

    @staticmethod
    def add_license_plate(parent: NodePath, position: Tuple[float, float, float],
                         plate_number: str = "PANDA3D"):
        """Add license plate with text"""
        x, y, z = position

        # Plate background
        plate = CardMaker("license_plate")
        plate.setFrame(-0.25, 0.25, -0.10, 0.10)
        plate_node = parent.attachNewNode(plate.generate())
        plate_node.setPos(x, y, z)
        plate_node.setP(-90)
        plate_node.setColor(1.0, 1.0, 1.0, 1.0)  # White plate

        # Plate border
        border = CardMaker("plate_border")
        border.setFrame(-0.26, 0.26, -0.11, 0.11)
        border_node = parent.attachNewNode(border.generate())
        border_node.setPos(x, y - 0.01, z)
        border_node.setP(-90)
        border_node.setColor(0.15, 0.15, 0.18, 1.0)  # Black border

        # Note: Actual text would require TextNode
        # For now, adding colored strips to represent text area
        text_area = CardMaker("text_area")
        text_area.setFrame(-0.20, 0.20, -0.06, 0.06)
        text_node = plate_node.attachNewNode(text_area.generate())
        text_node.setPos(0, 0.01, 0)
        text_node.setColor(0.10, 0.10, 0.12, 1.0)

    @staticmethod
    def add_tire_tread(parent: NodePath, wheel_pos: Tuple[float, float, float],
                      wheel_radius: float):
        """Add tire tread detail"""
        # Tread pattern is added to tire surface
        x, y, z = wheel_pos

        # Create tread grooves (simplified as lines)
        for i in range(12):
            angle = (i / 12.0) * 360
            tread = CardMaker(f"tread_{i}")
            tread.setFrame(-0.01, 0.01, 0, wheel_radius * 0.2)
            tread_node = parent.attachNewNode(tread.generate())
            tread_node.setPos(x, y, z)
            tread_node.setH(angle)
            tread_node.setColor(0.08, 0.08, 0.10, 1.0)

    @staticmethod
    def add_exhaust_tip(parent: NodePath, position: Tuple[float, float, float],
                       diameter: float = 0.08):
        """Add detailed exhaust pipe tip"""
        x, y, z = position

        # Outer pipe
        outer_pipe = CardMaker("exhaust_outer")
        outer_pipe.setFrame(-diameter, diameter, -diameter, diameter)
        outer_node = parent.attachNewNode(outer_pipe.generate())
        outer_node.setPos(x, y, z)
        outer_node.setP(-90)
        outer_node.setColor(0.35, 0.35, 0.38, 1.0)  # Chrome-ish

        # Inner pipe (darker)
        inner_pipe = CardMaker("exhaust_inner")
        inner_diameter = diameter * 0.7
        inner_pipe.setFrame(-inner_diameter, inner_diameter, -inner_diameter, inner_diameter)
        inner_node = outer_node.attachNewNode(inner_pipe.generate())
        inner_node.setPos(0, 0.02, 0)
        inner_node.setColor(0.10, 0.10, 0.12, 1.0)  # Dark/sooty interior

        # Soot/carbon buildup around tip
        soot = CardMaker("exhaust_soot")
        soot.setFrame(-diameter*1.2, diameter*1.2, -diameter*1.2, diameter*1.2)
        soot_node = outer_node.attachNewNode(soot.generate())
        soot_node.setPos(0, 0.01, 0)
        soot_node.setColor(0.08, 0.08, 0.10, 0.5)  # Semi-transparent dark


class EnvironmentalDetailEnhancer:
    """
    Adds ultra-detailed features to environmental props.

    Enhancements:
    - Street sign posts with reflective coating
    - Trash with overflow
    - Park benches with weathering
    - Detailed fire hydrants with chains
    - Mailbox slot and collection times
    - Traffic light wiring and sensors
    """

    @staticmethod
    def add_detailed_street_sign(parent: NodePath, position: Tuple[float, float, float],
                                sign_text: str = "MAIN ST"):
        """Add detailed street sign with post"""
        x, y, z = position

        # Sign post
        post = CardMaker("sign_post")
        post.setFrame(-0.05, 0.05, 0, 3.0)
        post_node = parent.attachNewNode(post.generate())
        post_node.setPos(x, y, z)
        post_node.setColor(0.50, 0.50, 0.52, 1.0)

        # Sign board (green background typical for street signs)
        sign_board = CardMaker("sign_board")
        sign_board.setFrame(-0.6, 0.6, -0.15, 0.15)
        board_node = post_node.attachNewNode(sign_board.generate())
        board_node.setPos(0, 0, 2.5)
        board_node.setP(-90)
        board_node.setColor(0.15, 0.55, 0.25, 1.0)  # Green

        # Reflective border
        border = CardMaker("sign_border")
        border.setFrame(-0.62, 0.62, -0.17, 0.17)
        border_node = post_node.attachNewNode(border.generate())
        border_node.setPos(0, -0.01, 2.5)
        border_node.setP(-90)
        border_node.setColor(0.95, 0.95, 0.98, 1.0)  # Reflective white

        # Mounting brackets
        for bracket_z in [2.35, 2.65]:
            bracket = CardMaker("bracket")
            bracket.setFrame(-0.08, 0.08, -0.03, 0.03)
            bracket_node = post_node.attachNewNode(bracket.generate())
            bracket_node.setPos(0, 0, bracket_z)
            bracket_node.setP(-90)
            bracket_node.setColor(0.25, 0.25, 0.28, 1.0)

    @staticmethod
    def add_overflowing_trash_can(parent: NodePath, position: Tuple[float, float, float]):
        """Add trash can with overflow (urban detail)"""
        x, y, z = position

        # Main can body (cylindrical)
        can = CardMaker("trash_can")
        can.setFrame(-0.3, 0.3, 0, 0.8)
        can_node = parent.attachNewNode(can.generate())
        can_node.setPos(x, y, z)
        can_node.setP(-90)
        can_node.setColor(0.25, 0.50, 0.25, 1.0)  # Dark green

        # Lid (slightly open)
        lid = CardMaker("trash_lid")
        lid.setFrame(-0.32, 0.32, -0.32, 0.32)
        lid_node = can_node.attachNewNode(lid.generate())
        lid_node.setPos(0, 0, 0.82)
        lid_node.setH(15)  # Tilted open
        lid_node.setColor(0.20, 0.45, 0.20, 1.0)

        # Overflow trash (crumpled paper)
        for i in range(3):
            trash = CardMaker(f"trash_{i}")
            size = np.random.uniform(0.08, 0.15)
            trash.setFrame(-size, size, -size, size)
            trash_node = can_node.attachNewNode(trash.generate())
            offset_x = np.random.uniform(-0.2, 0.2)
            offset_y = np.random.uniform(-0.2, 0.2)
            trash_node.setPos(offset_x, offset_y, 0.75 + i * 0.1)
            # Random trash colors (white paper, brown bags, etc.)
            colors = [(0.95, 0.95, 0.98, 1.0), (0.65, 0.55, 0.45, 1.0), (0.85, 0.85, 0.88, 1.0)]
            trash_node.setColor(*colors[i % 3])
            trash_node.setH(np.random.uniform(0, 360))

    @staticmethod
    def add_detailed_fire_hydrant(parent: NodePath, position: Tuple[float, float, float]):
        """Add detailed fire hydrant with chain"""
        x, y, z = position

        # Main body
        body = CardMaker("hydrant_body")
        body.setFrame(-0.15, 0.15, 0, 0.6)
        body_node = parent.attachNewNode(body.generate())
        body_node.setPos(x, y, z)
        body_node.setP(-90)
        body_node.setColor(0.85, 0.20, 0.15, 1.0)  # Fire engine red

        # Top cap
        cap = CardMaker("hydrant_cap")
        cap.setFrame(-0.12, 0.12, -0.12, 0.12)
        cap_node = body_node.attachNewNode(cap.generate())
        cap_node.setPos(0, 0, 0.65)
        cap_node.setColor(0.75, 0.18, 0.13, 1.0)

        # Side nozzles (2)
        for side in [-1, 1]:
            nozzle = CardMaker(f"nozzle_{side}")
            nozzle.setFrame(-0.06, 0.06, 0, 0.15)
            nozzle_node = body_node.attachNewNode(nozzle.generate())
            nozzle_node.setPos(side * 0.15, 0, 0.35)
            nozzle_node.setH(side * 90)
            nozzle_node.setP(-90)
            nozzle_node.setColor(0.20, 0.20, 0.22, 1.0)  # Metal nozzle

            # Nozzle cap with chain
            cap_nozzle = CardMaker(f"nozzle_cap_{side}")
            cap_nozzle.setFrame(-0.07, 0.07, -0.07, 0.07)
            cap_nozzle_node = nozzle_node.attachNewNode(cap_nozzle.generate())
            cap_nozzle_node.setPos(0, 0, 0.16)
            cap_nozzle_node.setColor(0.75, 0.65, 0.20, 1.0)  # Brass

            # Chain link (simplified)
            chain = CardMaker(f"chain_{side}")
            chain.setFrame(-0.02, 0.02, 0, 0.12)
            chain_node = cap_nozzle_node.attachNewNode(chain.generate())
            chain_node.setPos(0, 0.08, -0.08)
            chain_node.setP(-45)
            chain_node.setColor(0.60, 0.60, 0.62, 1.0)

        # Base pentagonal nuts (realistic hydrant feature)
        for nut_z in [0.15, 0.45]:
            nut = CardMaker(f"nut_{nut_z}")
            nut.setFrame(-0.18, 0.18, -0.05, 0.05)
            nut_node = body_node.attachNewNode(nut.generate())
            nut_node.setPos(0, 0, nut_z)
            nut_node.setP(-90)
            nut_node.setColor(0.20, 0.20, 0.22, 1.0)
