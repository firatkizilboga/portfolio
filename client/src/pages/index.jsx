//import snake game
import SnakeGame from '/components/snake-game';
import Header from '/components/layout/header';


export default function Index() {
    return (
        <div> 
            <Header />
            <SnakeGame />
        </div>
    );
}
