import os
import google.generativeai as genai
import tkinter as tk
from tkinter import ttk, messagebox
import re

API_KEY = os.getenv("GEMINI_API_KEY", "apicode")
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


def format_bold_and_bullets(widget, text):
    widget.delete("1.0", tk.END)
    bold_pattern = r'\*\*(.*?)\*\*'
    bullet_pattern = r'(^|[\n])[\*-]\s'

    parts = re.split(bold_pattern, text)

    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            widget.insert(tk.END, part, 'bold')
        else:
            bullet_part = re.sub(bullet_pattern, r'\1• ', part)
            widget.insert(tk.END, bullet_part)


def is_code_relevant(user_code):
    patterns = [
        r'\b(?:def|function|class|import|for|while|if|else|return|try|catch|async|await|var|let|const|#|print|int|str|float|bool|list|dict|set|tuple)\b',
        r'[\w\s]*=[^=]',
        r'\b(print|input|len|range)\s*\(',
        r'(?<!\w)(x|y|z|a|b|c|i|j|k|m|n|o|p|q|r|s|t|u|v|w|x|y|z)\s*=',
        r'\b\d+\b',
        r'\".*?\"|\'[^\']*\'',
        r'\b\d+\.\d+\b',
    ]

    return any(re.search(pattern, user_code) for pattern in patterns)


def on_analyze():
    analyze_button.config(text="Analyzing...", state=tk.DISABLED)
    root.update_idletasks()

    user_code = code_input.get("1.0", tk.END).strip()

    if not user_code:
        messagebox.showwarning("Input Error", "Please enter code to analyze.")
        analyze_button.config(text="Analyze Code", state=tk.NORMAL)
        return

    if not is_code_relevant(user_code):
        messagebox.showwarning("Input Error", "The input does not appear to be valid code. Please check your input.")
        analyze_button.config(text="Analyze Code", state=tk.NORMAL)
        return

    try:
        analysis_result, vulnerabilities_suggestions = analyze_code(user_code)

        result_output.tag_configure('bold', font=('Helvetica', 12, 'bold'))
        result_output.insert(tk.END, "**Analysis Result**\n", 'bold')
        format_bold_and_bullets(result_output, analysis_result)

        vulnerabilities_output.tag_configure('bold', font=('Helvetica', 12, 'bold'))
        vulnerabilities_output.insert(tk.END, "**Vulnerabilities & Suggestions**\n", 'bold')
        format_bold_and_bullets(vulnerabilities_output, vulnerabilities_suggestions)

        target_language = language_var.get()
        if target_language:
            translated_code = translate_code(user_code, target_language)
            translated_output.delete("1.0", tk.END)
            translated_output.insert(tk.END, translated_code)

    finally:
        analyze_button.config(text="Analyze Code", state=tk.NORMAL)


def analyze_code(user_code):
    try:
        chat_session = model.start_chat(history=[])
        analysis_response = chat_session.send_message(user_code)
        analysis_result = analysis_response.text

        vulnerabilities_message = f"Analyze the following code for vulnerabilities and improvement suggestions:\n\n{user_code}"
        vulnerabilities_response = chat_session.send_message(vulnerabilities_message)
        vulnerabilities_suggestions = vulnerabilities_response.text

        return analysis_result, vulnerabilities_suggestions
    except Exception as e:
        return f"An error occurred: {e}", ""


def translate_code(user_code, target_language):
    try:
        translation_message = f"Translate this code to {target_language}:\n\n{user_code}"
        translation_response = model.start_chat().send_message(translation_message)
        code_only = re.sub(r'^.*?```(?:.*?)\n(.*?)```.*?$', r'\1', translation_response.text, flags=re.DOTALL)
        return code_only.strip()
    except Exception as e:
        return f"An error occurred during translation: {e}"


def reset_fields():
    code_input.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)
    vulnerabilities_output.delete("1.0", tk.END)
    translated_output.delete("1.0", tk.END)


root = tk.Tk()
root.title("Code Analyzer")
root.geometry("1000x700")
root.configure(bg='#1e1e1e')

