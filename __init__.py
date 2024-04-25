from .prompt_combinator import PromptCombinator
from .prompt_combinator import PromptCombinatorMerger

NODE_CLASS_MAPPINGS = {
    "PromptCombinator": PromptCombinator,
    "PromptCombinatorMerger": PromptCombinatorMerger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombinator": "🔢 Prompt Combinator",
    "PromptCombinatorMerger": "🔢 Prompt Combinator Merger"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
