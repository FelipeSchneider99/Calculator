import tkinter as tk

last_was_result = False  # Track if last action was '='
last_result = None       # Store last result

def on_click(value):
    global last_was_result, last_result
    current = display_var.get()
    operators = {'+', '-', 'x', '÷'}

    if value == 'c':
        display_var.set('')
        last_was_result = False
        last_result = None
    elif value == '=':
        try:
            import ast
            import operator

            expr = current.replace('x', '*').replace('÷', '/')

            # Safe eval using ast
            def safe_eval(expr):
                allowed_operators = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.USub: operator.neg
                }

                def _eval(node):
                    if isinstance(node, ast.Num):
                        return node.n
                    elif isinstance(node, ast.BinOp):
                        if type(node.op) in allowed_operators:
                            return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
                        else:
                            raise ValueError("Unsupported operator")
                    elif isinstance(node, ast.UnaryOp):
                        if type(node.op) in allowed_operators:
                            return allowed_operators[type(node.op)](_eval(node.operand))
                        else:
                            raise ValueError("Unsupported unary operator")
                    else:
                        raise ValueError("Unsupported expression")

                node = ast.parse(expr, mode='eval').body
                return _eval(node)

            result = str(safe_eval(expr))
            display_var.set(result)
            last_result = result
            last_was_result = True
        except Exception:
            display_var.set('Error')
            last_result = None
            last_was_result = True
    else:
        if last_was_result:
            if value in operators and last_result is not None and last_result not in ('Error', ''):
                # Start new operation with last_result + operator
                display_var.set(str(last_result) + value)
                last_was_result = False
                return
            else:
                # Start new number, clear display
                display_var.set('')
                last_was_result = False
                # fall through to add digit below

        # Prevent two operators in a row
        if value in operators:
            if not current:
                # If display is empty but last_result exists, use last_result
                if last_result is not None and last_result not in ('Error', ''):
                    display_var.set(str(last_result) + value)
                return
            if current[-1] in operators:
                return  # Ignore if last was operator

        display_var.set(display_var.get() + value)

root = tk.Tk()
root.title("Calculator")

display_var = tk.StringVar()
display = tk.Entry(root, textvariable=display_var, font=('Arial', 20), bd=10, relief=tk.RIDGE, justify='right')
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky='we')

buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('÷', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('x', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('c', 4, 1), ('=', 4, 2), ('+', 4, 3),
]

for (text, row, col) in buttons:
    tk.Button(root, text=text, width=5, height=2, font=('Arial', 18),
              command=lambda val=text: on_click(val)).grid(row=row, column=col, padx=5, pady=5)

root.mainloop()
