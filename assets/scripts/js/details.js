allMedia = []

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
                imgElt.setAttribute('alt', data[elt]['title'])
                imgElt.setAttribute('src', imgPrefix + data[elt]['data'])
                imgElt.addEventListener('click', openImage)
                
                event.path[1].appendChild(imgElt)
                allMedia.push(imgElt)
            }
        }
        else if (data.length==1){
            imgPrefix = `data:${data[0]['type']};base64,`
            imgElt = document.createElement('img')
            imgElt.setAttribute('class', 'p-actual')
            imgElt.setAttribute('alt', data[0]['title'])
            imgElt.setAttribute('src', imgPrefix + data[0]['data'])
            imgElt.style.width = '100%'
            imgElt.addEventListener('click', openImage)
                
            event.path[1].appendChild(imgElt)
            allMedia.push(imgElt)
        }
    }
}

scroller = document.querySelector('.touch-scroll')

slideImg = document.querySelector('.slide-img')

async function openImage(event) {
    function checkSrc(checkElt) {
        return checkElt.src ?checkElt.src == event.target.src : alert('wrong target')
    }
    srcElt = allMedia.find(checkSrc)
    console.log(srcElt)
    slideImg.style.backgroundImage = `url(${srcElt.src})`
    slideImg.style.backgroundSize = 'contain'
    slideImg.style.backgroundPosition = 'center'
    slideImg.style.backgroundRepeat = 'no-repeat'
    scroller.style.display = 'flex'
}
console.log(allMedia)

toastCover = document.querySelector('#toast-cover')
toast = document.querySelector('#toast')
async function plusSlide(event) {
    slideImg = document.querySelector('.slide-img')
    preSlice = slideImg.style.backgroundImage.slice(5)
    postSlice = preSlice.slice(0, -2)
    function checkList(checkCur) {
        return checkCur ?checkCur.src == postSlice : alert('wrong target')
    }
    curIndex = allMedia.find(checkList)
    for (sortmedia=0; sortmedia<allMedia.length; sortmedia++) {
        if (sortmedia < allMedia.length) {
            // console.log(allMedia[sortmedia].src)
            if (allMedia[sortmedia].src == postSlice) {
                if (sortmedia == allMedia.length || sortmedia > allMedia.length) {}
                else {
                    sortedmedia = sortmedia+1
                    slideImg.style.backgroundImage = `url(${allMedia[sortedmedia].src})`
                }
            }
        }
        else if (sortmedia == allMedia.length) {
            toastCover.style.display = 'flex'
            toast.innerHTML = 'You have reached the end!'
            
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
    }
    console.log(curIndex)
}
async function minusSlide(event) {
    slideImg = document.querySelector('.slide-img')
    preSlice = slideImg.style.backgroundImage.slice(5)
    postSlice = preSlice.slice(0, -2)
    function checkList(checkCur) {
        return checkCur ?checkCur.src == postSlice : alert('wrong target')
    }
    curIndex = allMedia.find(checkList)
    for (sortmedia=0; sortmedia<allMedia.length; sortmedia++) {
        if (sortmedia < allMedia.length) {
            // console.log(allMedia[sortmedia].src)
            if (allMedia[sortmedia].src == postSlice) {
                if (sortmedia == allMedia.length || sortmedia > allMedia.length) {}
                else {
                    sortedmedia = sortmedia-1
                    slideImg.style.backgroundImage = `url(${allMedia[sortedmedia].src})`
                }
            }
        }
    }
}
async function closePix(event) {
    scroller.style.display = 'none'
}