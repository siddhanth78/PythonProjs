const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.get('/', (req, res) => {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>OpenCV Stream</title>
      <script src="/socket.io/socket.io.js"></script>
      <style>
        body, html {
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
        }
        #videoCanvas {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }
      </style>
    </head>
    <body>
      <canvas id="videoCanvas"></canvas>
      <script>
        const socket = io();
        const canvas = document.getElementById('videoCanvas');
        const ctx = canvas.getContext('2d');
        let img = new Image();

        function resizeCanvas() {
          canvas.width = window.innerWidth;
          canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        socket.on('image', (imageData) => {
          img.onload = () => {
            const scale = Math.min(canvas.width / img.width, canvas.height / img.height);
            const x = (canvas.width / 2) - (img.width / 2) * scale;
            const y = (canvas.height / 2) - (img.height / 2) * scale;
            ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
          };
          img.src = 'data:image/jpeg;base64,' + imageData;
        });
      </script>
    </body>
    </html>
  `;
  res.send(html);
});

io.on('connection', (socket) => {
  console.log('A client connected');

  const pythonPath = path.join(__dirname, 'pose_test.py');
  const pythonProcess = spawn('python', [pythonPath]);

  pythonProcess.stdout.on('data', (data) => {
    socket.emit('image', data.toString().trim());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
    pythonProcess.kill();
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});