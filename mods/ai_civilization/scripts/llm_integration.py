"""
LLM Integration for AI Civilization - Qwen 1.5B
Provides natural language reasoning for citizen decision-making

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import torch


@dataclass
class LLMConfig:
    """Configuration for LLM integration"""
    model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    max_tokens: int = 150
    temperature: float = 0.8
    batch_size: int = 4  # Process multiple citizens at once
    cache_enabled: bool = True
    cache_size: int = 100


class QwenCitizenLLM:
    """
    Qwen 1.5B-powered decision-making for AI citizens.

    Features:
    - Local inference (no API costs)
    - Batched processing for efficiency
    - Response caching for common scenarios
    - AMD GPU optimized
    """

    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self.model = None
        self.tokenizer = None
        self.response_cache = {}

        # Initialize model
        self._load_model()

    def _load_model(self):
        """Load Qwen model using transformers"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer

            print(f"Loading Qwen 1.5B on {self.config.device}...")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=True
            )

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16 if self.config.device == "cuda" else torch.float32,
                device_map="auto" if self.config.device == "cuda" else None,
                trust_remote_code=True
            )

            if self.config.device == "cpu":
                self.model = self.model.to(self.config.device)

            self.model.eval()
            print(f"Qwen 1.5B loaded successfully on {self.config.device}")

        except ImportError:
            print("ERROR: transformers not installed. Run: pip install transformers torch")
            print("Falling back to behavior tree mode...")
            self.model = None
        except Exception as e:
            print(f"ERROR loading Qwen: {e}")
            print("Falling back to behavior tree mode...")
            self.model = None

    def is_available(self) -> bool:
        """Check if LLM is loaded and ready"""
        return self.model is not None

    def generate_decision(self, citizen_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate decision for a citizen based on their current state.

        Args:
            citizen_state: Complete citizen state (needs, personality, memories, etc.)

        Returns:
            Decision dict with action, reasoning, and confidence
        """
        if not self.is_available():
            return {"action": "use_behavior_tree", "reasoning": "LLM not available", "confidence": 0.0}

        # Check cache first
        cache_key = self._create_cache_key(citizen_state)
        if self.config.cache_enabled and cache_key in self.response_cache:
            return self.response_cache[cache_key]

        # Build prompt
        prompt = self._build_decision_prompt(citizen_state)

        # Generate response
        response = self._generate(prompt)

        # Parse response into structured decision
        decision = self._parse_decision(response, citizen_state)

        # Cache result
        if self.config.cache_enabled:
            self.response_cache[cache_key] = decision

            # Limit cache size
            if len(self.response_cache) > self.config.cache_size:
                # Remove oldest entry
                self.response_cache.pop(next(iter(self.response_cache)))

        return decision

    def _build_decision_prompt(self, state: Dict[str, Any]) -> str:
        """Build prompt for decision-making"""

        # Extract key state info
        needs = state.get('needs', {})
        personality = state.get('personality', {})
        money = state.get('money', 0)
        items = state.get('items', [])
        nearby = state.get('num_nearby', 0)
        archetype = state.get('archetype', 'citizen')

        # Get critical need
        critical_need = max(needs, key=needs.get) if needs else 'none'
        critical_value = needs.get(critical_need, 0.5)

        # Build personality description
        personality_desc = []
        if personality.get('extraversion', 0.5) > 0.6:
            personality_desc.append("outgoing")
        elif personality.get('extraversion', 0.5) < 0.4:
            personality_desc.append("reserved")

        if personality.get('conscientiousness', 0.5) > 0.6:
            personality_desc.append("diligent")
        elif personality.get('conscientiousness', 0.5) < 0.4:
            personality_desc.append("spontaneous")

        if personality.get('agreeableness', 0.5) > 0.6:
            personality_desc.append("cooperative")
        elif personality.get('agreeableness', 0.5) < 0.4:
            personality_desc.append("competitive")

        personality_str = ", ".join(personality_desc) if personality_desc else "balanced"

        # Build context
        context_parts = []
        context_parts.append(f"You are a {archetype} with a {personality_str} personality.")
        context_parts.append(f"You have ${money:.0f} and {len(items)} items.")

        if nearby > 0:
            context_parts.append(f"There are {nearby} people nearby.")
        else:
            context_parts.append("You are alone.")

        # Describe needs
        need_desc = []
        if needs.get('hunger', 0) > 0.7:
            need_desc.append("very hungry")
        if needs.get('energy', 1.0) < 0.3:
            need_desc.append("exhausted")
        if needs.get('social', 0.5) < 0.3:
            need_desc.append("lonely")
        if needs.get('wealth', 0.5) < 0.3:
            need_desc.append("financially stressed")

        if need_desc:
            context_parts.append(f"You feel {', '.join(need_desc)}.")
        else:
            context_parts.append("You feel okay overall.")

        context = " ".join(context_parts)

        # Available actions
        actions = [
            "work (earn money but lose energy)",
            "rest (restore energy)",
            "socialize (talk to nearby people, satisfy social needs)",
            "seek_food (find food to reduce hunger)",
            "trade (exchange items/money with others)",
            "idle (do nothing, slight energy recovery)"
        ]

        # Build final prompt
        prompt = f"""<|im_start|>system
You are simulating a citizen in an AI society experiment. Make a realistic decision based on your current state.<|im_end|>
<|im_start|>user
{context}

Available actions:
{chr(10).join(f"- {a}" for a in actions)}

What should you do right now? Respond with ONLY the action name (one word: work/rest/socialize/seek_food/trade/idle) and a brief reason (max 20 words).<|im_end|>
<|im_start|>assistant
"""

        return prompt

    def _generate(self, prompt: str) -> str:
        """Generate response from model"""
        try:
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.config.device)

            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode
            response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

            return response.strip()

        except Exception as e:
            print(f"LLM generation error: {e}")
            return "idle because of an error"

    def _parse_decision(self, response: str, state: Dict) -> Dict[str, Any]:
        """Parse LLM response into structured decision"""

        # Valid actions
        valid_actions = ['work', 'rest', 'socialize', 'seek_food', 'trade', 'idle']

        # Extract action (first word typically)
        response_lower = response.lower()
        action = 'idle'  # default

        for valid_action in valid_actions:
            if valid_action in response_lower:
                action = valid_action
                break

        # Extract reasoning (everything after action word)
        reasoning = response.strip()
        if action in reasoning:
            reasoning = reasoning.split(action, 1)[-1].strip()

        # Clean reasoning
        if reasoning.startswith('because'):
            reasoning = reasoning[7:].strip()
        elif reasoning.startswith(':'):
            reasoning = reasoning[1:].strip()

        # Limit reasoning length
        if len(reasoning) > 100:
            reasoning = reasoning[:100] + "..."

        return {
            'action': action,
            'reasoning': reasoning,
            'confidence': 0.8,  # Could be calculated from model logits
            'raw_response': response
        }

    def _create_cache_key(self, state: Dict) -> str:
        """Create cache key from state (simplified)"""
        needs = state.get('needs', {})
        nearby = state.get('num_nearby', 0)

        # Round needs to nearest 0.1 for cache hits
        needs_rounded = {k: round(v, 1) for k, v in needs.items()}

        key_data = {
            'needs': needs_rounded,
            'nearby': nearby > 0,
            'archetype': state.get('archetype', 'citizen')
        }

        return json.dumps(key_data, sort_keys=True)

    def batch_generate_decisions(self, citizen_states: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate decisions for multiple citizens at once (more efficient).

        Args:
            citizen_states: List of citizen states

        Returns:
            List of decisions (same order as input)
        """
        if not self.is_available():
            return [{"action": "use_behavior_tree", "reasoning": "LLM not available", "confidence": 0.0}] * len(citizen_states)

        # Process in batches
        decisions = []

        for i in range(0, len(citizen_states), self.config.batch_size):
            batch = citizen_states[i:i + self.config.batch_size]

            # For now, process sequentially (true batching requires padding)
            # TODO: Implement proper batched inference
            batch_decisions = [self.generate_decision(state) for state in batch]
            decisions.extend(batch_decisions)

        return decisions


# Singleton instance
_llm_instance: Optional[QwenCitizenLLM] = None

def get_llm(config: LLMConfig = None) -> QwenCitizenLLM:
    """Get or create LLM singleton instance"""
    global _llm_instance

    if _llm_instance is None:
        _llm_instance = QwenCitizenLLM(config)

    return _llm_instance


if __name__ == "__main__":
    # Test LLM integration
    print("Testing Qwen 1.5B integration...")

    llm = get_llm()

    if llm.is_available():
        print("LLM loaded successfully!")

        # Test decision
        test_state = {
            'archetype': 'artist',
            'money': 150,
            'items': ['sketchbook', 'phone'],
            'needs': {
                'hunger': 0.8,
                'energy': 0.4,
                'social': 0.3,
                'wealth': 0.2,
                'safety': 1.0,
                'achievement': 0.5
            },
            'personality': {
                'openness': 0.7,
                'conscientiousness': 0.4,
                'extraversion': 0.6,
                'agreeableness': 0.7,
                'neuroticism': 0.5
            },
            'num_nearby': 3
        }

        print("\nTest citizen state:")
        print(f"  Archetype: {test_state['archetype']}")
        print(f"  Money: ${test_state['money']}")
        print(f"  Hunger: {test_state['needs']['hunger']:.2f}")
        print(f"  Energy: {test_state['needs']['energy']:.2f}")
        print(f"  Nearby: {test_state['num_nearby']}")

        print("\nGenerating decision...")
        decision = llm.generate_decision(test_state)

        print(f"\nDecision: {decision['action']}")
        print(f"Reasoning: {decision['reasoning']}")
        print(f"Confidence: {decision['confidence']:.2f}")

    else:
        print("LLM not available - using behavior trees")
