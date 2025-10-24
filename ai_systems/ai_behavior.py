"""
Advanced Behavior Tree System for NPC AI
Implements Phase 4: NPC Framework & Emergent AI
"""
from enum import Enum
from typing import Optional, List, Callable, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import numpy as np


class NodeStatus(Enum):
    """Behavior tree node execution status"""
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3


class BehaviorNode(ABC):
    """
    Abstract base class for behavior tree nodes.
    Implements the core behavior tree pattern used in modern game AI.
    """

    def __init__(self, name: str = "Node"):
        self.name = name
        self.status = NodeStatus.FAILURE

    @abstractmethod
    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        """
        Execute node logic.

        Args:
            blackboard: Shared memory/state for the agent

        Returns:
            NodeStatus indicating execution result
        """
        pass

    def reset(self):
        """Reset node state"""
        self.status = NodeStatus.FAILURE


# ==================== COMPOSITE NODES ====================

class Sequence(BehaviorNode):
    """
    Sequence node: executes children in order until one fails.
    Returns SUCCESS only if all children succeed.
    """

    def __init__(self, name: str = "Sequence", children: List[BehaviorNode] = None):
        super().__init__(name)
        self.children = children or []
        self.current_child = 0

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        """Execute children sequentially"""
        while self.current_child < len(self.children):
            child = self.children[self.current_child]
            status = child.tick(blackboard)

            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return NodeStatus.RUNNING

            if status == NodeStatus.FAILURE:
                self.current_child = 0  # Reset for next tick
                self.status = NodeStatus.FAILURE
                return NodeStatus.FAILURE

            # Success - move to next child
            self.current_child += 1

        # All children succeeded
        self.current_child = 0
        self.status = NodeStatus.SUCCESS
        return NodeStatus.SUCCESS

    def reset(self):
        super().reset()
        self.current_child = 0
        for child in self.children:
            child.reset()


class Selector(BehaviorNode):
    """
    Selector node: executes children until one succeeds.
    Returns FAILURE only if all children fail.
    Also known as "Priority Selector" or "Fallback".
    """

    def __init__(self, name: str = "Selector", children: List[BehaviorNode] = None):
        super().__init__(name)
        self.children = children or []
        self.current_child = 0

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        """Execute children until one succeeds"""
        while self.current_child < len(self.children):
            child = self.children[self.current_child]
            status = child.tick(blackboard)

            if status == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return NodeStatus.RUNNING

            if status == NodeStatus.SUCCESS:
                self.current_child = 0  # Reset for next tick
                self.status = NodeStatus.SUCCESS
                return NodeStatus.SUCCESS

            # Failure - try next child
            self.current_child += 1

        # All children failed
        self.current_child = 0
        self.status = NodeStatus.FAILURE
        return NodeStatus.FAILURE

    def reset(self):
        super().reset()
        self.current_child = 0
        for child in self.children:
            child.reset()


class Parallel(BehaviorNode):
    """
    Parallel node: executes all children simultaneously.
    Configurable success/failure policy.
    """

    def __init__(self, name: str = "Parallel",
                 children: List[BehaviorNode] = None,
                 success_threshold: int = 1):
        super().__init__(name)
        self.children = children or []
        self.success_threshold = success_threshold

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        """Execute all children in parallel"""
        success_count = 0
        failure_count = 0
        running_count = 0

        for child in self.children:
            status = child.tick(blackboard)

            if status == NodeStatus.SUCCESS:
                success_count += 1
            elif status == NodeStatus.FAILURE:
                failure_count += 1
            else:
                running_count += 1

        # Check success threshold
        if success_count >= self.success_threshold:
            self.status = NodeStatus.SUCCESS
            return NodeStatus.SUCCESS

        # Check if too many failures
        if failure_count > len(self.children) - self.success_threshold:
            self.status = NodeStatus.FAILURE
            return NodeStatus.FAILURE

        # Still running
        self.status = NodeStatus.RUNNING
        return NodeStatus.RUNNING


