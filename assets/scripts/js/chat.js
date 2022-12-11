curDiv = document.querySelector('.chat-box')
dataDiv = document.querySelectorAll('.chat-rows')
// document.onload =curDiv.focus()

genCover = document.querySelector('#gen-cover')

genCover.lastElementChild.scrollIntoView()

window.addEventListener('load', function(event) { genCover.lastElementChild.scrollIntoView()
})
toastCover = document.querySelector('#toast-cover')

msgtxt = document.querySelector('#new-msg')

async function send_msg(event, xlogged, xchatid) {
    if (msgtxt.value==''){
        toastCover.style.display = 'flex'
        toast.innerHTML = 'Message is empty'
        let animation = anime({
            targets: "#toast-cover",
            keyframes: [
                {opacity: 1},
                {opacity: .75},
                {opacity: .5},
                {opacity: .25},
                {opacity: 0}
            ],
            duration: 4000,
            easing: "linear"
        });
        setTimeout(function() {
            toastCover.style.display = 'none'
        }, 4500);
    }
    else {
        msgData = {
            'msg_txt' : msgtxt.value,
            'chat_id': xchatid
        }
        parsedData = JSON.stringify(msgData)
        
        let postMsg = await fetch(`sendmsg`, {
                method: "POST",
                redirect: "follow",
                headers: {
                    "Content-Type": ("application/json")
                    },
                body: parsedData,
            }
        )
        res = await postMsg
        console.log(res.status)
        if (res.status=='200'){
            getLastChat(xchatid)
        } else {
            toastCover.style.display = 'flex'
            toast.innerHTML = 'An error occurred!'
            let animation = anime({
                targets: "#toast-cover",
                keyframes: [
                    {opacity: 1},
                    {opacity: .5},
                    {opacity: 0}
                ],
                duration: 2000,
                easing: "linear"
            });
            setTimeout(function() {
                toastCover.style.display = 'none'
            }, 2500);
        }
        msgtxt.value = ''
    }
}

async function getLastChat(xchatid) {
    let fetchChat = await fetch(`get_chat?chatid=${xchatid}`)
    res = await fetchChat
    if (res.status==200) {
        data = await res.json()
        console.log(data['user'])
    }
    else {
        toastCover.style.display = 'flex'
        toast.innerHTML = 'Unable to fetch data'
        let animation = anime({
            targets: "#toast-cover",
            keyframes: [
                {opacity: 1},
                {opacity: .5},
                {opacity: 0}
            ],
            duration: 2000,
            easing: "linear"
        });
        setTimeout(function() {
            toastCover.style.display = 'none'
        }, 2500);
    }
}
setInterval(getLastChat(location.search.slice(-1)), 10000)

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