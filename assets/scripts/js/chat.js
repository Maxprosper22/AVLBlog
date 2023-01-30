curDiv = document.querySelector('.chat-box')
dataDiv = document.querySelectorAll('.chat-rows')

genCover = document.querySelector('#gen-cover')

genCover.lastElementChild.scrollIntoView()

window.addEventListener('load', function(event) { genCover.lastElementChild.scrollIntoView()
})
toastCover = document.querySelector('#toast-cover')

maxpee = document.getElementsByTagName('maxpee')

async function main() {
    pyodide = await loadPyodide()
    await pyodide.loadPackage("micropip")
    micropip = pyodide.pyimport("micropip")
    micropip.install(location.origin+'/static/scripts/libraries/pyodide/websockets-10.4-cp311-cp311-linux_aarch64.whl')
    // pyodide.loadPackage('websockets')
    maxpee[0].style.display = 'none'
    pyodide.runPython(maxpee[0].innerHTML)
    // return pyodide, micropip
}
// main()

msgtxt = document.querySelector('#new-msg')

let socket = new WebSocket('ws://127.0.0.1:8765')

async function send_msg(event, xlogged, xchatid) {
        if (msgtxt.value==''){
            toastCover.style.display = 'flex'
            toast.innerHTML = 'Message is empty'
            let animation = anime({targets: "#toast-cover", keyframes: [{opacity: 1}, {opacity: .75}, {opacity: .5},{opacity: .25}, {opacity: 0}],
                duration: 4000,
                easing: "linear"
            });
            setTimeout(function() {toastCover.style.display = 'none'}, 4500);
        }
        else {
            msgData = {
                'sender': xlogged,
                'msg_txt' : msgtxt.value,
                'chat_id': xchatid,
                'token': '',
            }
            parsedData = JSON.stringify(msgData)
            // console.log(parsedData)
            // console.log(socket)
            socket.addEventListener('onopen', () => {
                socket.send(parsedData)
            })
            msgtxt.value = ''
        }
    // })
}
socket.addEventListener('message', ({data}) => {
    data = JSON.parse(data)
    alert('A message has arrived!')
    console.log(event.data)
    chatRow = document.createElement('DIV')
    chatRow.setAttribute('class', 'chat-rows')
    
    chatBox = document.createElement('DIV')
    chatBox.className = "chat-box chat-mate"
    
    chatMsg = document.createElement('P')
    chatMsg.innerHTML = data['msg_txt']
    chatMsg.className = 'chat-item'
    
    chatDate = document.createElement('P')
    chatDate.innerHTML = data['chat_id']
    chatDate.className = 'chat-item msg-date'
    
    chatBox.appendChild(chatMsg)
    chatBox.appendChild(chatDate)
    chatRow.appendChild(chatBox)
    genCover.appendChild(chatRow)
})

eContainer = document.getElementById('emoji-container')

load_emoji(eContainer, emojiList)


async function showEmo(event) {
    if (eContainer.style.display=='none') {
        genCover.style.height = '34vh'
        eContainer.style.display = 'flex'
        eContainer.style.height = '16.5em'
        eContainer.style.position = 'relative'
        eContainer.style.bottom = 0
    } else {
        eContainer.style.display = 'none'
        // genCover.style.bottom = '3.5em'
        genCover.style.height = '68vh'
    }
}

async function closeEmo(event) {
    if (eContainer.style.display != 'none') {
        eContainer.style.display = 'none'
        genCover.style.height = '39.5vh'
    }
}

async function closeTxt(event) {
    genCover.style.height = '68vh'
}
txtArea = document.querySelector('#new-msg')

async function getEmojis(emjContainer) {
    for (elt=0; elt < emjContainer.children.length; elt++) {
        targetElt = document.querySelector('#new-msg')
        emjContainer.children[elt].addEventListener('click', function(event) {
            targetElt.value += event.target.innerHTML
        })
    }
}

getEmojis(eContainer)

async function closeTxtArea(event) {
    if (txtArea.style.active) {
        txtArea.blur()
        genCover.style.height = '68vh'
    } 
    else if (eContainer.style.display != 'none') {
        eContainer.style.display = 'none'
    }
}

async function insertSym(event) {
    keyName = event.key
    if (event.key == 'enter') {
        console.log(event.key)
        alert(event.key)
    }
}
msgtxt.addEventListener('keypress', insertSym)