console.log(document.querySelector('.chat-box').children)
curDiv = document.querySelector('.chat-box')
dataDiv = document.querySelectorAll('.chat-rows')
document.onload =curDiv.focus()

genCover = document.querySelector('#gen-cover')

genCover.lastElementChild.scrollIntoView()

window.addEventListener('load', function(event) { genCover.lastElementChild.scrollIntoView()
})
            
async function send_msg(event, xlogged, xchatmate, xchat) {
    // console.log(xchatdata)
    msgtxt = event.target.parentElement.children[0]
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
        msgData = {'msg_txt' : msgtxt.value, 'contact': xchatmate, 'chat_id': location.search.slice(-1)}
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
        if (res.status=='200'){
            data = await res.json()
            console.log(data['user'])
            
            if (data.user==xlogged) {
                const topChatElt = document.createElement('div')
                topChatElt.className = 'chat-rows'
                
                const subChatElt = document.createElement('div')
                subChatElt.setAttribute('class', ['chat-box', 'user-chat'])
                // subChatElt.classList.add('user-chat')
                
                
                const msgP = document.createElement('p')
                msgP.innerHTML == data['msg_txt']
                msgP.setAttribute('classList', 'chat-item')
                
                const dateP = document.createElement('p')
                dateP.innerHTML == data['date']
                dateP.classList.add('chat-item')
                dateP.classList.add('msg-date')
                
                subChatElt.appendChild(msgP)
                subChatElt.appendChild(dateP)
                topChatElt.appendChild(subChatElt)
                genCover.appendChild(topChatElt)
                
                // location.reload()
                subChatElt.scrollIntoView()
            } else {
                const topChatElt = document.createElement('div')
                topChatElt.classList.add('chat-rows')
                genCover.appendChild(topChatElt)
                
                const subChatElt = document.createElement('div')
                subChatElt.classList.add('chat-box')
                subChatElt.classList.add('chatmate')
                
                topChatElt.appendChild(subChatElt)
                
                const msgP = document.createElement('p')
                msgP.innerHTML == data['msg_txt']
                msgP.className = 'chat-item'
                
                const dateP = document.createElement('p')
                dateP.className = 'chat-item'
                dateP.classList.add('msg-date')
                dateP.innerHTML == data['date']
                
                subChatElt.appendChild(msgP)
                subChatElt.appendChild(dateP)
                
                topChatElt.scrollIntoView()
            }
            
            // console.log(xchatdata())
        } else {
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

// sendBtn = document.querySelector('.sendmsg')
// sendBtn.addEventListener('click', send_msg)