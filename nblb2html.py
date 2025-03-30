## ZH_CN Original Version ##

import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip

def extract_nblb_info(file_path):
    entries = []
    current_entry = None
    current_field = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if '-' in line:
                parts = line.split('-', 1)
                field_part = parts[0].strip()
                value_part = parts[1].strip()
                
                if field_part == 'PMID':
                    if current_entry is not None:
                        entries.append(current_entry)
                    current_entry = {
                        'PMID': value_part,
                        'TI': '',
                        'LID': []
                    }
                    current_field = None
                elif field_part == 'TI':
                    current_entry['TI'] = value_part
                    current_field = 'TI'
                elif field_part == 'LID':
                    current_entry['LID'].append(value_part)
                    current_field = 'LID'
                else:
                    current_field = None
            else:
                if current_field == 'TI':
                    current_entry['TI'] += '\n' + line
                elif current_field == 'LID' and current_entry['LID']:
                    current_entry['LID'][-1] += '\n' + line

        if current_entry is not None:
            entries.append(current_entry)
    
    output = []
    for idx, entry in enumerate(entries, 1):
        ti = entry['TI'].replace('\n', ' ')  # 移除换行符
        pmid = entry['PMID']
        doi = next((lid for lid in entry['LID'] if '[doi]' in lid), '未找到DOI')
        
        output.append(f"{idx}、{ti}")
        output.append(f"PubMed_Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}")
        output.append(f"LID（DOI）: {doi}\n")
    
    return len(entries), '\n'.join(output).strip()

def main():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="选择.nblb文件",
        filetypes=[("NBLB 文件", "*.nblb")]
    )
    
    if not file_path:
        messagebox.showinfo("提示", "未选择文件")
        return
    
    try:
        count, result = extract_nblb_info(file_path)
        pyperclip.copy(result)
        messagebox.showinfo(
            "完成", 
            f"已找到 {count} 个PubMed ID\n结果已复制到剪贴板！\n\n"
            "粘贴查看完整结果（Ctrl+V）"
        )
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出错：{str(e)}")

if __name__ == "__main__":
    main()
