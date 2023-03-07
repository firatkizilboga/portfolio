export default function getServerUrl(path, is_websocket=false) {
    if (path){
        path = path;
    }
    else{
        path = "";
    }
    if (is_websocket){
        return "ws://127.0.0.1:8000/"+path;
    }
    return "http://127.0.0.1:8000/"+path;
}