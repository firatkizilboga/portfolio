import React from 'react';
import Link from 'next/link'



export default function Header() {
    return (
        <div className='background-dark'>
            <div className='d-flex align-items-center justify-content-between flex-wrap snakegame-grid'>
                    <Link 
                    href="/"
                        ><h1>
                            &gt;&gt;&gt; Our.Portfolio(&#128293;)
                        </h1>
                    </Link>

                <div className='d-flex align-items-center justify-content-between'>
                    <Link 
                    className='mx-3'
                    href="/snake-game">
                        Snake Game
                    </Link>

                    <Link href="/about"
                    className='mx-3'
                    >
                        About
                    </Link>
                </div>
            </div>

            <div className='divider'></div>
        </div>
    );
}
