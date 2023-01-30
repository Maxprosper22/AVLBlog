let postsCover = document.querySelector('#all-posts')
let photos = document.querySelector('#photos')
let about = document.querySelector('.about')
let account = document.querySelector('.account')
allTablinks = document.querySelectorAll('.tablinks')
    
// console.log(allTablinks)
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
            imgData.src = galleryPrefix + pixdata[imgItem]['data']
            
            if (document.getElementById('imglist')) {
                let imgContainer = document.getElementById('imglist')
                imgContainer.appendChild(imgData)
            }
        }
    }
}

async function follow(event, curUser, xUser) {
    followX = await fetch(`follow?username=${curUser}&xid=${xUser}`)
    
    res = await followX
    console.log(res.body)
}

coverImg = document.querySelector('.cover-img')
profileImg = document.querySelector('.p-avatar')
viewDiv = document.querySelector('.view')
viewImg = document.querySelector('.view-img')

async function pixView(event) {
    viewDiv.style.display = 'flex'
    viewImg.src = event.target.src
}

async function closePix(event) {
    viewDiv.style.display = 'none'
}

// Upload New Profile Photo
let mediaPicker = document.createElement('input')
mediaPicker.setAttribute('id', 'pick_file')
mediaPicker.style.visibility = 'hidden'
mediaPicker.setAttribute('type', 'file')
mediaPicker.setAttribute('accept', 'images/*')

let mediaArray = []

async function setupReader(xfile) {
    let mediaData = {}
    mediaData.name = xfile['name']
    mediaData.type = xfile['type']
    console.log(xfile)
    
    let reader = new FileReader();
    reader.readAsDataURL(xfile)
    reader.onload = function(e) {
        mediaData.data = e.target.result.split(',')[1]
        src = `data:${xfile.type};base64,` + mediaData.data
        console.log(src)
        console.log(src)
        viewImg.src = src
    
    return mediaData
}
async function pickFiles(event) {
    mediaPicker.click()
    mediaPicker.addEventListener('change', (e)=>{
        console.log("holla")
        console.log(mediaPicker.file)
        setupReader(mediaPicker.files[0])
    }});
    
    return mediaPicker, mediaList
}