async function tabswitch(event) {
    let postsCover = document.querySelector('#all-posts')
    let photos = document.querySelector('#photos')
    let about = document.querySelector('.about')
    let account = document.querySelector('.account')
        
    if (event.target.innerHTML == 'Posts') {
        postsCover.style.display = 'block'
        photos.style.display = 'none'
        account.style.display = 'none'
    }
    else if (event.target.innerHTML == 'Photos') {
        postsCover.style.display = 'none'
        photos.style.display = 'flex'
        account.style.display = 'none'
    }
    else if (event.target.innerHTML == 'Account') {
        postsCover.style.display = 'none'
        photos.style.display = 'none'
        account.style.display = 'flex'
    }
}

async function getPhotos(event, userID) {
    uID = userID
    let getFiles = await fetch(`/posts/get_photos?userID=${uID}`)
    let res = await getFiles
    if (res.status == 200) {
        pixdata = await res.json()
        for (imgItem= 0; imgItem<pixdata.length; imgItem++) {
            galleryPrefix = `data:${pixdata[imgItem]['type']};base64,`
            imgData = document.createElement('img')
            imgData.setAttribute('class', 'photo-item')
            imgData.setAttribute('src', galleryPrefix + pixdata[imgItem]['data'])
            
            if (document.getElementById('imglist')) {
                let imgContainer = document.getElementById('imglist')
                imgContainer.appendChild(imgData)
            }
        }
    }
}