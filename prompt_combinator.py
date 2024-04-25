from itertools import product


class PromptCombinator:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that generates all possible combinations of prompts from several lists of strings.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id_separator": ("STRING", {"default": '@'}),
                "comment_prefix": ("STRING", {"default": '#'}),
                "input_list_1": ("STRING", {"default": '', "multiline": True}),
                "input_list_2": ("STRING", {"default": '', "multiline": True}),
                "input_list_3": ("STRING", {"default": '', "multiline": True}),
                "input_list_4": ("STRING", {"default": '', "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("combinations", "id_1", "id_2", "id_3", "id_4")
    OUTPUT_IS_LIST = (True, True, True, True, True)

    FUNCTION = "execute"

    CATEGORY = "batch"

    def parse_input(self, input_list, id_separator, comment_prefix):
        # Split by newlines and ensure at least one empty element if list is empty
        entries = input_list.strip().split('\n') if input_list.strip() else ['']
        ids = []
        descriptions = []
        for entry in entries:
            # Skip processing for lines that are empty or start with comment prefix
            if entry.strip() == '' or entry.strip().startswith(comment_prefix):
                continue
            # Split entry by the separator, default to empty ID if separator not present
            parts = entry.split(id_separator, 1)
            if len(parts) == 1:
                ids.append('')
                descriptions.append(parts[0].strip())
            else:
                ids.append(parts[0].strip())
                descriptions.append(parts[1].strip())
        # If empty, guarantee that it returns at least an empty id and description
        if not ids:
            ids.append('')
        if not descriptions:
            descriptions.append('')

        return ids, descriptions

    def combine_descriptions_and_ids(self, *inputs, id_separator, comment_prefix):
        list_of_ids = []
        list_of_descriptions = []
        
        # Parse all inputs
        for input_list in inputs:
            ids, descriptions = self.parse_input(input_list, id_separator, comment_prefix)
            list_of_ids.append(ids)
            list_of_descriptions.append(descriptions)

        # Generate all combinations of descriptions and corresponding IDs
        all_description_combinations = list(product(*list_of_descriptions))
        all_id_combinations = list(product(*list_of_ids))

        # Flatten the list of combinations
        outputs = ['\n'.join(comb) for comb in all_description_combinations]
        id_lists = list(zip(*all_id_combinations))
    
        return outputs, id_lists

    def execute(self, id_separator, comment_prefix, input_list_1, input_list_2, input_list_3, input_list_4):
        combinations, (ids1, ids2, ids3, ids4) = self.combine_descriptions_and_ids(input_list_1, input_list_2, input_list_3, input_list_4, id_separator=id_separator, comment_prefix=comment_prefix)
        return (combinations, ids1, ids2, ids3, ids4)


class PromptCombinatorMerger:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that merges the prompts and IDs out of two PromptCombinators.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "combinations_1": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "combinations_2": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
            },
            "optional": {
                "input_id1_list_1": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id2_list_1": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id3_list_1": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id4_list_1": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id1_list_2": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id2_list_2": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id3_list_2": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "input_id4_list_2": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
            }
        }
    INPUT_IS_LIST = (True, True, True, True, True, True, True, True, True, True)

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("combinations", "id_1", "id_2", "id_3", "id_4")
    OUTPUT_IS_LIST = (True, True, True, True, True)

    FUNCTION = "execute"

    CATEGORY = "batch"

    def merge_lists(self, list1, list2):
        """
        Helper method to merge two lists, handling cases where one or both may be undefined or empty.
        """
        if not list1:
            list1 = []
        if not list2:
            list2 = []
        return list1 + list2

    def execute(self, combinations_1, input_id1_list_1, input_id2_list_1, input_id3_list_1, input_id4_list_1, combinations_2, input_id1_list_2, input_id2_list_2, input_id3_list_2, input_id4_list_2):
        # Combine the combinations and IDs lists from two sets of inputs
        combined_combinations = self.merge_lists(combinations_1, combinations_2)
        combined_ids1 = self.merge_lists(input_id1_list_1, input_id1_list_2)
        combined_ids2 = self.merge_lists(input_id2_list_1, input_id2_list_2)
        combined_ids3 = self.merge_lists(input_id3_list_1, input_id3_list_2)
        combined_ids4 = self.merge_lists(input_id4_list_1, input_id4_list_2)

        # Check if all outputs are empty, return None if so
        if not any([combined_combinations, combined_ids1, combined_ids2, combined_ids3, combined_ids4]):
            return None

        return (combined_combinations, combined_ids1, combined_ids2, combined_ids3, combined_ids4)
