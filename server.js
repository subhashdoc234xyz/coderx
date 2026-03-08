const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const { spawn } = require('child_process');
const fs = require('fs');
const cors = require('cors');

const app = express();
app.use(cors());

// --- ADDED THIS LINE ---
app.use(express.static('public')); 
// -----------------------

const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

const PORT = 5000;

io.on('connection', (socket) => {
    let process = null;
    let silenceTimer = null;

    const startSilenceDetection = () => {
        if (silenceTimer) clearTimeout(silenceTimer);
        silenceTimer = setTimeout(() => {
            if (process && process.exitCode === null) {
                socket.emit('input_required');
            }
        }, 150); // 150ms of silence = program is waiting for input
    };

    socket.on('run_code', ({ code, language }) => {
        const filename = language === 'python' ? 'temp.py' : language === 'java' ? 'Main.java' : 'temp.c';
        fs.writeFileSync(filename, code);

        let command, args;
        if (language === 'python') {
            command = 'python'; args = ['-u', filename];
        } else if (language === 'java') {
            require('child_process').spawnSync('javac', [filename]);
            command = 'java'; args = ['Main'];
        } else {
            // Windows GCC Compilation
            const compileResult = require('child_process').spawnSync('gcc', [filename, '-o', 'temp.exe']);
            if (compileResult.stderr && compileResult.stderr.length > 0) {
                socket.emit('output', compileResult.stderr.toString());
            }
            command = 'temp.exe';
            args = [];
        }

        try {
            process = spawn(command, args, { shell: true });

            process.stdout.on('data', (data) => {
                socket.emit('output', data.toString());
                startSilenceDetection(); 
            });

            process.stderr.on('data', (data) => {
                socket.emit('output', data.toString());
            });

            process.on('close', (code) => {
                if (silenceTimer) clearTimeout(silenceTimer);
                socket.emit('finished', code);
                process = null;
            });

            startSilenceDetection();
        } catch (e) {
            socket.emit('output', "\nFailed to run process.");
        }
    });

    socket.on('submit_input', (input) => {
        if (process) {
            process.stdin.write(input + "\n");
            socket.emit('output', input + "\n"); // Show what user typed
            startSilenceDetection(); // Restart wait timer for loops
        }
    });

    socket.on('disconnect', () => {
        if (process) process.kill();
    });
});

server.listen(PORT, () => console.log(`Compiler Server running on port ${PORT}`));