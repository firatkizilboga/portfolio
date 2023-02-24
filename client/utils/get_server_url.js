export default function getServerUrl(path) {
    if (path){
        path = path;
    }
    else{
        path = "";
    }

    return "http://firatkizilboga.com:8000/"+path;
}