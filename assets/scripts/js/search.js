async function getSpace(event) {
    targetSpace = event.target.innerHTML
    location = `/pages/${targetSpace}`
}

spaceItem = document.querySelectorAll('.space-item')

for (item = 0; item < spaceItem.length; item++) {
    spaceItem[item].addEventListener('click', getSpace)
}