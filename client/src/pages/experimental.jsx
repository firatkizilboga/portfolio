import { useState, useEffect } from "react";



export default function index() {
  async function connectWebSocket() {
    return new Promise((resolve, reject) => {
      const ws = new WebSocket("ws://127.0.0.1:8000/ws/evolve");
  
      ws.onopen = () => {
        console.log("WebSocket connection opened");
        resolve(ws);
      };
  
      ws.onerror = (event) => {
        console.error("WebSocket error:", event);
        reject(event);
      };
    });
  }
  const [frames, setFrames] = useState([]);
  async function handleMessage(data) {
    const parsedData = JSON.parse(data);
    setFrames(data);
  };

  const [isConnected, setIsConnected] = useState(false);
  useEffect(() => {
    let ws = null;
    
    if (isConnected !== true) {
      const setupWebSocket = async () => {
        ws = await connectWebSocket();
        setIsConnected(true);
        ws.onmessage = async (event) =>{ await handleMessage(event.data)};
      };
      setupWebSocket().then(
        async () => await ws.send(JSON.stringify({ population_size: 100,
          mutation_rate: 0.1, 
          max_generations: 30,
          max_frames_playback: 600,
          max_frames_training: 600, }))
      );
    }
    
  });

  return (
    <div>
      <h1>Experimental</h1>
      <p>Here you can run experiments with the genetic algorithm.</p>
      {frames}
    </div>
  );
}