# ==================== DECORATOR NODES ====================

class Inverter(BehaviorNode):
    """Inverts the result of child node"""

    def __init__(self, name: str = "Inverter", child: BehaviorNode = None):
        super().__init__(name)
        self.child = child

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        if not self.child:
            return NodeStatus.FAILURE

        status = self.child.tick(blackboard)

        if status == NodeStatus.SUCCESS:
            return NodeStatus.FAILURE
        elif status == NodeStatus.FAILURE:
            return NodeStatus.SUCCESS
        else:
            return NodeStatus.RUNNING


class Repeater(BehaviorNode):
    """Repeats child node N times or until failure"""

    def __init__(self, name: str = "Repeater", child: BehaviorNode = None, count: int = -1):
        super().__init__(name)
        self.child = child
        self.max_count = count  # -1 = infinite
        self.current_count = 0

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        if not self.child:
            return NodeStatus.FAILURE

        while self.max_count < 0 or self.current_count < self.max_count:
            status = self.child.tick(blackboard)

            if status == NodeStatus.RUNNING:
                return NodeStatus.RUNNING

            if status == NodeStatus.FAILURE:
                self.current_count = 0
                return NodeStatus.FAILURE

            self.current_count += 1

            if self.max_count > 0 and self.current_count >= self.max_count:
                self.current_count = 0
                return NodeStatus.SUCCESS

        return NodeStatus.RUNNING


class Succeeder(BehaviorNode):
    """Always returns SUCCESS regardless of child result"""

    def __init__(self, name: str = "Succeeder", child: BehaviorNode = None):
        super().__init__(name)
        self.child = child

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        if self.child:
            self.child.tick(blackboard)
        return NodeStatus.SUCCESS


# ==================== CONDITION NODES ====================

class Condition(BehaviorNode):
    """
    Condition node: evaluates a boolean function.
    Used for decision-making in behavior trees.
    """

    def __init__(self, name: str, condition_fn: Callable[['Blackboard'], bool]):
        super().__init__(name)
        self.condition_fn = condition_fn

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        try:
            result = self.condition_fn(blackboard)
            self.status = NodeStatus.SUCCESS if result else NodeStatus.FAILURE
            return self.status
        except Exception as e:
            print(f"Condition '{self.name}' error: {e}")
            self.status = NodeStatus.FAILURE
            return NodeStatus.FAILURE


# ==================== ACTION NODES ====================

class Action(BehaviorNode):
    """
    Action node: executes an action function.
    Returns status based on action result.
    """

    def __init__(self, name: str, action_fn: Callable[['Blackboard'], NodeStatus]):
        super().__init__(name)
        self.action_fn = action_fn

    def tick(self, blackboard: 'Blackboard') -> NodeStatus:
        try:
            self.status = self.action_fn(blackboard)
            return self.status
        except Exception as e:
            print(f"Action '{self.name}' error: {e}")
            self.status = NodeStatus.FAILURE
            return NodeStatus.FAILURE


# ==================== BLACKBOARD SYSTEM ====================

