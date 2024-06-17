from .prompt_combinator import PromptCombinator
from .prompt_combinator import PromptCombinatorMerger
from .prompt_combinator import PromptCombinatorExportGallery

NODE_CLASS_MAPPINGS = {
    "PromptCombinator": PromptCombinator,
    "PromptCombinatorMerger": PromptCombinatorMerger,
    "PromptCombinatorExportGallery": PromptCombinatorExportGallery,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCombinator": "🔢 Prompt Combinator",
    "PromptCombinatorMerger": "🔢 Prompt Combinator Merger",
    "PromptCombinatorExportGallery": "🔢 Prompt Combinator Export Gallery",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
