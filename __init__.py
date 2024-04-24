from .prompt_combinator import PromptCombinator

NODE_CLASS_MAPPINGS = {
    "PromptCombinator": PromptCombinator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombinator": "🔢 Prompt Combinator"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
