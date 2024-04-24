from itertools import product


class PromptCombinator:
    """
    A example node
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

    CATEGORY = "batch/🔢 PromptCombinator"

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

