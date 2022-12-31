async function getSpace(event, curUser) {
    targetSpace = event.target.innerHTML
    location = `/s/${targetSpace}`
}
async function getPage(event, curUser) {
    targetPage = event.target.innerHTML
    location = `/p/${targetPage}`
}

spaceItem = document.querySelectorAll('.space-item')

async function search(event, ) {
    searchQuery = document.querySelector('#search')
    sQuery = searchQuery.value
    if (sQuery == '') {
        toastCover.style.display = 'flex'
        toast.innerHTML = 'Field cannot be empty'
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
    else if (sQuery != '') {
        location = `results/${sQuery}`
    }
}