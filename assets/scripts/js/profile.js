console.log(document.referrer)

let fields = document.querySelectorAll('.field')

let postsCover = document.querySelector('.posts-cover')
let photos = document.querySelector('.photos')
let about = document.querySelector('.about')
let account = document.querySelector('.account')

console.log(fields)

function tabswitch(event) {
    // for (child=0; child < fields.length; child++) {
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
    // }
}