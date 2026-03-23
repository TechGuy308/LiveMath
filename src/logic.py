from sympy import sympify, simplify, solve, symbols
import latex2sympy2
import re
import ollama
import requests
import json
#from sympy.parsing.latex import parse_latex

#junk_patterns = [r"!", r",", r";", r"enspace"]

def solve_prob(detected_latex):
    try:
        '''
        for pattern in junk_patterns:
            clean_latex = re.sub(pattern,"", rf"{detected_latex}")
            clean_latex = re.sub(r"d_\{?x\}?", "dx", clean_latex, flags=re.IGNORECASE)
        '''
        
        clean_latex= str(detected_latex).replace(r"\\","")  
        solution = latex2sympy2.latex2sympy(rf"{clean_latex}")
        #detected_latex.replace(r"\begin{matrix}", "").replace(r"\end{matrix}", "")
        #expr=parse_latex(f"{clean_latex}")
        #equations = [eq.strip() for eq in expr.split(r"\\")]
        print(clean_latex)
        print(solution)
        return [clean_latex,solution]
    except Exception as e:
        # If the LaTeX is too messy for the parser, 
        # fall back to a simple text comparison for now
        print(f"Parser Error: {e}")

ques,sol = solve_prob()
def get_steps(latex, answer):
    url = "http://localhost:11434/api/generate"
    
    prompt_text = f"Problem: {latex}\nFinal Answer: {answer}"
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

get_steps(ques, sol)