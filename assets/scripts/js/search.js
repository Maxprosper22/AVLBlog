async function getSpace(event, curUser) {
    targetSpace = event.target.innerHTML
    location = `/s/${targetSpace}`
}
async function getPage(event, curUser) {
    targetPage = event.target.innerHTML
    location = `/p/${targetPage}`
}

spaceItem = document.querySelectorAll('.space-item')