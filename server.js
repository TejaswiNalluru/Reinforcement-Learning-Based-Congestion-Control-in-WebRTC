const express = require('express');
const http = require('http');
const socketIO = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

app.use(express.static('public'));

io.on('connection', socket => {
  socket.on('offer', data => socket.broadcast.emit('offer', data));
  socket.on('answer', data => socket.broadcast.emit('answer', data));
  socket.on('candidate', data => socket.broadcast.emit('candidate', data));
  socket.on('stats', data => socket.broadcast.emit('stats', data));
  socket.on('rl-action', data => socket.broadcast.emit('rl-action', data));
});

server.listen(3000, () => console.log('Server running at http://localhost:3000'));
