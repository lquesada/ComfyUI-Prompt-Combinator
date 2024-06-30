from itertools import product
import re
import random
import os
import base64

import folder_paths

from PIL import Image
from PIL.PngImagePlugin import PngInfo

import numpy as np

id_pattern = re.compile(r'^[a-zA-Z0-9 ]+$')

class PromptCombinator:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that generates all possible combinations of prompts from several lists of strings.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id_separator": ("STRING", {"default": '@'}),
                "comment_prefix": ("STRING", {"default": '#'}),
                "join_prompt_using": (["comma and space", "space", "enter"], {"default": "comma and space"}),
                "input_list_1": ("STRING", {"default": '', "multiline": True}),
            },
            "optional": {
                "input_list_2": ("STRING", {"default": '', "multiline": True}),
                "input_list_3": ("STRING", {"default": '', "multiline": True}),
                "input_list_4": ("STRING", {"default": '', "multiline": True}),
                "input_list_5": ("STRING", {"default": '', "multiline": True}),
                "input_list_6": ("STRING", {"default": '', "multiline": True}),
                "input_list_7": ("STRING", {"default": '', "multiline": True}),
                "input_list_8": ("STRING", {"default": '', "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING", "PROMPTCOMBINATORIDS", "STRING")
    RETURN_NAMES = ("prompts", "combination_ids", "filenames")
    OUTPUT_IS_LIST = (True, True, True)

    FUNCTION = "execute"

    CATEGORY = "prompt_combinator"

    def parse_input(self, input_list, id_separator, comment_prefix):
        entries = input_list.strip().split('\n') if input_list.strip() else ['']
        ids = []
        descriptions = []
        no_id_counter = 1

        for entry in entries:
            if entry.strip() == '' or entry.strip().startswith(comment_prefix):
                continue
            parts = entry.split(id_separator, 1)
            if len(parts) == 1:
                ids.append(None)
                descriptions.append(parts[0].strip())
            else:
                id_candidate = parts[0].strip()
                assert id_pattern.match(id_candidate), f'IDs can only contain alphanumeric characters (a-z, A-Z, 0-9). Offending id is {id_candidate}'
                ids.append(id_candidate)
                descriptions.append(parts[1].strip())

        if ids == []:
            ids.append('')
        if not descriptions:
            descriptions.append('')

        return ids, descriptions

    def combine_descriptions_and_ids(self, *inputs, id_separator, comment_prefix, join_prompt_using):
        list_of_ids = []
        list_of_descriptions = []
        no_id_counters = [1] * len(inputs)

        for input_idx, input_list in enumerate(inputs):
            ids, descriptions = self.parse_input(input_list, id_separator, comment_prefix)
            for i in range(len(ids)):
                if ids[i] is None:
                    ids[i] = f'input_{input_idx+1}_no_id_{no_id_counters[input_idx]}'
                    no_id_counters[input_idx] += 1
            list_of_ids.append(ids)
            list_of_descriptions.append(descriptions)

        all_description_combinations = list(product(*list_of_descriptions))
        all_id_combinations = list(product(*list_of_ids))

        if join_prompt_using == "comma and space":
            use = ', '
        elif join_prompt_using == "space":
            use = ' '
        else: #"enter"
            use = '\n'

        outputs = [use.join(filter(None, comb)).strip() for comb in all_description_combinations]
        ids_lists = [list(comb) for comb in all_id_combinations]

        return outputs, ids_lists

    def execute(self, id_separator, comment_prefix, join_prompt_using, input_list_1, input_list_2="", input_list_3="", input_list_4="", input_list_5="", input_list_6="", input_list_7="", input_list_8=""):
        prompts, ids = self.combine_descriptions_and_ids(
            input_list_1, input_list_2, input_list_3, input_list_4, input_list_5, input_list_6, input_list_7, input_list_8,
            id_separator=id_separator, comment_prefix=comment_prefix, join_prompt_using=join_prompt_using
        )

        filenames = []
        for id_list in ids:
            filename_parts = [id_part for id_part in id_list]
            filenames.append('-'.join(filename_parts))

        return prompts, ids, filenames


class PromptCombinatorMerger:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that merges the prompts and IDs out of two PromptCombinators.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts_1": ("STRING", {"forceInput": True}),
                "combination_ids_1": ("PROMPTCOMBINATORIDS",),
                "prompts_2": ("STRING", {"forceInput": True}),
                "combination_ids_2": ("PROMPTCOMBINATORIDS",),
            },
        }

    INPUT_IS_LIST = True

    RETURN_TYPES = ("STRING", "PROMPTCOMBINATORIDS", "STRING")
    RETURN_NAMES = ("prompts", "combination_ids", "filenames")
    OUTPUT_IS_LIST = (True, True, True)

    FUNCTION = "execute"

    CATEGORY = "prompt_combinator"

    def merge_lists(self, list1, list2):
        if not list1:
            list1 = []
        if not list2:
            list2 = []
        return list1 + list2

    def execute(self, prompts_1, combination_ids_1, prompts_2, combination_ids_2):
        combined_prompts = self.merge_lists(prompts_1, prompts_2)
        combined_ids = self.merge_lists(combination_ids_1, combination_ids_2)

        filenames = []
        for id_list in combination_ids_1:
            filename_parts = []
            for i, id_part in enumerate(id_list):
                if id_part.startswith('input_'):
                    filename_parts.append(f'input_merge_1_{id_part}')
                else:
                    filename_parts.append(id_part)
            filenames.append('-'.join(filename_parts))
        for id_list in combination_ids_2:
            filename_parts = []
            for i, id_part in enumerate(id_list):
                if id_part.startswith('input_'):
                    filename_parts.append(f'input_merge_2_{id_part}')
                else:
                    filename_parts.append(id_part)
            filenames.append('-'.join(filename_parts))

        return combined_prompts, combined_ids, filenames


