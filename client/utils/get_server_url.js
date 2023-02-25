export default function getServerUrl(path) {
    if (path){
        path = path;
    }
    else{
        path = "";
    }

    return "http://127.0.0.1:8000/"+path;
}