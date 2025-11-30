import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

def parse_fnt(fnt_path):
    with open(fnt_path, encoding='utf-8') as f:
        lines = f.readlines()
    info, common, chars_count = '', '', ''
    chars, page_map = [], {}
    for line in lines:
        if line.startswith('info '):
            info = line
        elif line.startswith('common '):
            common = line
        elif line.startswith('page '):
            m = re.match(r'page id=(\d+) file="(.+?)"', line)
            if m:
                page_id, file_name = int(m.group(1)), m.group(2)
                page_map[page_id] = file_name
        elif line.startswith('chars '):
            chars_count = line
        elif line.startswith('char '):
            chars.append(line)
    return info, common, chars_count, chars, page_map

def split_fnt(info, common, chars_count, chars, page_map, font_name, dds_files, out_dir):
    for page_id, dds_name in page_map.items():
        dds_src = dds_files.get(dds_name)
        if not dds_src:
            print(f"缺少DDS文件: {dds_name}")
            continue
        new_dds_name = f"{font_name}_{page_id}.dds"
        os.makedirs(out_dir, exist_ok=True)
        dds_dst = os.path.join(out_dir, new_dds_name)
        with open(dds_src, 'rb') as src, open(dds_dst, 'wb') as dst:
            dst.write(src.read())
        new_fnt_name = f"{font_name}_{page_id}.fnt"
        fnt_dst = os.path.join(out_dir, new_fnt_name)
        with open(fnt_dst, 'w', encoding='utf-8') as f:
            f.write(info)
            f.write(common)
            f.write(chars_count)
            for char in chars:
                if f"page={page_id}" in char:
                    f.write(char)
    print(f"导出完成: {out_dir}")

