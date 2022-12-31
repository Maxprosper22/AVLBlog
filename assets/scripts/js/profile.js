let postsCover = document.querySelector('#all-posts')
let photos = document.querySelector('#photos')
let about = document.querySelector('.about')
let account = document.querySelector('.account')
allTablinks = document.querySelectorAll('.tablinks')
options = document.querySelector('#options')
    
console.log(allTablinks)
console.log(options)
async function tabswitch(event) {
        
    for (tablink=0; tablink<allTablinks.length; tablink++){
        allTablinks[tablink].style.borderBottom = '1px solid rgb(0, 128, 128, .2)'
        
        if (event.target.innerHTML==allTablinks[tablink].innerHTML) {
            allTablinks[tablink].style.borderBottom = '2px solid rgb(0, 128, 128, .2)'
            
            if (event.target.innerHTML == 'Posts') {
                postsCover.style.display = 'flex'
                postsCover.style.flexDirection = 'column'
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

async function follow(event, curUser, xUser) {
    followX = await fetch(`follow?${curUser}&${xUser}`)
    
    res = await followX
    console.log(res)
}