main_frame = tk.Frame(root, bg='#1e1e1e')
main_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(main_frame, text="Enter Your Code:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').pack(padx=10, pady=5, anchor="w")

input_frame = tk.Frame(main_frame, bg='#2e2e2e')
input_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_rowconfigure(0, weight=1)

code_input = tk.Text(input_frame, height=10, bg='#2e2e2e', fg='white', insertbackground='white', font=("Consolas", 12), wrap="none")
code_input.grid(row=0, column=0, sticky="nsew")

input_scroll_y = tk.Scrollbar(input_frame, command=code_input.yview)
input_scroll_y.grid(row=0, column=1, sticky="ns")
code_input['yscrollcommand'] = input_scroll_y.set

input_scroll_x = tk.Scrollbar(input_frame, orient="horizontal", command=code_input.xview)
input_scroll_x.grid(row=1, column=0, sticky="ew")
code_input['xscrollcommand'] = input_scroll_x.set

language_var = tk.StringVar()
tk.Label(main_frame, text="Select Language for Translation:", font=("Helvetica", 12), bg='#1e1e1e', fg='white').pack(padx=10, pady=5, anchor="w")
language_dropdown = ttk.Combobox(main_frame, textvariable=language_var, font=("Helvetica", 12), state='readonly')
language_dropdown['values'] = ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go']
language_dropdown.pack(padx=10, pady=5, fill=tk.X)

button_frame = tk.Frame(main_frame, bg='#1e1e1e')
button_frame.pack(padx=10, pady=10, anchor="e")

analyze_button = ttk.Button(button_frame, text="Analyze Code", command=on_analyze)
analyze_button.pack(side=tk.LEFT, padx=5)
reset_button = ttk.Button(button_frame, text="Reset", command=reset_fields)
reset_button.pack(side=tk.LEFT, padx=5)

style = ttk.Style()
style.theme_use('clam')

style.configure('TNotebook.Tab', font=('Helvetica', 12, 'bold'), padding=[10, 5], background='#007acc', foreground='white', focuscolor=style.configure(".")["background"], borderwidth=1)
style.map('TNotebook.Tab', background=[('selected', '#e63946')], foreground=[('selected', 'white')])

style.configure('TNotebook', background='#1e1e1e', tabmargins=[2, 5, 2, 0])

output_notebook = ttk.Notebook(main_frame)
output_notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

result_frame = ttk.Frame(output_notebook)
output_notebook.add(result_frame, text="Analysis Result")

result_output_frame = tk.Frame(result_frame)
result_output_frame.pack(fill=tk.BOTH, expand=True)

result_output_frame.grid_columnconfigure(0, weight=1)
result_output_frame.grid_rowconfigure(0, weight=1)

result_output = tk.Text(result_output_frame, bg='#2e2e2e', fg='white', wrap="none", height=10)
result_output.grid(row=0, column=0, sticky="nsew")

result_scroll_y = tk.Scrollbar(result_output_frame, command=result_output.yview)
result_scroll_y.grid(row=0, column=1, sticky="ns")
result_output['yscrollcommand'] = result_scroll_y.set

result_scroll_x = tk.Scrollbar(result_output_frame, orient="horizontal", command=result_output.xview)
result_scroll_x.grid(row=1, column=0, sticky="ew")
result_output['xscrollcommand'] = result_scroll_x.set

vulnerabilities_frame = ttk.Frame(output_notebook)
output_notebook.add(vulnerabilities_frame, text="Vulnerabilities & Suggestions")

vulnerabilities_output_frame = tk.Frame(vulnerabilities_frame)
vulnerabilities_output_frame.pack(fill=tk.BOTH, expand=True)

vulnerabilities_output_frame.grid_columnconfigure(0, weight=1)
vulnerabilities_output_frame.grid_rowconfigure(0, weight=1)

vulnerabilities_output = tk.Text(vulnerabilities_output_frame, bg='#2e2e2e', fg='white', wrap="none", height=10)
vulnerabilities_output.grid(row=0, column=0, sticky="nsew")

vulnerabilities_scroll_y = tk.Scrollbar(vulnerabilities_output_frame, command=vulnerabilities_output.yview)
vulnerabilities_scroll_y.grid(row=0, column=1, sticky="ns")
vulnerabilities_output['yscrollcommand'] = vulnerabilities_scroll_y.set

vulnerabilities_scroll_x = tk.Scrollbar(vulnerabilities_output_frame, orient="horizontal", command=vulnerabilities_output.xview)
vulnerabilities_scroll_x.grid(row=1, column=0, sticky="ew")
vulnerabilities_output['xscrollcommand'] = vulnerabilities_scroll_x.set

translated_frame = ttk.Frame(output_notebook)
output_notebook.add(translated_frame, text="Translated Code")

translated_output_frame = tk.Frame(translated_frame)
translated_output_frame.pack(fill=tk.BOTH, expand=True)

translated_output_frame.grid_columnconfigure(0, weight=1)
translated_output_frame.grid_rowconfigure(0, weight=1)

translated_output = tk.Text(translated_output_frame, bg='#2e2e2e', fg='white', wrap="none", height=10)
translated_output.grid(row=0, column=0, sticky="nsew")

translated_scroll_y = tk.Scrollbar(translated_output_frame, command=translated_output.yview)
translated_scroll_y.grid(row=0, column=1, sticky="ns")
translated_output['yscrollcommand'] = translated_scroll_y.set

translated_scroll_x = tk.Scrollbar(translated_output_frame, orient="horizontal", command=translated_output.xview)
translated_scroll_x.grid(row=1, column=0, sticky="ew")
translated_output['xscrollcommand'] = translated_scroll_x.set

root.mainloop()
