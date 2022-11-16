if (document.querySelector('.createpost')) {
    let shortcut = document.querySelector('.createpost')
    shortcut.addEventListener('click', createpost)
}

function simbtn(e) {
    e.target.style.backgroundColor = 'rgb(0, 128, 128, 0.1'
}

// document.querySelector('#like').addEventListener('click', simbtn)
// document.querySelector('#cmmt').addEventListener('click', simbtn)

async function fetchImg(event, path) {
    let getFile = await fetch(`https:127.0.0.1:8080/static${path}`)
    let res = await getFile()
    console.log(res.status)
}