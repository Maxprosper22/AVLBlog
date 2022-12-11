async function main() {
    let pyodide = await loadPyodide();
    return pyodide;
}

// let pyodideReadyPromise = main();

let mediaPicker = document.createElement('input')
mediaPicker.setAttribute('id', 'pick_file')
mediaPicker.setAttribute('style', 'visibility: hidden')
mediaPicker.setAttribute('type', 'file')
mediaPicker.setAttribute('accept', 'images/*')
mediaPicker.setAttribute('multiple', 'multiple')

mediaArray = []
let mediaList = []
let mediaHold = document.querySelector('#media-hold')
async function pickFiles(event) {
    document.querySelector('.new-post-form').appendChild(mediaPicker)
    mediaPicker.click()
    mediaPicker.addEventListener('change', (e)=>{
        function setupReader(xfile) {
            let mediaData = {}
            mediaData.name = xfile.name
            mediaData.type = xfile.type
            
            let reader = new FileReader();
            reader.readAsDataURL(xfile)
            reader.onload = function(e) {
                mediaData.data = e.target.result.split(',')[1]
                src = `data:${xfile.type};base64,`
                src += mediaData.data
                let mediaItem = document.createElement('img')
                mediaItem.setAttribute('class', 'media-items')
                mediaItem.src = src
                mediaHold.appendChild(mediaItem)
                };
                
            console.log(mediaData)
            mediaList.push(mediaData)
            return mediaData
        }
        for (file=0; file < mediaPicker.files.length; file++) {
            setupReader(mediaPicker.files[file])
        }
    });
    
    return mediaPicker, mediaList
}

toastCover = document.querySelector('#toast-cover')
toast = document.querySelector('#toast')
async function submitpost(e) {
    e.preventDefault();
    
    let txt = document.getElementById('text_content');
    let media = document.querySelector('#pick_file')
    
    data = {
        "author": document.querySelector('.username').innerHTML,
        "writeup": txt.value,
        "media": mediaList
    };
    postData = JSON.stringify(data);

    let newPost = await fetch(`${location.origin}/posts/add_post`, {
            method: "POST",
            redirect: "follow",
            headers: {
                "Content-Type": ("application/json")
                },
            body: postData,
        }
    );
    if (newPost.status==200) {
        toastCover.style.display = 'flex'
        toast.innerHTML = 'New Post Created'
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
        setTimeout(function() {
            location.reload()
        }, 4500);
    } else {
        toastCover.style.display = 'flex'
        toast.innerHTML = 'An error occurred'
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

document.getElementById('post-btn').addEventListener('click', submitpost);


// CKEDITOR.replace('text_content', {
//     customConfig: 'custom/custom_config.js'
// })

// let editorData = CKEDITOR.instances.text_content.getData()
// function checkFields (e) {
//     if (editorData === '') {
//         e.preventDefault()
//         alert('Error: Cannot Submit empty post!')
//     }
// }
// document.getElementById('post-btn').addEventListener('click', checkFields)