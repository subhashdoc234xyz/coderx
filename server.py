from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import ollama
import json

app = Flask(__name__)
CORS(app) 

# Switched to the Ollama Cloud model
TARGET_MODEL = 'gpt-oss:20b-cloud'

# --- 1. PROMPT FOR THE CHAT BUBBLE ---
CHAT_PROMPT = """
You are a dedicated coding engine.
RULES:
1. Write COMPLETE code.
2. For Java: You MUST use 'public class Main'.
3. For Java: You MUST include 'public static void main(String[] args)'.
4. Output Markdown blocks (```java).
5. No conversational filler.
"""

# --- 2. PROMPT FOR THE ANIMATION TRACE ---
TRACE_PROMPT = """
You are the backend execution trace engine for 'CodeViz'.
Simulate the execution of the code step-by-step and output a valid JSON array.
RULES:
1. Output ONLY pure, valid JSON. NO markdown formatting.
2. Track variables in 'memory_state'.
3. ACCURACY: Your trace MUST perfectly match the program output provided.
4. STUDENT-FRIENDLY VISUALS: Do NOT show the final invisible increment of a loop counter. 
5. VARIABLE SCOPE: Remove variables from 'memory_state' once they go out of scope.
Schema: [{"step": 1, "action": "highlight", "line": 1, "code_text": "code", "explanation": "explain", "memory_state": {"var": 1}}]
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    def generate():
        try:
            stream = ollama.chat(
                model=TARGET_MODEL, 
                messages=[
                    {'role': 'system', 'content': CHAT_PROMPT},
                    {'role': 'user', 'content': user_message},
                ],
                stream=True,
            )
            for chunk in stream:
                content = chunk['message']['content']
                if content:
                    yield content
        except Exception as e:
            yield f"\n[System Error]: {str(e)}"

    return Response(generate(), mimetype='text/plain')

@app.route('/generate_trace', methods=['POST'])
def generate_trace():
    data = request.json
    user_code = data.get('code', '')
    user_inputs = data.get('inputs', '') 
    program_output = data.get('output', '')
    
    prompt_message = f"Generate trace for the following code:\n{user_code}"
    if user_inputs or program_output:
        prompt_message += "\n\n--- EXECUTION CONTEXT ---"
        if user_inputs: prompt_message += f"\nINPUTS: {user_inputs}"
        if program_output: prompt_message += f"\nRESULT: {program_output}"

    try:
        response = ollama.chat(
            model=TARGET_MODEL, 
            messages=[
                {'role': 'system', 'content': TRACE_PROMPT},
                {'role': 'user', 'content': prompt_message}, 
            ],
            stream=False, 
        )
        
        raw_output = response['message']['content']
        clean_output = raw_output.replace("```json", "").replace("```", "").strip()

        try:
            return jsonify(json.loads(clean_output)), 200
        except json.JSONDecodeError:
            # Fallback for small models that might fail JSON formatting
            return jsonify([{"step": 1, "line": 1, "explanation": "Logic trace failed to format.", "memory_state": {}}]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"⚡ Light Agent running with {TARGET_MODEL} on http://localhost:5001")
    app.run(port=5001, debug=True)