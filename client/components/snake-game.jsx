import { useEffect, useRef, useState } from "react";
import getServerUrl from "utils/get_server_url";


export function evolve(max_generations, population_size){
    //make a get request to the server endpoint /api/evolve
    var formdata = new FormData();
    formdata.append(max_generations, "20");
    formdata.append(population_size, "100");
    formdata.append("mutation_rate", "0.3");

    var requestOptions = {
        method: 'GET',
        body: formdata,
        redirect: 'follow'
      };
    
      
    let games = fetch(getServerUrl("/api/snake-game/evolve/"), requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));

    return games
}

function playback(playbackData){
    useEffect(() => {
    
        const initMatrix = [];
        for (let i = 0; i < matrixHeight; i++) {
          initMatrix[i] = [];
          for (let j = 0; j < matrixWidth; j++) {
            initMatrix[i][j] = 0;
          }
        }
        setMatrix(initMatrix);
      }, []);
    
      // iterate through playback data and update matrix
      useEffect(() => {
  
        let index = 0;
        const intervalId = setInterval(() => {
          if (index >= playbackData.length) {
            clearInterval(intervalId);
            return;
          }
    
          const frame = playbackData[index];
          const newMatrix = [];
          for (let i = 0; i < matrixHeight; i++) {
            newMatrix[i] = [];
            for (let j = 0; j < matrixWidth; j++) {
              newMatrix[i][j] = 0;
            }
          }
    
          for (let [x, y] of frame.snake) {
            newMatrix[y][x] = 1;
          }
          let [x, y] = frame.food;
          newMatrix[y][x] = 1;
    
          setMatrix(newMatrix);
          index++;
        }, 500);
    
        // clear matrix when component unmounts or playbackData changes
        return () => {
          clearInterval(intervalId);
          const clearMatrix = [];
          for (let i = 0; i < matrixHeight; i++) {
            clearMatrix[i] = [];
            for (let j = 0; j < matrixWidth; j++) {
              clearMatrix[i][j] = 0;
            }
          }
          setMatrix(clearMatrix);
        };
      }, [playbackData]);  
}

export default function SnakeGame() {
    const evolveBtn = useRef();
    let playbackData = [];

    const matrixWidth = 20;
    const matrixHeight = 20;
    const [matrix, setMatrix] = useState([]);

    // render matrix
    return (
      <div>

        <button
        onClick={(event) => {playbackData = evolve(20,100)}}>
            Evolve
        </button>        
        <button
        onClick={playback}>
            Playback
        </button>

        {matrix.map((row, i) => (
          <div key={i}>
            {row.map((cell, j) => (
              <span key={`${i}-${j}`} className={cell === 1 ? 'snake' : 'empty'}></span>
            ))}
          </div>
        ))}
      </div>
    );
  }