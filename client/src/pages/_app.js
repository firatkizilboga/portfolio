import "bootstrap/dist/css/bootstrap.min.css";
import '/styles/globals.css'
import {Noto_Sans_Mono} from "@next/font/google"

const mono = Noto_Sans_Mono({subsets: ['latin'],weight: '700'})

export default function App({ Component, pageProps }) {
  return (<main className={mono.className}>
    <Component {...pageProps} />
  </main>)

}
