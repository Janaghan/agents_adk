def calculate_math(expression: str) -> str:
    """Evaluates mathematical expressions."""
    try:
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error: {str(e)}"
