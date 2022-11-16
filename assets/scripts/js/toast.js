toastCover = document.querySelector('#toast-cover')
toast = document.querySelector('#toast')

async function showToast(msg) {
    toastCover.style.display = 'flex'
    toast.innerHTML = 'An error occurred!'
}