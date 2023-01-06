let websocket = new WebSocket("ws://127.0.0.1:8765/");
websocket.onopen = function (event) {
    websocket.send('Holla, server')
    console.log(event)
}
websocket.onmessage = data => {
    console.log(data.data)
}
websocket.onclose = event => {
    console.log(event)
}