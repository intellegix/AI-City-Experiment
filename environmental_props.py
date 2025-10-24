"""
Environmental Props System - City Details
Creates street furniture, vegetation, and urban details

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from typing import Tuple, List
from enum import Enum


class PropType(Enum):
    """Types of environmental props"""
    STREET_LIGHT = 0
    TRAFFIC_LIGHT = 1
    BENCH = 2
    TRASH_CAN = 3
    MAILBOX = 4
    FIRE_HYDRANT = 5
    BUS_STOP = 6
    TREE = 7
    STREET_SIGN = 8
    PARKING_METER = 9
    BIKE_RACK = 10
    NEWSPAPER_BOX = 11


class EnvironmentalProp:
    """
    Environmental prop generator for city details.

    Creates realistic urban furniture and vegetation:
    - Street lights (modern LED and classic)
    - Traffic lights (with lights and poles)
    - Benches (park and bus stop benches)
    - Trash cans (various styles)
    - Mailboxes (USPS style)
    - Fire hydrants
    - Bus stops with shelters
    - Trees (various types)
    - Street signs
    - Parking meters
    - Bike racks
    - Newspaper boxes
    """

    def __init__(self, prop_type: PropType, seed: int = None):
        """Initialize prop generator"""
        self.prop_type = prop_type
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float],
                       heading: float = 0) -> NodePath:
        """Create prop 3D model"""
        prop_node = parent_node.attachNewNode(f"prop_{self.prop_type.name}_{self.seed}")
        prop_node.setPos(*position)
        prop_node.setH(heading)

        # Create appropriate prop
        if self.prop_type == PropType.STREET_LIGHT:
            self._create_street_light(prop_node)
        elif self.prop_type == PropType.TRAFFIC_LIGHT:
            self._create_traffic_light(prop_node)
        elif self.prop_type == PropType.BENCH:
            self._create_bench(prop_node)
        elif self.prop_type == PropType.TRASH_CAN:
            self._create_trash_can(prop_node)
        elif self.prop_type == PropType.MAILBOX:
            self._create_mailbox(prop_node)
        elif self.prop_type == PropType.FIRE_HYDRANT:
            self._create_fire_hydrant(prop_node)
        elif self.prop_type == PropType.BUS_STOP:
            self._create_bus_stop(prop_node)
        elif self.prop_type == PropType.TREE:
            self._create_tree(prop_node)
        elif self.prop_type == PropType.STREET_SIGN:
            self._create_street_sign(prop_node)
        elif self.prop_type == PropType.PARKING_METER:
            self._create_parking_meter(prop_node)
        elif self.prop_type == PropType.BIKE_RACK:
            self._create_bike_rack(prop_node)
        elif self.prop_type == PropType.NEWSPAPER_BOX:
            self._create_newspaper_box(prop_node)

        return prop_node

    def _create_street_light(self, parent: NodePath):
        """Create street light pole with lamp"""
        card_maker = CardMaker("street_light")

        # Pole (metal gray)
        pole_color = (0.35, 0.35, 0.38, 1.0)
        pole_height = 6.0
        pole_width = 0.15

        card_maker.setFrame(-pole_width/2, pole_width/2, 0, pole_height)
        pole = parent.attachNewNode(card_maker.generate())
        pole.setColor(pole_color)

        # Horizontal arm extending out
        arm_length = 1.2
        card_maker.setFrame(0, arm_length, -pole_width/2, pole_width/2)
        arm = parent.attachNewNode(card_maker.generate())
        arm.setPos(0, 0, pole_height - 0.3)
        arm.setH(90)
        arm.setColor(pole_color)

        # Lamp head (modern LED)
        lamp_color = (0.95, 0.95, 0.88, 1.0)  # Warm white when lit
        lamp_size = 0.4

        card_maker.setFrame(-lamp_size/2, lamp_size/2, -lamp_size/2, 0)
        lamp = parent.attachNewNode(card_maker.generate())
        lamp.setPos(arm_length - 0.2, 0, pole_height - 0.3)
        lamp.setColor(lamp_color)

        # Lamp housing (dark)
        housing_color = (0.15, 0.15, 0.18, 1.0)
        card_maker.setFrame(-lamp_size/2 - 0.05, lamp_size/2 + 0.05,
                           -lamp_size, -lamp_size/2)
        housing = parent.attachNewNode(card_maker.generate())
        housing.setPos(arm_length - 0.2, 0, pole_height - 0.3)
        housing.setColor(housing_color)

        # Base
        base_size = 0.5
        card_maker.setFrame(-base_size/2, base_size/2, -base_size/2, base_size/2)
        base = parent.attachNewNode(card_maker.generate())
        base.setZ(0.1)
        base.setP(-90)
        base.setColor(pole_color)

    def _create_traffic_light(self, parent: NodePath):
        """Create traffic light with colored lights"""
        card_maker = CardMaker("traffic_light")

        # Pole
        pole_color = (0.25, 0.25, 0.28, 1.0)
        pole_height = 5.0
        pole_width = 0.15

        card_maker.setFrame(-pole_width/2, pole_width/2, 0, pole_height)
        pole = parent.attachNewNode(card_maker.generate())
        pole.setColor(pole_color)

        # Light housing (hanging)
        housing_color = (0.15, 0.15, 0.15, 1.0)  # Black
        housing_width = 0.4
        housing_height = 1.2
        housing_depth = 0.35

        # Front of housing
        card_maker.setFrame(-housing_width/2, housing_width/2, 0, housing_height)
        housing_front = parent.attachNewNode(card_maker.generate())
        housing_front.setPos(0, -housing_depth/2, pole_height - housing_height - 0.3)
        housing_front.setColor(housing_color)

        # Traffic lights (red, yellow, green)
        light_radius = 0.15
        lights = [
            (pole_height - 0.5, (0.85, 0.08, 0.08, 1.0)),    # Red (top)
            (pole_height - 0.9, (0.95, 0.85, 0.12, 1.0)),    # Yellow (middle)
            (pole_height - 1.3, (0.12, 0.85, 0.25, 1.0)),    # Green (bottom)
        ]

        for light_z, light_color in lights:
            card_maker.setFrame(-light_radius, light_radius, -light_radius, light_radius)
            light = parent.attachNewNode(card_maker.generate())
            light.setPos(0, -housing_depth/2 - 0.02, light_z)
            light.setColor(light_color)

        # Visor above each light (sun shade)
        visor_color = (0.10, 0.10, 0.12, 1.0)
        for light_z, _ in lights:
            card_maker.setFrame(-housing_width/2, housing_width/2,
                               -0.08, 0)
            visor = parent.attachNewNode(card_maker.generate())
            visor.setPos(0, -housing_depth/2 - 0.1, light_z + light_radius + 0.02)
            visor.setP(-20)
            visor.setColor(visor_color)

    def _create_bench(self, parent: NodePath):
        """Create park bench"""
        card_maker = CardMaker("bench")

        # Bench colors
        wood_color = (0.55, 0.42, 0.28, 1.0)  # Wood
        metal_color = (0.25, 0.25, 0.28, 1.0)  # Dark metal

        # Seat (wood slats)
        seat_width = 1.5
        seat_depth = 0.5
        seat_height = 0.45

        # Seat surface
        card_maker.setFrame(-seat_width/2, seat_width/2, -seat_depth/2, seat_depth/2)
        seat = parent.attachNewNode(card_maker.generate())
        seat.setZ(seat_height)
        seat.setP(-90)
        seat.setColor(wood_color)

        # Backrest
        backrest_height = 0.5
        card_maker.setFrame(-seat_width/2, seat_width/2, 0, backrest_height)
        backrest = parent.attachNewNode(card_maker.generate())
        backrest.setPos(0, -seat_depth/2, seat_height)
        backrest.setP(-10)  # Slight angle for comfort
        backrest.setColor(wood_color)

        # Legs (4 metal legs)
        leg_positions = [
            (-seat_width/2 + 0.1, -seat_depth/2 + 0.1),
            (seat_width/2 - 0.1, -seat_depth/2 + 0.1),
            (-seat_width/2 + 0.1, seat_depth/2 - 0.1),
            (seat_width/2 - 0.1, seat_depth/2 - 0.1),
        ]

        for leg_x, leg_y in leg_positions:
            card_maker.setFrame(-0.05, 0.05, 0, seat_height)
            leg = parent.attachNewNode(card_maker.generate())
            leg.setPos(leg_x, leg_y, 0)
            leg.setColor(metal_color)

        # Armrests
        for x in [-seat_width/2, seat_width/2]:
            card_maker.setFrame(-0.08, 0.08, -seat_depth/2, seat_depth/2)
            armrest = parent.attachNewNode(card_maker.generate())
            armrest.setPos(x, 0, seat_height + 0.15)
            armrest.setH(90)
            armrest.setColor(wood_color)

    def _create_trash_can(self, parent: NodePath):
        """Create trash can"""
        card_maker = CardMaker("trash_can")

        # Trash can (cylindrical - represented as octagon)
        can_color = (0.25, 0.55, 0.30, 1.0)  # Green
        can_radius = 0.35
        can_height = 0.90

        sides = 8
        for i in range(sides):
            angle1 = (i / sides) * 360
            angle2 = ((i + 1) / sides) * 360

            x1 = can_radius * np.cos(np.radians(angle1))
            y1 = can_radius * np.sin(np.radians(angle1))
            x2 = can_radius * np.cos(np.radians(angle2))
            y2 = can_radius * np.sin(np.radians(angle2))

            side_width = np.sqrt((x2-x1)**2 + (y2-y1)**2)

            card_maker.setFrame(0, side_width, 0, can_height)
            side = parent.attachNewNode(card_maker.generate())
            side.setPos(x1, y1, 0)
            side.setH(angle1)
            side.setColor(can_color)

        # Lid
        lid_color = (0.20, 0.20, 0.22, 1.0)  # Dark lid
        card_maker.setFrame(-can_radius, can_radius, -can_radius, can_radius)
        lid = parent.attachNewNode(card_maker.generate())
        lid.setZ(can_height)
        lid.setP(-90)
        lid.setColor(lid_color)

        # Lid dome (slightly raised)
        dome_radius = can_radius * 0.7
        card_maker.setFrame(-dome_radius, dome_radius, -dome_radius, dome_radius)
        dome = parent.attachNewNode(card_maker.generate())
        dome.setZ(can_height + 0.1)
        dome.setP(-90)
        dome.setColor(lid_color)

    def _create_mailbox(self, parent: NodePath):
        """Create USPS-style mailbox"""
        card_maker = CardMaker("mailbox")

        # Mailbox (blue USPS color)
        box_color = (0.15, 0.35, 0.65, 1.0)  # Blue
        box_width = 0.4
        box_depth = 0.35
        box_height = 1.2
        box_z = 1.0

        # Post
        post_color = (0.25, 0.25, 0.28, 1.0)
        card_maker.setFrame(-0.08, 0.08, 0, box_z)
        post = parent.attachNewNode(card_maker.generate())
        post.setColor(post_color)

        # Box body
        # Front
        card_maker.setFrame(-box_width/2, box_width/2, 0, box_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -box_depth/2, box_z)
        front.setColor(box_color)

        # Back
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, box_depth/2, box_z)
        back.setH(180)
        back.setColor(box_color)

        # Sides
        card_maker.setFrame(-box_depth/2, box_depth/2, 0, box_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-box_width/2, 0, box_z)
        left.setH(90)
        left.setColor(box_color)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(box_width/2, 0, box_z)
        right.setH(-90)
        right.setColor(box_color)

        # Top (slanted)
        card_maker.setFrame(-box_width/2, box_width/2, -box_depth/2, box_depth/2)
        top = parent.attachNewNode(card_maker.generate())
        top.setZ(box_z + box_height)
        top.setP(-85)
        top.setColor(box_color)

        # Mail slot (white/silver)
        slot_color = (0.85, 0.85, 0.88, 1.0)
        card_maker.setFrame(-box_width/3, box_width/3, -0.05, 0.05)
        slot = parent.attachNewNode(card_maker.generate())
        slot.setPos(0, -box_depth/2 - 0.01, box_z + box_height/2)
        slot.setColor(slot_color)

    def _create_fire_hydrant(self, parent: NodePath):
        """Create fire hydrant"""
        card_maker = CardMaker("hydrant")

        # Hydrant (red/yellow)
        hydrant_color = (0.85, 0.15, 0.15, 1.0)  # Red
        cap_color = (0.95, 0.88, 0.15, 1.0)  # Yellow caps

        # Main body (cylindrical)
        body_radius = 0.25
        body_height = 0.80

        sides = 8
        for i in range(sides):
            angle1 = (i / sides) * 360
            angle2 = ((i + 1) / sides) * 360

            x1 = body_radius * np.cos(np.radians(angle1))
            y1 = body_radius * np.sin(np.radians(angle1))
            x2 = body_radius * np.cos(np.radians(angle2))
            y2 = body_radius * np.sin(np.radians(angle2))

            side_width = np.sqrt((x2-x1)**2 + (y2-y1)**2)

            card_maker.setFrame(0, side_width, 0, body_height)
            side = parent.attachNewNode(card_maker.generate())
            side.setPos(x1, y1, 0)
            side.setH(angle1)
            side.setColor(hydrant_color)

        # Top cap
        card_maker.setFrame(-body_radius, body_radius, -body_radius, body_radius)
        top = parent.attachNewNode(card_maker.generate())
        top.setZ(body_height)
        top.setP(-90)
        top.setColor(cap_color)

        # Side nozzles (2)
        nozzle_radius = 0.08
        nozzle_length = 0.20

        for angle in [90, -90]:  # Left and right
            x_pos = body_radius * np.cos(np.radians(angle))
            y_pos = body_radius * np.sin(np.radians(angle))

            card_maker.setFrame(-nozzle_radius, nozzle_radius,
                               -nozzle_radius, nozzle_radius)
            nozzle = parent.attachNewNode(card_maker.generate())
            nozzle.setPos(x_pos, y_pos, body_height * 0.6)
            nozzle.setH(angle)
            nozzle.setColor(hydrant_color)

            # Nozzle cap
            card_maker.setFrame(-nozzle_radius * 1.2, nozzle_radius * 1.2,
                               -nozzle_radius * 1.2, nozzle_radius * 1.2)
            cap = parent.attachNewNode(card_maker.generate())
            cap.setPos(x_pos + nozzle_length * np.cos(np.radians(angle)),
                      y_pos + nozzle_length * np.sin(np.radians(angle)),
                      body_height * 0.6)
            cap.setH(angle)
            cap.setColor(cap_color)

    def _create_bus_stop(self, parent: NodePath):
        """Create bus stop with shelter"""
        card_maker = CardMaker("bus_stop")

        # Shelter structure
        shelter_width = 2.5
        shelter_depth = 1.2
        shelter_height = 2.5

        # Support posts (4 corners)
        post_color = (0.35, 0.35, 0.38, 1.0)  # Metal gray
        post_width = 0.12

        posts = [
            (-shelter_width/2, -shelter_depth/2),
            (shelter_width/2, -shelter_depth/2),
            (-shelter_width/2, shelter_depth/2),
            (shelter_width/2, shelter_depth/2),
        ]

        for px, py in posts:
            card_maker.setFrame(-post_width/2, post_width/2, 0, shelter_height)
            post = parent.attachNewNode(card_maker.generate())
            post.setPos(px, py, 0)
            post.setColor(post_color)

        # Roof
        roof_color = (0.65, 0.65, 0.70, 1.0)  # Light gray
        card_maker.setFrame(-shelter_width/2 - 0.1, shelter_width/2 + 0.1,
                           -shelter_depth/2 - 0.1, shelter_depth/2 + 0.1)
        roof = parent.attachNewNode(card_maker.generate())
        roof.setZ(shelter_height)
        roof.setP(-90)
        roof.setColor(roof_color)

        # Back wall (glass/plastic)
        wall_color = (0.70, 0.75, 0.80, 0.5)  # Translucent
        card_maker.setFrame(-shelter_width/2, shelter_width/2, 0, shelter_height - 0.3)
        back_wall = parent.attachNewNode(card_maker.generate())
        back_wall.setPos(0, shelter_depth/2, 0.15)
        back_wall.setH(180)
        back_wall.setColor(wall_color)
        back_wall.setTransparency(TransparencyAttrib.MAlpha)

        # Bench inside
        bench_width = shelter_width * 0.7
        bench_depth = 0.4
        bench_height = 0.45
        bench_color = (0.45, 0.45, 0.48, 1.0)

        card_maker.setFrame(-bench_width/2, bench_width/2, -bench_depth/2, bench_depth/2)
        bench = parent.attachNewNode(card_maker.generate())
        bench.setPos(0, shelter_depth/4, bench_height)
        bench.setP(-90)
        bench.setColor(bench_color)

        # Bus stop sign
        sign_color = (0.95, 0.95, 0.95, 1.0)  # White
        sign_width = 0.5
        sign_height = 0.6

        card_maker.setFrame(-sign_width/2, sign_width/2, 0, sign_height)
        sign = parent.attachNewNode(card_maker.generate())
        sign.setPos(-shelter_width/2 - 0.3, 0, 1.8)
        sign.setColor(sign_color)

        # Sign post
        card_maker.setFrame(-0.05, 0.05, 0, 1.8)
        sign_post = parent.attachNewNode(card_maker.generate())
        sign_post.setPos(-shelter_width/2 - 0.3, 0, 0)
        sign_post.setColor(post_color)

    def _create_tree(self, parent: NodePath):
        """Create tree with trunk and foliage"""
        card_maker = CardMaker("tree")

        # Trunk (brown)
        trunk_color = (0.45, 0.32, 0.22, 1.0)
        trunk_radius = 0.3
        trunk_height = np.random.uniform(3.5, 5.5)

        # Trunk (octagonal)
        sides = 8
        for i in range(sides):
            angle1 = (i / sides) * 360
            angle2 = ((i + 1) / sides) * 360

            x1 = trunk_radius * np.cos(np.radians(angle1))
            y1 = trunk_radius * np.sin(np.radians(angle1))
            x2 = trunk_radius * np.cos(np.radians(angle2))
            y2 = trunk_radius * np.sin(np.radians(angle2))

            side_width = np.sqrt((x2-x1)**2 + (y2-y1)**2)

            card_maker.setFrame(0, side_width, 0, trunk_height)
            side = parent.attachNewNode(card_maker.generate())
            side.setPos(x1, y1, 0)
            side.setH(angle1)
            side.setColor(trunk_color)

        # Foliage (green, spherical - represented as multiple layers)
        foliage_colors = [
            (0.25, 0.65, 0.30, 1.0),  # Bright green
            (0.30, 0.55, 0.28, 1.0),  # Medium green
            (0.35, 0.70, 0.35, 1.0),  # Light green
        ]
        foliage_color = foliage_colors[np.random.randint(0, len(foliage_colors))]

        foliage_radius = np.random.uniform(1.5, 2.5)
        foliage_z = trunk_height

        # Create foliage as layered discs (simplified)
        for layer in range(5):
            layer_z = foliage_z + layer * 0.5
            layer_radius = foliage_radius * (1.0 - abs(layer - 2) * 0.2)

            card_maker.setFrame(-layer_radius, layer_radius, -layer_radius, layer_radius)
            foliage_layer = parent.attachNewNode(card_maker.generate())
            foliage_layer.setZ(layer_z)
            foliage_layer.setP(-90)
            foliage_layer.setColor(foliage_color)

    def _create_street_sign(self, parent: NodePath):
        """Create street sign"""
        card_maker = CardMaker("street_sign")

        # Post
        post_color = (0.30, 0.30, 0.33, 1.0)
        post_height = 2.5
        post_width = 0.08

        card_maker.setFrame(-post_width/2, post_width/2, 0, post_height)
        post = parent.attachNewNode(card_maker.generate())
        post.setColor(post_color)

        # Sign (green street name sign)
        sign_color = (0.20, 0.55, 0.30, 1.0)  # Green
        sign_width = 1.2
        sign_height = 0.25

        card_maker.setFrame(-sign_width/2, sign_width/2, -sign_height/2, sign_height/2)
        sign = parent.attachNewNode(card_maker.generate())
        sign.setPos(0, 0, post_height - 0.3)
        sign.setColor(sign_color)

        # Sign border (white)
        border_color = (0.95, 0.95, 0.95, 1.0)
        border_width = 0.03

        # Top border
        card_maker.setFrame(-sign_width/2, sign_width/2, sign_height/2 - border_width, sign_height/2)
        top_border = parent.attachNewNode(card_maker.generate())
        top_border.setPos(0, -0.01, post_height - 0.3)
        top_border.setColor(border_color)

    def _create_parking_meter(self, parent: NodePath):
        """Create parking meter"""
        card_maker = CardMaker("parking_meter")

        # Post
        post_color = (0.30, 0.30, 0.33, 1.0)
        post_height = 1.3
        post_width = 0.06

        card_maker.setFrame(-post_width/2, post_width/2, 0, post_height)
        post = parent.attachNewNode(card_maker.generate())
        post.setColor(post_color)

        # Meter head
        meter_color = (0.60, 0.62, 0.65, 1.0)  # Silver
        meter_width = 0.25
        meter_height = 0.35
        meter_depth = 0.15

        # Front
        card_maker.setFrame(-meter_width/2, meter_width/2, 0, meter_height)
        meter_front = parent.attachNewNode(card_maker.generate())
        meter_front.setPos(0, -meter_depth/2, post_height)
        meter_front.setColor(meter_color)

        # Back
        meter_back = parent.attachNewNode(card_maker.generate())
        meter_back.setPos(0, meter_depth/2, post_height)
        meter_back.setH(180)
        meter_back.setColor(meter_color)

        # Display screen (digital)
        screen_color = (0.15, 0.20, 0.15, 1.0)  # Dark green LCD
        card_maker.setFrame(-meter_width/3, meter_width/3, -meter_height/4, meter_height/4)
        screen = parent.attachNewNode(card_maker.generate())
        screen.setPos(0, -meter_depth/2 - 0.01, post_height + meter_height * 0.6)
        screen.setColor(screen_color)

    def _create_bike_rack(self, parent: NodePath):
        """Create bike rack"""
        card_maker = CardMaker("bike_rack")

        # Rack (metal)
        rack_color = (0.35, 0.35, 0.38, 1.0)
        num_loops = 5
        loop_width = 0.5
        loop_height = 0.80
        spacing = 0.6

        for i in range(num_loops):
            x_pos = (i - num_loops/2) * spacing

            # Vertical posts (2 per loop)
            post_radius = 0.04
            card_maker.setFrame(-post_radius, post_radius, 0, loop_height)

            left_post = parent.attachNewNode(card_maker.generate())
            left_post.setPos(x_pos - loop_width/2, 0, 0)
            left_post.setColor(rack_color)

            right_post = parent.attachNewNode(card_maker.generate())
            right_post.setPos(x_pos + loop_width/2, 0, 0)
            right_post.setColor(rack_color)

            # Horizontal bar (top of loop)
            card_maker.setFrame(x_pos - loop_width/2, x_pos + loop_width/2,
                               -post_radius, post_radius)
            top_bar = parent.attachNewNode(card_maker.generate())
            top_bar.setZ(loop_height)
            top_bar.setP(-90)
            top_bar.setColor(rack_color)

    def _create_newspaper_box(self, parent: NodePath):
        """Create newspaper vending box"""
        card_maker = CardMaker("newspaper_box")

        # Box (typically red or blue)
        box_colors = [
            (0.75, 0.15, 0.15, 1.0),  # Red
            (0.15, 0.35, 0.75, 1.0),  # Blue
        ]
        box_color = box_colors[np.random.randint(0, len(box_colors))]
        box_width = 0.55
        box_depth = 0.45
        box_height = 1.1

        # Front (with window)
        card_maker.setFrame(-box_width/2, box_width/2, 0, box_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -box_depth/2, 0)
        front.setColor(box_color)

        # Window (to see newspapers)
        window_color = (0.70, 0.75, 0.80, 0.6)  # Translucent
        card_maker.setFrame(-box_width/2 + 0.1, box_width/2 - 0.1, box_height * 0.3, box_height * 0.7)
        window = parent.attachNewNode(card_maker.generate())
        window.setPos(0, -box_depth/2 - 0.01, 0)
        window.setColor(window_color)
        window.setTransparency(TransparencyAttrib.MAlpha)

        # Back
        card_maker.setFrame(-box_width/2, box_width/2, 0, box_height)
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, box_depth/2, 0)
        back.setH(180)
        back.setColor(box_color)

        # Sides
        card_maker.setFrame(-box_depth/2, box_depth/2, 0, box_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-box_width/2, 0, 0)
        left.setH(90)
        left.setColor(box_color)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(box_width/2, 0, 0)
        right.setH(-90)
        right.setColor(box_color)


class PropManager:
    """Manages placement of environmental props in the city"""

    def __init__(self):
        """Initialize prop manager"""
        pass

    def place_street_props(self, parent_node: NodePath, road_positions: List[Tuple[float, float]],
                          density: float = 1.0):
        """Place street furniture along roads"""
        props_placed = []

        for i, (x, z) in enumerate(road_positions):
            # Street lights every 20m
            if i % 4 == 0:
                light = EnvironmentalProp(PropType.STREET_LIGHT)
                light_node = light.create_3d_model(parent_node, (x + 3, z, 0), heading=0)
                props_placed.append(light_node)

            # Random other props
            if np.random.random() < density * 0.1:
                prop_type = np.random.choice([
                    PropType.TRASH_CAN,
                    PropType.BENCH,
                    PropType.MAILBOX,
                    PropType.PARKING_METER,
                ])
                prop = EnvironmentalProp(prop_type)
                prop_node = prop.create_3d_model(parent_node, (x + 2.5, z + 1, 0))
                props_placed.append(prop_node)

        return props_placed

    def place_intersection_props(self, parent_node: NodePath, intersection_pos: Tuple[float, float]):
        """Place props at intersection"""
        x, z = intersection_pos
        props_placed = []

        # Traffic lights at each corner
        for corner_x, corner_z in [(x+5, z+5), (x-5, z+5), (x+5, z-5), (x-5, z-5)]:
            traffic_light = EnvironmentalProp(PropType.TRAFFIC_LIGHT)
            light_node = traffic_light.create_3d_model(parent_node, (corner_x, corner_z, 0))
            props_placed.append(light_node)

        return props_placed

    def place_park_props(self, parent_node: NodePath, park_area: Tuple[float, float, float, float]):
        """Place props in park areas"""
        x_min, z_min, x_max, z_max = park_area
        props_placed = []

        # Trees
        num_trees = np.random.randint(5, 15)
        for _ in range(num_trees):
            tree_x = np.random.uniform(x_min, x_max)
            tree_z = np.random.uniform(z_min, z_max)
            tree = EnvironmentalProp(PropType.TREE)
            tree_node = tree.create_3d_model(parent_node, (tree_x, tree_z, 0))
            props_placed.append(tree_node)

        # Benches
        num_benches = np.random.randint(3, 8)
        for _ in range(num_benches):
            bench_x = np.random.uniform(x_min, x_max)
            bench_z = np.random.uniform(z_min, z_max)
            bench = EnvironmentalProp(PropType.BENCH)
            bench_node = bench.create_3d_model(parent_node, (bench_x, bench_z, 0),
                                              heading=np.random.uniform(0, 360))
            props_placed.append(bench_node)

        return props_placed


if __name__ == "__main__":
    """Test environmental props"""
    print("Environmental Props System Test")
    print("=" * 70)

    for prop_type in PropType:
        print(f"  - {prop_type.name}")

    print("\n" + "=" * 70)
    print(f"Total prop types: {len(PropType)}")
    print("Complete city detailing system!")
