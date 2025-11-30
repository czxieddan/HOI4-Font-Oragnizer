<div align="center">
<!-- Title: -->
  <a href="https://czxieddan.top/">
    <img src="https://i.imgur.com/h1Kllvh.png" height="200">
  </a>
  <h1>HOI4 Font Oragnizer - <a href="https://github.com/czxieddan/">CzXieDdan</a></h1>
  <a href="https://docs.python.org/3.14/">
    <img src="https://img.shields.io/badge/HOI4%20Font%20Oragnizer-93CE70?logo=python&logoColor=FFDF58&labelColor=3D7AAB&label=Python%203.14%20Powered" height="20">
  </a>
</div>

A handy tool that helps you organize large batches of **`.fnt` files** for use in _**HOI4**_ as your excellent organizer.

## DESCRIPTION

### Usage

As everyone knows, in **_HOI4_**, each **`.fnt` file** needs to be paired with a corresponding **`.dds` file**. But in fact, most of the other software on the market, such as **_bmfont64_**, export **`.fnt` files** where all the pages in the **`.fnt`** are stored in a single, unique **`.fnt`**. This cannot be used normally in _**HOI4**_. Therefore, we often need to manually separate the characters corresponding to each messy page from the **`.fnt` file**. If you're struggling with large-scale manual tasks, then this organizer will become your best partner.

### Feature
1. #### Visualization and Clean interface
    You can see the UI here.
   
    <img width="730" height="560" alt="df23dfa0cbcaba4a5d0a3c1fc00e48ce" src="https://github.com/user-attachments/assets/3023eada-6276-46f9-957e-1ea92c23306a" />
    
    **Visualization** frees you from the hassle of the command line and lets you experience your results more intuitively, while the **Clean interface** design helps you quickly understand what you need to do.

3. #### Multilingual
    Supports **Simplified Chinese**.
   
    <img width="730" height="560" alt="dfb67d436493c27b41414c82492e273f" src="https://github.com/user-attachments/assets/3042d7ab-7d75-4632-afec-e9773ab49b3b" />
    
    Serving the largest **_HOI4_ modding community** in the world today.
5. #### Table
    + Concise and to-the-point prompt. You can quickly find out if you are missing any files.
    <img width="730" height="560" alt="e944e9a6fa9f178c485c6846648e1fa8" src="https://github.com/user-attachments/assets/33790673-585d-47fc-8da7-123f704b4e47" />

    + Supports one-time import and batch classification and organization of multiple fonts.
    <img width="730" height="560" alt="080edcbbc9194e1deb73600af238b170" src="https://github.com/user-attachments/assets/56bc05f3-f564-428f-8693-bad64de4e76e" />

6. #### **_HOI4_** Mode
    Automatically generate additional **_HOI4_** font **`.gfx` Graphical asset files** with one click, and ensure all files are placed according to the addresses required by the **_HOI4_ Mod**.
    <img width="730" height="560" alt="cbe71bae66f6771af19678cf8a6b8a6d" src="https://github.com/user-attachments/assets/c1ffd4f6-6ee9-419a-8099-abc6e3a12d6e" />

    ```python
    if hoI4_mode.get():
        gfx_dir = os.path.join(out_base, font_name, 'interface', 'fonts')
        os.makedirs(gfx_dir, exist_ok=True)
        gfx_path = os.path.join(gfx_dir, f"{font_name}.gfx")
        fontfiles = []
        for page_id in sorted(page_dds_map.keys()):
            fontfiles.append(f'\t\t\t"gfx/fonts/{font_name}/{font_name}_{page_id}"')
        gfx_content = (
            "bitmapfonts = {\n"
            "\tbitmapfont = {\n"
            f"\t\tname = \"{font_name}\"\n"
            "\t\tfontfiles = {\n"
            f"{chr(10).join(fontfiles)}\n"
            "\t\t}\n"
            "\t\tcolor = 0xffffffff\n"
            "\t\tborder_color = 0x00000000\n"
            "\t}\n"
            "}"
        )
        with open(gfx_path, 'w', encoding='utf-8') as f:
            f.write(gfx_content)
    ```
7. #### Organize
    When exporting, all fonts will be sorted into their respective folders according to their names.
8. #### Versatility
    Common libraries save you from tedious configuration.
    ```python
    import os
    import re
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from PIL import Image, ImageTk
    ```

## HOW TO USE

1. ### Non-technical user (Windows)
    Directly download our latest executable program.
    
    <a href="https://github.com/czxieddan/HOI4-Font-Oragnizer/releases/download/v0.0.1/HOI4.Font.Organizer-0.0.1.exe"><img src="https://img.shields.io/badge/Download-v0.0.1-brightgreen?style=for-the-badge" height="30"></a>

2. ### Python <a href="https://docs.python.org/3.14/"><img src="https://img.shields.io/badge/HOI4%20Font%20Oragnizer-93CE70?logo=python&logoColor=FFDF58&labelColor=3D7AAB&label=Python%203.14%20Powered" height="16"></a>

    Get the project.
    
    <a href="https://github.com/czxieddan/HOI4-Font-Oragnizer/archive/refs/tags/v0.0.1.zip"><img src="https://img.shields.io/badge/Download-v0.0.1-brightgreen?style=for-the-badge" height="30"></a>

## SPECIAL PROMPT
    
### **AI** Generated Content Disclosure
Generative AI technology was used to assist in the production of this project, including but not limited to **_GPT-4.1_**.

### Special Thanks
    
<div align="center"><a href="https://steamcommunity.com/sharedfiles/filedetails/?id=3445449478"><img width="849" height="361" alt="SZTSG" src="https://github.com/user-attachments/assets/2bee341e-253a-4066-a76b-a892e630e111" /></a></div>

Thank **_[The Library of Shuang Ze](https://github.com/Paradox-Developer-Foundation/QIUQI-LIBRARY)_** for its long-term significant contributions to the Simplified Chinese modder community, which have had a tremendous impact on the community's development. We would like to give special thanks for this.
