const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const NodeWebcam = require('node-webcam');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const screenx = 640;
const screeny = 480;

// Set up webcam
const Webcam = NodeWebcam.create({
  width: screenx,
  height: screeny,
  quality: 100,
  saveShots: false,
  output: "jpeg",
  device: false,
  callbackReturn: "buffer"
});

function captureFrame() {
  return new Promise((resolve, reject) => {
    Webcam.capture("frame", (err, data) => {
      if (err) reject(err);
      else resolve(data);
    });
  });
}

async function sendFrame() {
  try {
    const imageBuffer = await captureFrame();
    const base64Image = `data:image/jpeg;base64,${imageBuffer.toString('base64')}`;
    io.emit('frame', base64Image);
  } catch (error) {
    console.error('Error capturing frame:', error);
  }
  setTimeout(sendFrame, 33); // Approximately 30 fps
}

// Serve static files
app.use(express.static('public'));

// Serve the main page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Socket.IO connection
io.on('connection', (socket) => {
  console.log('A user connected');
  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  sendFrame(); // Start sending frames when the server starts
});