import os
import google.generativeai as genai
import tkinter as tk
from tkinter import ttk, messagebox
import re

API_KEY = os.getenv("GEMINI_API_KEY", "your_api")
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

def analyze_code(user_code):
    try:
        chat_session = model.start_chat(history=[])
        analysis_response = chat_session.send_message(user_code)
        analysis_result = format_bold_headings(analysis_response.text)

        vulnerabilities_message = f"Analyze the following code for vulnerabilities and improvement suggestions:\n\n{user_code}"
        vulnerabilities_response = chat_session.send_message(vulnerabilities_message)
        vulnerabilities_suggestions = vulnerabilities_response.text

        return analysis_result, vulnerabilities_suggestions
    except Exception as e:
        return f"An error occurred: {e}", ""

def format_bold_headings(text):
    return re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)

def translate_code(user_code, target_language):
    try:
        translation_message = f"Translate the following code to {target_language}:\n\n{user_code}"
        translation_response = model.start_chat().send_message(translation_message)
        return translation_response.text
    except Exception as e:
        return f"An error occurred during translation: {e}"

def on_analyze():
    user_code = code_input.get("1.0", tk.END).strip()
    if not user_code:
        messagebox.showwarning("Input Error", "Please enter code to analyze.")
        return

    analysis_result, vulnerabilities_suggestions = analyze_code(user_code)
    display_results(analysis_result, vulnerabilities_suggestions)

    target_language = language_var.get()
    if target_language:
        translated_code = translate_code(user_code, target_language)
        translated_output.delete("1.0", tk.END)
        translated_output.insert(tk.END, translated_code)

def display_results(analysis_result, vulnerabilities_suggestions):
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, analysis_result)

    vulnerabilities_output.delete("1.0", tk.END)
    vulnerabilities_output.insert(tk.END, vulnerabilities_suggestions)

def reset_fields():
    code_input.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)
    vulnerabilities_output.delete("1.0", tk.END)
    translated_output.delete("1.0", tk.END)

root = tk.Tk()
root.title("Code Analyzer")
root.geometry("800x600")
root.configure(bg='#1e1e1e')

canvas = tk.Canvas(root, bg='#1e1e1e')
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

for i in range(10):
    scrollable_frame.grid_rowconfigure(i, weight=1)
scrollable_frame.grid_columnconfigure(0, weight=1)

tk.Label(scrollable_frame, text="Enter Your Code:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').grid(row=0, column=0, padx=10, pady=5, sticky="w")
code_input = tk.Text(scrollable_frame, height=10, bg='#2e2e2e', fg='white', insertbackground='white', font=("Helvetica", 12))
code_input.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

language_var = tk.StringVar()
tk.Label(scrollable_frame, text="Select Language for Translation:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').grid(row=2, column=0, padx=10, pady=5, sticky="w")
language_dropdown = ttk.Combobox(scrollable_frame, textvariable=language_var, font=("Helvetica", 12), state='readonly')
language_dropdown['values'] = ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'Go']
language_dropdown.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

button_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
tk.Button(button_frame, text="Analyze Code", command=on_analyze, bg='#007acc', fg='white', font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Reset", command=reset_fields, bg='#e63946', fg='white', font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
button_frame.grid(row=4, column=0, padx=10, pady=10, sticky="e")

result_frame = tk.Frame(scrollable_frame)
tk.Label(result_frame, text="Analysis Result:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').pack(pady=5)
result_output = tk.Text(result_frame, height=10, width=70, bg='#2e2e2e', fg='white', insertbackground='white', font=("Helvetica", 12))
result_scroll = ttk.Scrollbar(result_frame, command=result_output.yview)
result_output.config(yscrollcommand=result_scroll.set)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_output.pack(pady=5, fill=tk.BOTH, expand=True)

vulnerabilities_frame = tk.Frame(scrollable_frame)
tk.Label(vulnerabilities_frame, text="Vulnerabilities and Suggestions:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').pack(pady=5)
vulnerabilities_output = tk.Text(vulnerabilities_frame, height=10, width=70, bg='#2e2e2e', fg='white', insertbackground='white', font=("Helvetica", 12))
vulnerabilities_scroll = ttk.Scrollbar(vulnerabilities_frame, command=vulnerabilities_output.yview)
vulnerabilities_output.config(yscrollcommand=vulnerabilities_scroll.set)
vulnerabilities_scroll.pack(side=tk.RIGHT, fill=tk.Y)
vulnerabilities_output.pack(pady=5, fill=tk.BOTH, expand=True)

translated_frame = tk.Frame(scrollable_frame)
tk.Label(translated_frame, text="Translated Code:", font=("Helvetica", 14, "bold"), bg='#1e1e1e', fg='white').pack(pady=5)
translated_output = tk.Text(translated_frame, height=10, width=70, bg='#2e2e2e', fg='white', insertbackground='white', font=("Helvetica", 12))
translated_scroll = ttk.Scrollbar(translated_frame, command=translated_output.yview)
translated_output.config(yscrollcommand=translated_scroll.set)
translated_scroll.pack(side=tk.RIGHT, fill=tk.Y)
translated_output.pack(pady=5, fill=tk.BOTH, expand=True)

result_frame.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")
vulnerabilities_frame.grid(row=6, column=0, padx=10, pady=5, sticky="nsew")
translated_frame.grid(row=7, column=0, padx=10, pady=5, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.mainloop()
