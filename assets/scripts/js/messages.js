async function popmenu(event, xviewer, xfriend) {
    console.log(event.target.parentElement.nextElementSibling)
    event.target.parentElement.nextElementSibling.style.display = 'flex'
}

covers = document.querySelectorAll('.menu-cover')
for (i=0; i<covers.length; i++) {
    covers[i].addEventListener('click', function (){
        if (event.target == this) {
            event.target.style.display = 'none'
        }
    })
}

async function getchat(event, xviewer, xfriend, xchatid) {
    location = `chat/${xfriend}?chatid=${xchatid}`
    // if (event.target == this) {
    //     alert('Holla')
    //     location = `chat/${xfriend}?chatid=${xchatid}`
    // }
}
// msgs = document.querySelectorAll('.msg')
// for (i=0; i<msgs.length; i++) {
//     msgs[i].addEventListener('click', function (){
//         if (event.target == this) {
//             location = ''
//             console.log('Hello, THIS!')
//         } else {
//             console.log('Holla, THAT!')
//         }
//     })
// }