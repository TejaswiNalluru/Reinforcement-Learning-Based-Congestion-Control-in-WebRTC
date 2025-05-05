const socket = io();
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
let pc, localStream, sender;

(async () => {
  localStream = await navigator.mediaDevices.getUserMedia({ video: true });
  localVideo.srcObject = localStream;

  pc = new RTCPeerConnection();
  localStream.getTracks().forEach(track => {
    sender = pc.addTrack(track, localStream);
  });

  pc.onicecandidate = e => {
    if (e.candidate) socket.emit('candidate', e.candidate);
  };

  pc.ontrack = e => {
    remoteVideo.srcObject = e.streams[0];
  };

  socket.on('offer', async (data) => {
    await pc.setRemoteDescription(new RTCSessionDescription(data));
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    socket.emit('answer', answer);
  });

  socket.on('answer', async (data) => {
    await pc.setRemoteDescription(new RTCSessionDescription(data));
  });

  socket.on('candidate', async (data) => {
    try {
      await pc.addIceCandidate(new RTCIceCandidate(data));
    } catch (err) { console.error(err); }
  });


  socket.on('rl-action', async ({ bitrate }) => {
    if (sender) {
      try {
        const params = sender.getParameters();
        if (!params.encodings || params.encodings.length === 0) {
          params.encodings = [{}]; 
        }
        params.encodings[0].maxBitrate = bitrate * 1000; // in bits
        await sender.setParameters(params);
        console.log(" Bitrate set to:", bitrate);
      } catch(err){
      }
    }
  });
  

  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  socket.emit('offer', offer);

  setInterval(async () => {
    const stats = await pc.getStats();
    let outbound, inbound, remote;
  
    stats.forEach(report => {
      if (report.type === 'outbound-rtp' && report.kind === 'video') outbound = report;
      if (report.type === 'inbound-rtp' && report.kind === 'video') inbound = report;
      if (report.type === 'remote-inbound-rtp' && report.kind === 'video') remote = report;
    });
  
    const data = {
      bitrate: outbound ? outbound.bytesSent : 0,
      packetsLost: inbound ? inbound.packetsLost : 0,
      roundTripTime: remote ? remote.roundTripTime : 0,
      jitter: inbound ? inbound.jitter : 0
    };
  
    socket.emit('stats', data);
  }, 1000);
  
})();
