import { use, useEffect, useRef, useState } from "react";
import getServerUrl from "utils/get_server_url";

export async function evolve(max_generations, population_size, max_frames_training, max_frames_playback){
    //make a get request to the server endpoint /api/evolve
    var formdata = new FormData();
    formdata.append("max_generations", max_generations);
    formdata.append("population_size", population_size);
    formdata.append("max_frames_training", max_frames_training);
    formdata.append("max_frames_playback", max_frames_playback);
    
    formdata.append("mutation_rate", "0.3");


    var requestOptions = {
        method: 'POST',
        body: formdata,
        redirect: 'follow'
      };
    
    let games = fetch(getServerUrl("api/snake-game/evolve/"), requestOptions)
    .then(response => response.json())
    .then(result => result)
    .catch(error => console.log('error', error));
    //returns a list of games
    console.log(games)
    return games
};
export default function SnakeGame() {

  let width = 10;
  let height = 10;

  let [frames, setFrames] = useState([]);
  //create a matrix full of zeros
  let initial_frame = Array.from(Array(height), () => new Array(width).fill(0));
  let [frame, setFrame] = useState(initial_frame);
  let [frameId, setFrameId] = useState(0);
  let evolveButtonRef = useRef();
  let playRef = useRef();
  let loaderRef = useRef();

  const [isPlaying, setIsPlaying] = useState(false)
  let playHandleClick = () => {
    if (frames.length  == 1) {
      return;
    }else if (isPlaying) {
      setIsPlaying(false);
    }else{
      setIsPlaying(true);
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

      setFrameId(0);
      await evolve(max_generations, population_size, max_frames_training, max_frames_playback).then((inc_frames) => {
        setFrames(inc_frames);
      });
      evolveButtonRef.current.innerHTML = "Complete!";
      playRef.current.classList.remove("disabled");
      loaderRef.current.classList.add("invisible");
    }
  }
  
  useEffect(() => {
      const interval = setInterval(() => {
        if (frameId < frames.length && isPlaying) {
          let current_frame = frames[frameId]
          setFrame(current_frame);
          setFrameId(frameId+1);
          //sleep for 1 second
        }else{
          clearInterval(interval);
        }
      }, 15);
      return () => {
        clearInterval(interval);
      };

  }, [isPlaying, frameId]);

  return (
    <div className="p-5 d-flex flex-wrap justify-content-evenly align-items-left">
        <div className="">
          <div className="cell-matrix">
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
          <br />
        </div>
        <div className="snake-game-options d-flex flex-wrap">
          <div>
            <div className="m-2">
              <label htmlFor="max_generations">Maximum frame count in training</label><br />
              <input type="number" min={200} placeholder="type here min(200)" name = "max_frames_training"/>
            </div>

            <div className="m-2">
              <label htmlFor="max_generations">Maximum frame count in playback</label><br />
              <input type="number" min={200}  placeholder="type here min(200)" name = "max_frames_playback"/>
            </div>
          </div>

            <div>
              <div className="m-2">
                <label htmlFor="max_generations">Number of generations</label><br />
                <input type="number" min={1} placeholder="type here" name = "max_generations"/>
              </div>
              <div className="m-2">
                <label htmlFor="max_generations">Number of snakes in a generation</label><br />
                <input type="number" min={1}  placeholder="type here" name = "population_size"/>
              </div>
              <div className="m-2">
                <label htmlFor="max_generations">Mutation rate</label><br />
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
                <div class="loader invisible" ref={loaderRef}>
                  <div class="loaderBar"></div>
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

