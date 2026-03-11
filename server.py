from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app) 

# Using the latest fast model
TARGET_MODEL = 'gemini-2.5-flash'

# --- API KEY ROTATION SETUP ---
API_KEYS = [
    
    # ... add all your keys here
]

# Global tracker for which key we are currently using
CURRENT_KEY_INDEX = 0

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
1. Track variables in 'memory_state'.
2. ACCURACY: Your trace MUST perfectly match the program output provided.
3. STUDENT-FRIENDLY VISUALS: Do NOT show the final invisible increment of a loop counter. 
4. VARIABLE SCOPE: Remove variables from 'memory_state' once they go out of scope.
5. COMPRESSION: If a loop repeats more than 3 times, trace the first 2 iterations, skip the middle, and trace the final iteration to save space.
Schema: [{"step": 1, "action": "highlight", "line": 1, "code_text": "code", "explanation": "explain", "memory_state": {"var": 1}}]
"""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    def generate():
        global CURRENT_KEY_INDEX
        
        for _ in range(len(API_KEYS)):
            try:
                genai.configure(api_key=API_KEYS[CURRENT_KEY_INDEX])
                model = genai.GenerativeModel(TARGET_MODEL)
                
                full_prompt = f"System Instructions:\n{CHAT_PROMPT}\n\nUser Request:\n{user_message}"
                stream = model.generate_content(full_prompt, stream=True)
                
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
                return 
                
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "exhausted" in error_msg or "quota" in error_msg:
                    print(f"⚠️ Key {CURRENT_KEY_INDEX + 1} exhausted. Switching to next key...")
                    CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(API_KEYS)
                    continue 
                else:
                    yield f"\n[System Error]: {str(e)}"
                    return
        
        yield "\n[System Error]: All API keys have reached their free tier limits!"

    return Response(generate(), mimetype='text/plain')


@app.route('/generate_trace', methods=['POST'])
def generate_trace():
    global CURRENT_KEY_INDEX
    
    data = request.json
    user_code = data.get('code', '')
    user_inputs = data.get('inputs', '') 
    program_output = data.get('output', '')
    
    prompt_message = f"System Instructions:\n{TRACE_PROMPT}\n\nGenerate trace for the following code:\n{user_code}"
    if user_inputs or program_output:
        prompt_message += "\n\n--- EXECUTION CONTEXT ---"
        if user_inputs: prompt_message += f"\nINPUTS: {user_inputs}"
        if program_output: prompt_message += f"\nRESULT: {program_output}"

    for _ in range(len(API_KEYS)):
        try:
            genai.configure(api_key=API_KEYS[CURRENT_KEY_INDEX])
            
            # FIXED: We now force Gemini to return strict JSON formatting
            model = genai.GenerativeModel(
                model_name=TARGET_MODEL,
                generation_config={"response_mime_type": "application/json"}
            )
            
            response = model.generate_content(prompt_message)
            raw_output = response.text
            
            try:
                # Load the guaranteed JSON string
                return jsonify(json.loads(raw_output)), 200
            except json.JSONDecodeError:
                return jsonify([{"step": 1, "line": 1, "explanation": "Logic trace failed to format.", "memory_state": {}}]), 200

        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "exhausted" in error_msg or "quota" in error_msg:
                print(f"⚠️ Key {CURRENT_KEY_INDEX + 1} exhausted for trace. Switching to next key...")
                CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(API_KEYS)
                continue 
            else:
                # Print exact error to the terminal so we can see what went wrong
                print(f"❌ Backend Trace Error: {str(e)}") 
                return jsonify({"error": str(e)}), 500

    return jsonify({"error": "All API keys have reached their free tier limits!"}), 500


if __name__ == '__main__':
    print(f"⚡ Light Agent running with {TARGET_MODEL} on http://localhost:5001")
    app.run(port=5001, debug=True)