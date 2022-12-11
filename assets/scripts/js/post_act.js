async function viewPost(event, xpostid) {
    location = `/posts/post/${xpostid}`
}

async function popmenu(event, xviewer, xpostid) {
    console.log(event.target.parentElement.nextElementSibling)
    event.target.parentElement.nextElementSibling.style.display = 'flex'
}

async function openImage(event) {
    toucDiv = document.querySelector('.touch-scroll')
    toucDiv.appendChild(event.target)
    toucDiv.style.display = 'flex'
}
async function closepop(event) {
    event.stopPropagation()
    console.log(event.target)
    event.target.style.display = 'none'
    console.log(event.target)
}
async function poplinks(event) {
    event.stopPropagation()
    console.log(event.target)
}
popItems = document.querySelectorAll('.pop-items')
for (pItem=0; pItem<popItems.length; pItem++) {
    popItems[pItem].addEventListener('click', poplinks)
}

async function likepost(event, xviewer, xpostid) {
    if (xviewer != 'Guest') {
        likeData = {
            'viewer': xviewer,
            'postid': xpostid
        }
        parsedLike = JSON.stringify(likeData)
        
        let sendLike = await fetch('/posts/like', {
            method: 'POST',
            body: parsedLike
        })
        let res = await sendLike
        let data = await res.body
        console.log(data)
        
        if (data['like']) {
            event.target.children[1].innerHTML = data['num_likes']
        }
        else if (data['unlike']) {
            event.target.children[1].innerHTML = data['unlike']
        } else if (data['err']) {
            alert(data['err'])
        }
    }
    else {
        alert('You are not logged in')
    }
}

async function postComment () {
    let idField = document.getElementById('postid')
    if (document.querySelector('.viewer') !='Guest' && document.querySelector('#editor').value != '') {
        cmntData = {
            'author': document.querySelector('.viewer').innerHTML, 
            'comment': document.querySelector('#editor').value,
            'postid': document.querySelector('.postid').value
        }
        parsedData = JSON.stringify(cmntData)
        
        let req = await fetch('/posts/comment', {
            method: 'POST',
            body: parsedData
        })
        res = await req
        console.log(res.text)
        alert(res.text)
    } else {
        alert('Log in to leave a comment')
    }
}
if (document.querySelector('.comment-form')) {
    let cmtBTN = document.querySelector('#comment-btn')
    cmtBTN.addEventListener('click', postComment)
}

toastCover = document.querySelector('#toast-cover')
toast = document.querySelector('#toast')
async function copyLink(event, xpostId) {
    origin = location.origin
    postid = xpostId
    fullpath = `${origin}/posts/post/${postid}`
    navigator.clipboard.writeText(fullpath)
    toastCover.style.display = 'flex'
    toast.innerHTML = 'Copied link!'
    
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

async function getMedia(event, postid) {
    pId = postid
    let getFiles = await fetch(`/posts/get_media?postID=${pId}`)
    let res = await getFiles
    if (res.status == 200) {
        data = await res.json()
        if (data.length > 1){
            for (elt=0; elt < data.length; elt++) {
                imgPrefix = `data:${data[elt]['type']};base64,`
                imgElt = document.createElement('img')
                imgElt.setAttribute('class', 'p-actual')
                imgElt.setAttribute('src', imgPrefix + data[elt]['data'])
                
                event.path[1].appendChild(imgElt)
            }
        }
        else if (data.length==1){
            imgPrefix = `data:${data[0]['type']};base64,`
            imgElt = document.createElement('img')
            imgElt.setAttribute('class', 'p-actual')
            imgElt.addEventListener('click', openImage)
            imgElt.setAttribute('src', imgPrefix + data[0]['data'])
            imgElt.style.width = '100%'
                
            event.path[1].appendChild(imgElt)
        }
    }
}
