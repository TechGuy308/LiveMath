from sympy import sympify, simplify, solve, symbols
import latex2sympy2
import re
import ollama
import requests
import json
from langchain_ollama import OllamaLLM

model = OllamaLLM(model="phi3")
#from sympy.parsing.latex import parse_latex

#junk_patterns = [r"!", r",", r";", r"enspace"]

def clean_latex(detected_latex):
    latex = str(detected_latex)

    # Remove double slashes
    latex = latex.replace("\\\\", "")

    # Remove common junk
    latex = re.sub(r"\\left|\\right", "", latex)
    latex = re.sub(r"\\,", "", latex)
    latex = re.sub(r"\\;", "", latex)
    latex = re.sub(r"\\!", "", latex)

    # Fix subscripts like v_{0} → v0
    latex = re.sub(r"_(\{)?(\w+)(\})?", r"\2", latex)

    # Remove spaces
    latex = latex.replace(" ", "")

    try:
        cleaned = latex
        expr = latex2sympy2.latex2sympy(cleaned)
        return expr, cleaned
    except Exception as e:
        return detected_latex
        # If the LaTeX is too messy for the parser, 
        # fall back to a simple text comparison for now
        print(f"Parser Error: {e}")


def analyze(question, answer):
    url = "http://localhost:11434/api/generate"
    
    prompt_text = f"Problem: {question}\nFinal Answer: {answer}"
    system_instruction = "You are a math tutor API. Return ONLY JSON with 'steps' containing 'math' and 'hint'. No talk."

    data = {
        "model": "llama3", # or "mistral"
        "prompt": f"{system_instruction}\n\n{prompt_text}",
        "stream": False,
        "format": "json" # This is a secret weapon in Ollama to force JSON
    }

    response = requests.post(url, json=data)
    
    # Parse the response
    result = response.json()
    print (json.loads(result['response']))