class PromptCombinatorExportGallery:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that exports an .html gallery with all images, ids and prompts from Prompt Combinator.
    """
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "filename_prefix": ("STRING", {"default": "gallery"}),
                "image_export_format": ([".webp lossy 80", ".webp lossy 90", ".webp lossless", ".png lossless"], {"default": ".webp lossy 90"}),
                "embed_all_images_in_html": ("BOOLEAN", {"default": True}),
                "images": ("IMAGE",),
                "prompts": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "combination_ids": ("PROMPTCOMBINATORIDS",),
            },
        }
    INPUT_IS_LIST = True

    RETURN_TYPES = ()
    FUNCTION = "export_gallery"

    OUTPUT_NODE = True

    CATEGORY = "prompt_combinator"

    def export_gallery(self, filename_prefix, image_export_format, embed_all_images_in_html, images, prompts, combination_ids):
        assert len(combination_ids) == len(prompts), "Amount of combination ids must be the same as amount of prompts"
        assert len(images) == len(prompts), "Amount of images must be the same as amount of prompts"
        for image in images:
            assert image.shape[0] == 1, "All images must have a batch size of 1 to export a gallery. You must have done something unexpected."

        # Convert filename prefix input from array to string
        assert len(filename_prefix) == 1, "Only a filename prefix is allowed"
        filename_prefix = filename_prefix[0]
        filename_prefix = re.sub(r'[^\w().-/]', '_', filename_prefix)

        assert len(image_export_format) == 1, "Only an export format is allowed"
        image_export_format = image_export_format[0]

        assert len(embed_all_images_in_html) == 1, "Only an embed_all_images_in_html value is allowed"
        embed_all_images_in_html = embed_all_images_in_html[0]

        # Prepare output directories vs. tmp
        self.output_dir = folder_paths.get_output_directory()
        if not embed_all_images_in_html:
            output_dir = folder_paths.get_output_directory()
            final_dir = folder_paths.get_output_directory()
        else:
            self.type = "temp"
            output_dir = folder_paths.get_temp_directory()
            final_dir = folder_paths.get_output_directory()

        # Prepare list of ids for html
        ids = [[] for _ in range(8)]
        for combination in combination_ids:
            for i, id_part in enumerate(combination):
                if id_part not in ids[i]:
                    ids[i].append(id_part)

        # After processing all combinations, check each slot
        for i in range(len(ids)):
            if len(ids[i])==1 and ids[i][0] == '':
                ids[i] = []

        ids_text = []
        for id_list in ids:
            if id_list:
                ids_text.append(f'{id_list}')
            else:
                ids_text.append('null')

        # Loop until we find a unique filename and directory
        counter = 0
        while True:
            if counter == 0:
                output_file = os.path.join(final_dir, f"{filename_prefix}.html")
                files_dir = os.path.join(output_dir, f"{filename_prefix}_files")
                fileprefix = os.path.join(os.path.basename(f"{filename_prefix}_files"), "img-")
                savefilenameprefix = os.path.join(f"{filename_prefix}_files", "img-")
            else:
                output_file = os.path.join(final_dir, f"{filename_prefix}_{counter:05d}.html")
                files_dir = os.path.join(output_dir, f"{filename_prefix}_{counter:05d}_files")
                fileprefix = os.path.join(os.path.basename(f"{filename_prefix}_{counter:05d}_files"), "img-")
                savefilenameprefix = os.path.join(f"{filename_prefix}_{counter:05d}_files", "img-")
        
            if not os.path.exists(output_file) and not os.path.exists(files_dir):
                break
    
            counter += 1

        assert os.path.commonpath((final_dir, os.path.abspath(output_file))) == final_dir, "Saving outside the output folder is not allowed."
        assert os.path.commonpath((output_dir, os.path.abspath(files_dir))) == output_dir, "Saving outside the output folder is not allowed."

        os.makedirs(files_dir, exist_ok=True)

        if image_export_format == ".png lossless":
            filesuffix = ".png"
        else: # .webp
            filesuffix = ".webp"
    
        results = list()
        this_filenames = []
        save_filenames = []
        this_fileid = []
        for i, id_list in enumerate(combination_ids):
            filename_parts = []
            for id_part in id_list:
                filename_parts.append(id_part)
            file = '-'.join(filename_parts)
            this_filename = fileprefix + file + filesuffix
            save_filename = os.path.join(output_dir, savefilenameprefix + file + filesuffix)

            image = images[i]
            im = 255. * image.squeeze(0).cpu().numpy()
            img = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
            # Export image
            if image_export_format == ".png lossless":
                metadata = PngInfo()
                img.save(save_filename, pnginfo=metadata, compress_level=4)
                datatype = "data:image/png"
                extension = "png"
            else: # .webp
                imgexif = img.getexif()
                datatype = "data:image/webp"
                extension = "webp"
                if image_export_format == ".webp lossy 80":
                    img.save(save_filename, method=6, exif=imgexif, lossless=False, quality=80)
                elif image_export_format == ".webp lossy 90":
                    img.save(save_filename, method=6, exif=imgexif, lossless=False, quality=90)
                else: # ".webp lossless"
                    img.save(save_filename, method=6, exif=imgexif, lossless=True, quality=0)
            this_fileid.append(file)
            this_filenames.append(this_filename)
            save_filenames.append(save_filename)

        images_text = "["
        for i in range(len(save_filenames)):
            save_filename = save_filenames[i]
            this_filename = this_filenames[i]
            fileid = this_fileid[i]
            prompt = prompts[i]
            results.append({
                "filename": os.path.basename(os.path.normpath(save_filename)),
                "subfolder": os.path.dirname(os.path.normpath(save_filename)),
                "type": self.type
            });
            if not embed_all_images_in_html:
                images_text += "{ id: \""+ fileid +"\", filename: \""+ this_filename +"\", prompt: \""+prompt.replace('"', "'")+"\"},"
            else:
                base64_string = ''
                with open(save_filename, "rb") as f:
                    file_content = f.read()
                    base64_string = base64.b64encode(file_content).decode('utf-8')
                images_text += "{ id: \""+ fileid +"\", base64data: \""+ datatype +";base64,"+ base64_string +"\", prompt: \""+prompt.replace('"', "'")+"\"},"
        images_text += "]"

        data = {
            "{!ids1}": ids_text[0],
            "{!ids2}": ids_text[1],
            "{!ids3}": ids_text[2],
            "{!ids4}": ids_text[3],
            "{!ids5}": ids_text[4],
            "{!ids6}": ids_text[5],
            "{!ids7}": ids_text[6],
            "{!ids8}": ids_text[7],
            "{!fileprefix}": '"'+fileprefix.replace('"', '\\"')+'"',
            "{!filesuffix}": '"'+filesuffix.replace('"', '\\"')+'"',
            "{!images}": images_text,
            "{!width}": str(images[0].shape[2]),
            "{!height}": str(images[0].shape[1]),
            "{!format}": '"'+extension+'"',
        }

        # Read HTML template, fill in, and write HTML to file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if not embed_all_images_in_html:
            template_file = os.path.join(script_dir, 'html.template')
        else:
            template_file = os.path.join(script_dir, 'html_embedded.template')
        with open(template_file, 'r') as file:
            html_template = file.read()

        rep = dict((re.escape(k), v) for k, v in data.items()) 
        pattern = re.compile("|".join(rep.keys()))
        filled_html = pattern.sub(lambda m: rep[re.escape(m.group(0))], html_template)

        with open(output_file, 'w') as file:
            file.write(filled_html)
    
        print("Exported gallery to ",output_file)

        return { "ui": { "images": results } }


class PromptCombinatorRandomPrompt:
    """
    ComfyUI-Prompt-Combinator
    https://github.com/lquesada/ComfyUI-Prompt-Combinator

    Node that picks a random prompt from a prompt combinator output.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompts": ("STRING", {"default": '', "multiline": True, "forceInput": True}),
                "combination_ids": ("PROMPTCOMBINATORIDS",),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
        }
    INPUT_IS_LIST = True

    RETURN_TYPES = ("STRING", "PROMPTCOMBINATORIDS", "STRING")
    RETURN_NAMES = ("prompt", "combination_id", "filename")
    FUNCTION = "pick_random"

    OUTPUT_NODE = True

    CATEGORY = "prompt_combinator"

    def pick_random(self, prompts, combination_ids, seed):
        assert len(combination_ids) == len(prompts), "Amount of combination ids must be the same as amount of prompts"
    
        index = random.randint(0, len(prompts) - 1)
        prompt = prompts[index]
        combination_id = combination_ids[index]

        filename = '-'.join(combination_id)

        return (prompt, combination_id, filename)