def main():
    root = tk.Tk()
    root.title("HOI4 Font Organizer")
    root.geometry("700x500")

    def open_url(url):
        import webbrowser
        webbrowser.open(url)

    folder_path = tk.StringVar()
    hoI4_mode = tk.BooleanVar()
    lang = tk.StringVar(value='en')

    texts = {
        'zh': {
            'title': 'HOI4 字体整理员',
            'select_folder': '选择字体文件夹:     ',
            'browse': '  浏览  ',
            'mode': 'HOI4 模式',
            'preview': '字体预览',
            'fnt': 'FNT 文件',
            'dds': 'DDS 文件',
            'exportable': '可导出',
            'export': '  导出字体  ',
            'lang': ' 语言模式 ',
            'zh': '简体中文',
            'en': 'English',
            'project': ' 项 目 地 址 ',
        },
        'en': {
            'title': 'HOI4 Font Organizer',
            'select_folder': 'Select Font Folder:',
            'browse': 'Browse',
            'mode': 'HOI4 Mode',
            'preview': 'Font Preview',
            'fnt': 'FNT File',
            'dds': 'DDS File',
            'exportable': 'Exportable',
            'export': 'Export Font',
            'lang': 'Language',
            'zh': '简体中文',
            'en': 'English',
            'project': 'Project URL',
        }
    }

    def update_ui():
        t = texts[lang.get()]
        root.title(t['title'])
        label_folder.config(text=t['select_folder'])
        btn_browse.config(text=t['browse'])
        chk_mode.config(text=t['mode'])
        preview_frame.config(text=t['preview'])
        preview_tree.heading('fnt', text=t['fnt'])
        preview_tree.heading('dds', text=t['dds'])
        preview_tree.heading('exportable', text=t['exportable'])
        export_btn.config(text=t['export'])
        btn_project.config(text=texts[lang.get()]['project'])
        label_lang.config(text=t['lang'])
        btn_zh.config(text=t['zh'])
        btn_en.config(text=t['en'])
        if folder_path.get():
            for i in preview_tree.get_children():
                preview_tree.delete(i)
            for font_name, fnt_paths in font_files.items():
                fnt_path = fnt_paths[0]
                try:
                    info, common, chars_count, chars, page_map = parse_fnt(fnt_path)
                except Exception as e:
                    preview_tree.insert('', 'end', values=(os.path.basename(fnt_path), '', f'解析错误: {e}'))
                    continue
                missing_dds = []
                dds_list = []
                for page_id, dds_name in page_map.items():
                    dds_list.append(dds_name)
                    if dds_name not in dds_files:
                        missing_dds.append(dds_name)
                if not missing_dds:
                    can_export = texts[lang.get()]['exportable'] if lang.get() == 'zh' else 'Yes'
                else:
                    if lang.get() == 'zh':
                        can_export = f'缺少: {";".join(missing_dds)}'
                    else:
                        can_export = f'Missing: {", ".join(missing_dds)}'
                preview_tree.insert('', 'end', values=(os.path.basename(fnt_path), ','.join(dds_list), can_export))

    font_files = {}
    dds_files = {}

    def select_folder():
        path = filedialog.askdirectory()
        if path:
            folder_path.set(path)
            font_files.clear()
            dds_files.clear()
            for root_dir, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith('.fnt'):
                        font_name = os.path.splitext(file)[0]
                        font_files.setdefault(font_name, []).append(os.path.join(root_dir, file))
                    elif file.lower().endswith('.dds'):
                        dds_files[file] = os.path.join(root_dir, file)
            for i in preview_tree.get_children():
                preview_tree.delete(i)
            for font_name, fnt_paths in font_files.items():
                fnt_path = fnt_paths[0]
                try:
                    info, common, chars_count, chars, page_map = parse_fnt(fnt_path)
                except Exception as e:
                    preview_tree.insert('', 'end', values=(os.path.basename(fnt_path), '', f'解析错误: {e}'))
                    continue
                missing_dds = []
                dds_list = []
                for page_id, dds_name in page_map.items():
                    dds_list.append(dds_name)
                    if dds_name not in dds_files:
                        missing_dds.append(dds_name)
                if not missing_dds:
                    can_export = texts[lang.get()]['exportable'] if lang.get() == 'zh' else 'Yes'
                else:
                    if lang.get() == 'zh':
                        can_export = f'缺少: {";".join(missing_dds)}'
                    else:
                        can_export = f'Missing: {", ".join(missing_dds)}'
                preview_tree.insert('', 'end', values=(os.path.basename(fnt_path), ','.join(dds_list), can_export))
            export_btn.config(state=tk.NORMAL if font_files else tk.DISABLED)

    def export_fonts():
        t = texts[lang.get()]
        out_base = folder_path.get()
        if not out_base:
            messagebox.showerror(t['title'], t['select_folder'])
            return
        for font_name, fnt_paths in font_files.items():
            fnt_path = fnt_paths[0]
            info, common, chars_count, chars, page_map = parse_fnt(fnt_path)
            out_dir = os.path.join(out_base, font_name)
            if hoI4_mode.get():
                out_dir = os.path.join(out_base, font_name, 'gfx', 'fonts', font_name)
            os.makedirs(out_dir, exist_ok=True)
            page_dds_map = {}
            for page_id, dds_name in page_map.items():
                dds_base = re.sub(r'_0*([0-9]+)$', r'_\1', os.path.splitext(dds_name)[0])
                new_dds_name = f"{font_name}_{page_id}.dds"
                dds_src = dds_files.get(dds_name)
                if not dds_src:
                    continue
                dds_dst = os.path.join(out_dir, new_dds_name)
                with open(dds_src, 'rb') as src, open(dds_dst, 'wb') as dst:
                    dst.write(src.read())
                page_dds_map[page_id] = new_dds_name
                new_fnt_name = f"{font_name}_{page_id}.fnt"
                fnt_dst = os.path.join(out_dir, new_fnt_name)
                with open(fnt_dst, 'w', encoding='utf-8') as f:
                    f.write(info)
                    f.write(common)
                    f.write(chars_count)
                    for char in chars:
                        if f"page={page_id}" in char:
                            f.write(char)
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
        messagebox.showinfo(t['title'], t['export'] + ' OK!')

    frame_top = tk.Frame(root)
    frame_top.pack(fill=tk.X, pady=10)
    label_folder = tk.Label(frame_top)
    label_folder.pack(side=tk.LEFT, padx=5)
    tk.Entry(frame_top, textvariable=folder_path, width=50).pack(side=tk.LEFT, padx=5)
    btn_browse = tk.Button(frame_top, command=select_folder)
    btn_browse.pack(side=tk.LEFT, padx=5)

    frame_mode = tk.Frame(root)
    frame_mode.pack(fill=tk.X, pady=5)
    chk_mode = tk.Checkbutton(frame_mode, variable=hoI4_mode)
    chk_mode.pack(side=tk.LEFT, padx=5)

    preview_frame = tk.LabelFrame(root)
    preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    preview_tree = ttk.Treeview(preview_frame, columns=("fnt", "dds", "exportable"), show="headings")
    preview_tree.heading("fnt", text="FNT 文件")
    preview_tree.heading("dds", text="DDS 文件")
    preview_tree.heading("exportable", text="可导出")
    preview_tree.pack(fill=tk.BOTH, expand=True)

    export_btn = tk.Button(root, state=tk.DISABLED, command=export_fonts)
    export_btn.pack(pady=10)

    frame_lang = tk.Frame(root)
    frame_lang.pack(fill=tk.X, pady=5)
    label_lang = tk.Label(frame_lang)
    label_lang.pack(side=tk.LEFT, padx=5)
    btn_zh = tk.Button(frame_lang, command=lambda: (lang.set('zh'), update_ui()))
    btn_zh.pack(side=tk.LEFT, padx=2)
    btn_en = tk.Button(frame_lang, command=lambda: (lang.set('en'), update_ui()))
    btn_en.pack(side=tk.LEFT, padx=2)

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    btn_project = tk.Button(bottom_frame, cursor="hand2", command=lambda: open_url("https://github.com/czxieddan/HOI4-Font-Oragnizer"))
    btn_project.pack(side=tk.RIGHT, padx=10)

    author_frame = tk.Frame(bottom_frame)
    author_frame.pack(side=tk.BOTTOM)
    label_by = tk.Label(author_frame, text="                         by")
    label_by.pack(side=tk.LEFT)
    def open_author(event=None):
        open_url("https://czxieddan.top")
    label_author = tk.Label(author_frame, text="CzXieDdan", fg="blue", cursor="hand2")
    label_author.pack(side=tk.LEFT)
    label_author.bind("<Button-1>", open_author)

    update_ui()
    root.mainloop()

if __name__ == "__main__":
    main()