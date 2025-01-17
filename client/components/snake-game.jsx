import { use, useEffect, useRef, useState } from "react";
import getServerUrl from "utils/get_server_url";
import scrollToSection from "utils/scroll_to_section";
import React from "react";


export default function SnakeGame() {

  const [playbacks, setPlaybacks] = useState([]);

  async function connectWebSocket() {
    return new Promise((resolve, reject) => {
      let url =getServerUrl("ws/evolve", true)
      const ws = new WebSocket(url);
  
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

  async function handleMessage(data) {
    const parsedData = JSON.parse(data);
    let new_playbacks = playbacks;

    for(let i = 0; i < parsedData.length; i++){
        new_playbacks.push(parsedData[i]);
      }
    setPlaybacks(new_playbacks);
    
    };


  const [isConnected, setIsConnected] = useState(false);

  const Node = () => {
    return(
      <div className=" hidden-layer d-flex w-100 align-items-center">
          <input type="number" className="node" name = "hidden_layer" placeholder="3" onChange={handleNodeChange}/>
          <div className="divider w-100"/>
      </div>
    )
  }
  
  const addNode = (event) => {
    setHiddenLayers([...hiddenLayers, <Node key = {hiddenLayers.length} />]);
  }

  const handleNodeChange = (event) => {
    let node = event.target;
    let value = node.value;
    if (value < 1) {
      const index = hiddenLayers.indexOf(node);
      if (index > -1) { // only splice array when item is found
        hiddenLayers.splice(index, 1); // 2nd parameter means remove one item only
      }
      setHiddenLayers([...hiddenLayers]);
    }
  }

  let width = 10;
  let height = 10;
  //create a matrix full of zeros
  let initial_frame = Array.from(Array(height), () => new Array(width).fill(0));
  let [frame, setFrame] = useState(initial_frame);
  let [frameId, setFrameId] = useState(0);
  let evolveButtonRef = useRef();
  let playRef = useRef();
  let loaderRef = useRef();

  const [hiddenLayers, setHiddenLayers] = useState([]);
  const addNodeButtonRef = useRef();

  useEffect(() => {
    if (hiddenLayers.length<3){
      addNodeButtonRef.current.classList.remove("d-none");
    } else {
      addNodeButtonRef.current.classList.add("d-none");
    }
  }, [hiddenLayers])
  
  

  const [isPlaying, setIsPlaying] = useState(false)
  let playHandleClick = (event) => {
    if (playbacks.length  == 1) {
      return;
    }else if (isPlaying) {
      setIsPlaying(false);
    }else{
      setIsPlaying(true);
      scrollToSection(event,"snake-game")
    }
  }
  

  useEffect(() => {
    evolveButtonRef.current.innerHTML = "Evolve";
    evolveButtonRef.current.classList.remove("disabled");
    if (isPlaying) {
      playRef.current.innerHTML = "Pause";
    }else{
      playRef.current.innerHTML = "Play";
    }
  }, [isPlaying])

  let evolveHandleClick = async () => {
    if (!isPlaying) {
      playRef.current.classList.add("disabled");
      evolveButtonRef.current.innerHTML = "Evolving...";
      evolveButtonRef.current.classList.add("disabled");
      loaderRef.current.classList.remove("invisible");
      
      let max_generations = document.getElementsByName("max_generations")[0].value;
      let population_size = document.getElementsByName("population_size")[0].value;
      let max_frames_training = document.getElementsByName("max_frames_training")[0].value;
      let max_frames_playback = document.getElementsByName("max_frames_playback")[0].value;
      let mutation_rate = document.getElementsByName("mutation_rate")[0].value;
      let hidden_layer_nodes = document.getElementsByName("hidden_layer");
      let hidden_layer_values = [];

      for (let i = 0; i < hidden_layer_nodes.length; i++) {
        hidden_layer_values.push(hidden_layer_nodes[i].value ? hidden_layer_nodes[i].value : '3');
      }
      
      if (max_generations == "") {
        max_generations = "20";
      }
      if (population_size == "") {
        population_size = "50";
      }
      if (max_frames_training == "") {
        max_frames_training = "200";
      }
      if (max_frames_playback == "") {
        max_frames_playback = "200";
      }
      if (mutation_rate == "") {
        mutation_rate = "0.3";
      }
      if (hidden_layer_values.length == 0) {
        hidden_layer_values = null;
      }
      let payload = { 
        "max_generations": max_generations,
        "population_size": population_size,
        "max_frames_training": max_frames_training,
        "max_frames_playback": max_frames_playback,
        "mutation_rate": mutation_rate,
      }
      if (hidden_layer_values) {
        payload["network_arch"] = hidden_layer_values;
      }
      setFrameId(0);

      let ws = null;    
      if (isConnected !== true) {
        const setupWebSocket = async () => {
          ws = await connectWebSocket();
          setIsConnected(true);
          ws.onmessage = async (event) =>{await handleMessage(event.data)};
        };
        setupWebSocket().then(
          async () => await ws.send(JSON.stringify(payload))
        );
      }
      evolveButtonRef.current.innerHTML = "Complete!";
      playRef.current.classList.remove("disabled");
      loaderRef.current.classList.add("invisible");
    }
  }
  const [playbackSpeed, setPlaybackSpeed] = useState(30);
  useEffect(() => {
    const interval = setInterval(() => {
      if (frameId < playbacks.length && isPlaying) {
        let current_frame = playbacks[frameId]
        setFrame(current_frame);
        setFrameId(frameId + 1);
                //sleep for 1 second
      }else{
        clearInterval(interval);
      }
    }, playbackSpeed);
    return () => {
      clearInterval(interval);
    };

}, [isPlaying,frameId,playbackSpeed,playbacks]);


  return (
    <div className="p-5 d-flex flex-wrap justify-content-evenly align-items-left">
        <div className="">
          <div className="cell-matrix" id = "snake-game">
            {frame.map((row, i) => {
              return(
                <div key={i} className="cell-row d-flex">{ 
                  row.map((cell, j) => {
                    return(
                      <div key={`${i},${j}`} 
                      className="cell"
                      style={
                        {
                          backgroundColor: cell == 1 ? '#A4AF69' : cell == 2 ? '#ee5622' : '#f8f7ff'
                        }
                      }>
                            {""}
                          </div>
                        )
                      })}
                </div>
                )})}
          </div>
          Playback Rate:
          <input type="number" min={10} placeholder="30" onChange={
            (event) => {
              setPlaybackSpeed(event.target.value);
            }
          }/>

          <br />
        </div>
        <div className="snake-game-options">
          <p>Neural Network Architecture</p>
          <div className="neural-net-options d-flex align-items-center">
            <div className=" input-layer d-flex w-100 align-items-center">
              <input type="number" className="node" value={9} name = "input_layer" disabled/>
              <div className="divider w-100"/>
            </div>
            {hiddenLayers}
            <div type="button" className="node text-center justify-content-center align-items-center d-flex" ref = {addNodeButtonRef} onClick={addNode}>+</div>
            <div className="divider w-100"/>
            <div className=" output-layer">
                <input type="number" className="node" value={3} name = "output_layer" disabled/>
            </div>
          </div>

            <div>
              <div className="m-2">
                <label htmlFor="max_frames_training">Maximum frame count in training</label><br />
                <input type="number" min={200} placeholder="type here min(200)" name = "max_frames_training"/>
              </div>
              <div className="m-2">
                <label htmlFor="max_frames_playback">Maximum frame count in playback</label><br />
                <input type="number" min={200}  placeholder="type here min(200)" name = "max_frames_playback"/>
              </div>
            </div>

            <div>
              <div className="m-2">
                <label htmlFor="max_generations">Number of generations</label><br />
                <input type="number" min={1} placeholder="type here" name = "max_generations"/>
              </div>
              <div className="m-2">
                <label htmlFor="population_size">Number of snakes in a generation</label><br />
                <input type="number" min={1}  placeholder="type here" name = "population_size"/>
              </div>
              <div className="m-2">
                <label htmlFor="mutation_rate">Mutation rate</label><br />
                <input type="number" step="0.1" placeholder="0,2" name="mutation_rate" min={0} max={1}/>
              </div>




            <p>Beware! The higher these values, <br />
              the longer it will take for the simulation to run.</p>
            </div>

            <div className="align-items-center d-flex justify-items-between w-100">
              <div>
                <button
                className=""
                ref={evolveButtonRef} 
                onClick={evolveHandleClick}
              >
                Evolve
                </button>
                <div className="loader invisible" ref={loaderRef}>
                  <div className="loaderBar"></div>
                </div>
              </div>
            
              
              <button ref={playRef}
                className="disabled red"
                onClick={playHandleClick}
                >
                Play
                </button>
            </div>
        </div>
    </div>
  );
}

