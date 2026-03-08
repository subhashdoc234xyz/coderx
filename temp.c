// 3. Listen for INPUT REQUEST from the server
socket.on('input_required', () => {
    // 1. Ignore if we already stopped the program
    if (!isSocketRunning) return; 
    
    // 2. NEW FIX: Verify the code actually contains input commands!
    // This prevents GUI apps (like Tkinter) from triggering false input requests.
    const currentCode = editor.value;
    const hasInputCommands = /input\s*\(|scanf\s*\(|cin\s*>>|Scanner|\.readLine/i.test(currentCode);
    
    if (!hasInputCommands) {
        console.log("Ignored false input request (No input keywords found in code).");
        return; 
    }
    
    const modal = document.getElementById('inputModal');
    const inputField = document.getElementById('userProgramInput');
    const btn = document.getElementById('submitInputBtn');
    
    modal.style.display = 'block';
    inputField.value = '';
    inputField.focus();

    const send = () => {
        const val = inputField.value.trim();
        socket.emit('submit_input', val);
        modal.style.display = 'none';
        btn.removeEventListener('click', send);
    };
    
    // Ensure old listeners are cleared
    btn.replaceWith(btn.cloneNode(true));
    document.getElementById('submitInputBtn').addEventListener('click', send);
    
    inputField.onkeydown = (e) => { 
        if (e.key === 'Enter') { 
            e.preventDefault(); 
            document.getElementById('submitInputBtn').click(); 
        } 
    };
});