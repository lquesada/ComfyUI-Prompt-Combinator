ComfyUI-Prompt-Combinator

Copyright (c) 2024, Luis Quesada Torres - https://github.com/lquesada | www.luisquesada.com

Check ComfyUI here: https://github.com/comfyanonymous/ComfyUI

# Overview

"🔢 Prompt Combinator" is a node that generates all possible combinations of prompts from several lists of strings.

"🔢 Prompt Combinator Merger" is a node that enables merging the output of two different "🔢 Prompt Combinator" nodes.

"🔢 Prompt Combinator Export Gallery" is a node that generates an .html gallery to navigate the output of Prompt Combinator (prompts vs. images)

See an example of gallery [here](example_gallery.html).

## Simple example
Download the following example workflow from [here](prompt-combinator_example_workflow.json) or drag and drop the screenshot into ComfyUI.

![Workflow](prompt-combinator_example_workflow.png)

# Installation Instructions

Install via ComfyUI-Manager or go to the custom_nodes/ directory and run ```$ git clone https://github.com/lquesada/ComfyUI-Prompt-Combinator.git```

# Detailed Use Case
You want to produce all possible combinations of prompts from several lists of strings, e.g.

**Input list 1:**
```
a cat
a dog
```

**Input list 2:**
```
with pointy ears
with fluffy tail
with two heads
```

**Input list 3:**
```
cute
scary
```

**Expected output:** a list of strings that contain
```
a cat
with pointy ears
cute

a cat
with pointy ears
scary

a cat
with fluffy tail
cute

a cat
with fluffy tail
scary

a cat
with two heads
cute

a cat
with two heads
scary

a dog
with pointy ears
cute

a dog
with pointy ears
scary

a dog
with fluffy tail
cute

a dog
with fluffy tail
scary

a dog
with two heads
cute

a dog
with two heads
scary
```

Additionally, you may want to be able to identify what inputs were used in order to craft the filename_prefix, e.g.:
cat, pointy ears, scary_00001_.png
dog, two heads, cute_00001_.png

In order to achieve that, prepend the prompts with ids, e.g.:

**Input list 1:**
```
cat@a cat
dog@a dog
```

**Input list 2:**
```
pointy ears@with pointy ears
fluffy tail@with fluffy tail
two heads@with two heads
```

**Input list 3:**
```
cute@cute
scary@scary
```

# Changelog
## 2024-06-17
- Added Prompt Combinator Export Gallery node.
- Simplified input/output setup.
## 2024-05-25
- Extended from 4 inputs to 8 inputs.
## 2024-04-25
- Added Prompt Combinator Merge node.
## 2024-04-24
- Initial commit.

# License
Creative Commons License Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0), see [LICENSE](LICENSE)
