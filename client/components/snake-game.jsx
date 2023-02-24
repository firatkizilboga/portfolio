import { use, useEffect, useRef, useState } from "react";
import getServerUrl from "utils/get_server_url";

export async function evolve(max_generations, population_size){
    //make a get request to the server endpoint /api/evolve
    var formdata = new FormData();
    formdata.append("max_generations", max_generations);
    formdata.append("population_size", population_size);
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

  let evolveHandleClick = async () => {
    playRef.current.classList.add("disabled");
      let max_generations = document.getElementsByName("max_generations")[0].value;
      let population_size = document.getElementsByName("population_size")[0].value;
      await evolve(max_generations, population_size).then((inc_frames) => {
        setFrames(inc_frames);
      });
      playRef.current.classList.remove("disabled");
  }

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
    if (isPlaying) {
      playRef.current.innerHTML = "Pause";
    }else{
      playRef.current.innerHTML = "Play";
    }
  }, [isPlaying])
  



  useEffect(() => {
      const interval = setInterval(() => {
        if (frameId < frames.length && isPlaying) {
          let current_frame = frames[frameId]
          setFrame(current_frame);
          setFrameId(frameId+1);
          evolveButtonRef.current.innerHTML = `Evolve ${frameId}`;
          //sleep for 1 second
        }else{
          clearInterval(interval);
        }
      }, 30);
      return () => clearInterval(interval);

  }, [isPlaying, frameId]);

  return (
    <div className="p-5">
      <div className="align-items-center justify-content-evenly d-flex">
        <div className="cell-matrix">
          {frame.map((row, i) => {
            return(
              <div key={i} className="cell-row d-flex">{ 
                    row.map((cell, j) => {
                      return(
                        <div key={`${i},${j}`} style={
                          {
                            width: `40px`,
                            height: `40px`,
                            //conditional background color
                            backgroundColor: cell == 1 ? 'green' : cell == 2 ? 'red' : 'white'
                          }
                        }>
                          {""}
                        </div>
                      )
                    })}
              </div>
              )})}

        </div>
        <div className="">
            <div className="mb-2">
              <label htmlFor="max_generations">Number of generations</label><br />
              <input type="number" min={20} name = "max_generations"/>
            </div>
            <div className="mb-2">
              <label htmlFor="max_generations">Number of snakes in a generation</label><br />
              <input type="number" min={40} name = "population_size"/>
            </div>
            <div className="align-items-center d-flex justify-items-between w-100">
            <button
              className="btn btn-primary"
              ref={evolveButtonRef} 
              onClick={evolveHandleClick}
            >
              Evolve
              </button>
              <button ref={playRef}
              className="btn btn-danger disabled"
              onClick={playHandleClick}
              >
              Play
              </button>

            </div>
          </div>
        </div>
    </div>
  );
}

