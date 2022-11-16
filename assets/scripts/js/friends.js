async function popmenu(event, xviewer, xfriend) {
    console.log(event.target.parentElement.nextElementSibling)
    event.target.parentElement.nextElementSibling.style.display = 'flex'
}

covers = document.querySelectorAll('.fr-ops-cover')
for (i=0; i<covers.length; i++) {
    covers[i].addEventListener('click', function (){
        if (event.target == this) {
            event.target.style.display = 'none'
        }
    })
}