@dataclass
class Blackboard:
    """
    Shared memory system for behavior trees.
    Stores agent state, perceptions, and goals.
    """
    data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from blackboard"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        """Set value in blackboard"""
        self.data[key] = value

    def has(self, key: str) -> bool:
        """Check if key exists"""
        return key in self.data

    def clear(self):
        """Clear all data"""
        self.data.clear()

    def update(self, updates: Dict[str, Any]):
        """Update multiple values"""
        self.data.update(updates)


# ==================== UTILITY FUNCTIONS ====================

class UtilityAI:
    """
    Utility-based AI for decision-making.
    Evaluates options based on utility scores for emergent behavior.
    """

    @dataclass
    class UtilityOption:
        name: str
        action: Callable[['Blackboard'], NodeStatus]
        utility_fn: Callable[['Blackboard'], float]

    def __init__(self, options: List[UtilityOption] = None):
        self.options = options or []

    def add_option(self, name: str,
                   action: Callable[['Blackboard'], NodeStatus],
                   utility_fn: Callable[['Blackboard'], float]):
        """Add a utility option"""
        self.options.append(UtilityAI.UtilityOption(name, action, utility_fn))

    def evaluate(self, blackboard: Blackboard) -> Optional[Callable]:
        """Evaluate all options and return best action"""
        if not self.options:
            return None

        best_utility = -float('inf')
        best_action = None

        for option in self.options:
            try:
                utility = option.utility_fn(blackboard)
                if utility > best_utility:
                    best_utility = utility
                    best_action = option.action
            except Exception as e:
                print(f"Utility evaluation error for {option.name}: {e}")

        return best_action


# ==================== BEHAVIOR TREE ====================

class BehaviorTree:
    """
    Main behavior tree class.
    Manages tree execution and state.
    """

    def __init__(self, root: BehaviorNode, blackboard: Blackboard = None):
        self.root = root
        self.blackboard = blackboard or Blackboard()

    def tick(self) -> NodeStatus:
        """Execute one iteration of the behavior tree"""
        if self.root:
            return self.root.tick(self.blackboard)
        return NodeStatus.FAILURE

    def reset(self):
        """Reset tree state"""
        if self.root:
            self.root.reset()

    def visualize(self, node: BehaviorNode = None, depth: int = 0) -> str:
        """Generate text visualization of tree structure"""
        if node is None:
            node = self.root

        indent = "  " * depth
        result = f"{indent}[{node.name}] ({node.__class__.__name__})\n"

        # Recursively visualize children
        if hasattr(node, 'children'):
            for child in node.children:
                result += self.visualize(child, depth + 1)
        elif hasattr(node, 'child') and node.child:
            result += self.visualize(node.child, depth + 1)

        return result


# ==================== EXAMPLE BEHAVIOR TREES ====================

def create_patrol_behavior() -> BehaviorTree:
    """Create simple patrol behavior tree"""
    blackboard = Blackboard()

    patrol = Sequence("Patrol", [
        Action("FindWaypoint", lambda bb: NodeStatus.SUCCESS),
        Action("MoveTo", lambda bb: NodeStatus.SUCCESS),
        Action("Wait", lambda bb: NodeStatus.SUCCESS)
    ])

    return BehaviorTree(patrol, blackboard)


def create_npc_behavior() -> BehaviorTree:
    """Create complex NPC behavior with multiple states"""
    blackboard = Blackboard()

    # Main behavior selector
    root = Selector("NPCBehavior", [
        # High priority: Handle threats
        Sequence("HandleThreat", [
            Condition("IsThreatened", lambda bb: bb.get("threatened", False)),
            Action("Flee", lambda bb: NodeStatus.SUCCESS)
        ]),

        # Medium priority: Fulfill needs
        Sequence("FulfillNeeds", [
            Condition("IsHungry", lambda bb: bb.get("hunger", 0) > 80),
            Action("FindFood", lambda bb: NodeStatus.SUCCESS),
            Action("Eat", lambda bb: NodeStatus.SUCCESS)
        ]),

        # Low priority: Social interaction
        Sequence("SocialInteraction", [
            Condition("CanSocialize", lambda bb: bb.get("social", 0) < 50),
            Action("FindNearbyNPC", lambda bb: NodeStatus.SUCCESS),
            Action("Interact", lambda bb: NodeStatus.SUCCESS)
        ]),

        # Default: Wander
        Action("Wander", lambda bb: NodeStatus.SUCCESS)
    ])

    return BehaviorTree(root, blackboard)


if __name__ == "__main__":
    # Test behavior tree
    tree = create_npc_behavior()

    print("Behavior Tree Structure:")
    print(tree.visualize())

    # Simulate ticks
    print("\nSimulating behavior:")
    tree.blackboard.set("hunger", 85)

    for i in range(5):
        status = tree.tick()
        print(f"Tick {i + 1}: {status}")
