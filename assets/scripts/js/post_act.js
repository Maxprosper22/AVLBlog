async function loadpost(event, xpostid) {
    location = `/posts/post/${xpostid}`
}
allpost = document.querySelectorAll('.userpost')
for (xpost=0; xpost<allpost.length; xpost++) {
    allpost[xpost].addEventListener('click', function(){
        allpost[xpost].parentElement
    })
}

async function popmenu(event, xviewer, xpostid) {
    console.log(event.target.parentElement.nextElementSibling)
    event.target.parentElement.nextElementSibling.style.display = 'flex'
}

covers = document.querySelectorAll('.pop-cover')
for (i=0; i<covers.length; i++) {
    covers[i].addEventListener('click', function (){
        if (event.target == this) {
            event.target.style.display = 'none'
        }
    })
}

async function getPostMedia(event) {
    pId = event.target.parentElement.parentElement[3].value
    let getFiles = await fetch(`/posts/get_post_media?postid=${pId}`, {
        method: 'GET'
    })
    let res = await getFiles
    data = await res.json()
    alert(data)
    console.log('Holla')
}
pImage = document.getElementsByClassName('p-actual')
for (xImg=0; xImg<pImage.length; xImg++){
    pImage[xImg].addEventListener('loadstart', getPostMedia)
}

async function get_likes(xpostid) {
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
async function copyLink(event, xpostId) {
    origin = location.origin
    postid = xpostId
    fullpath = `${origin}/posts/post/${postid}`
    console.log(fullpath)
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