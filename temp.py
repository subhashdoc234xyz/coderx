import tkinter as tk
import math

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeViz - Scientific Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#0f172a") # Obsidian Background

        self.equation = ""
        self.ans = "0"
        
        # --- Display Screen ---
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            root, textvariable=self.display_var, font=('JetBrains Mono', 28, 'bold'), 
            bg="#09090b", fg="#0ea5e9", bd=0, justify="right", insertbackground="#0ea5e9"
        )
        self.display.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=30, pady=15, padx=10, sticky="nsew")

        # --- Button Layout ---
        buttons = [
            ['sin', 'cos', 'tan', 'log', 'ln'],
            ['(', ')', '^', '√', 'π'],
            ['7', '8', '9', 'DEL', 'AC'],
            ['4', '5', '6', '*', '/'],
            ['1', '2', '3', '+', '-'],
            ['0', '.', 'e', 'ANS', '=']
        ]

        # --- Generate Buttons ---
        for r, row in enumerate(buttons):
            for c, btn_text in enumerate(row):
                
                # Dynamic Coloring based on button type
                bg_color = "#1e293b"      # Obsidian Surface (Numbers)
                fg_color = "#f8fafc"      # Light text
                
                if btn_text in ('AC', 'DEL'):
                    bg_color = "#ef4444"  # Danger Red
                    fg_color = "#ffffff"
                elif btn_text == '=':
                    bg_color = "#0ea5e9"  # Primary Blue
                    fg_color = "#ffffff"
                elif btn_text in ('sin', 'cos', 'tan', 'log', 'ln', '√', '^', 'π', 'e', '(', ')', 'ANS'):
                    bg_color = "#334155"  # Darker gray for functions
                    fg_color = "#cbd5e1"
                elif btn_text in ('+', '-', '*', '/'):
                    bg_color = "#0284c7"  # Primary Dark for operators
                    fg_color = "#ffffff"

                btn = tk.Button(
                    root, text=btn_text, font=('Manrope', 14, 'bold'), 
                    bg=bg_color, fg=fg_color, activebackground="#94a3b8", 
                    activeforeground="#0f172a", borderwidth=0, cursor="hand2",
                    command=lambda t=btn_text: self.on_click(t)
                )
                btn.grid(row=r+1, column=c, padx=4, pady=4, sticky="nsew")

        # Configure grid weights so buttons expand to fill the window
        for i in range(5):
            root.grid_columnconfigure(i, weight=1)
        for i in range(7):
            root.grid_rowconfigure(i, weight=1)

    def on_click(self, char):
        if char == 'AC':
            self.equation = ""
        elif char == 'DEL':
            self.equation = self.equation[:-1]
        elif char == '=':
            try:
                # Prepare the string for Python's eval() function
                eval_str = self.equation
                eval_str = eval_str.replace('^', '**')
                eval_str = eval_str.replace('√', 'math.sqrt')
                eval_str = eval_str.replace('π', 'math.pi')
                eval_str = eval_str.replace('e', 'math.e')
                eval_str = eval_str.replace('sin', 'math.sin')
                eval_str = eval_str.replace('cos', 'math.cos')
                eval_str = eval_str.replace('tan', 'math.tan')
                eval_str = eval_str.replace('log', 'math.log10')
                eval_str = eval_str.replace('ln', 'math.log')
                eval_str = eval_str.replace('ANS', str(self.ans))
                
                # Evaluate the mathematical expression
                result = str(eval(eval_str))
                
                # Format float results to remove trailing zeros
                if '.' in result:
                    result = result.rstrip('0').rstrip('.')
                    
                self.ans = result
                self.equation = result
            except Exception:
                self.equation = "Error"
                
        elif char in ('sin', 'cos', 'tan', 'log', 'ln', '√'):
            if self.equation == "Error": self.equation = ""
            self.equation += char + '('
        else:
            if self.equation == "Error":
                self.equation = ""
            self.equation += char
            
        self.display_var.set(self.equation)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()