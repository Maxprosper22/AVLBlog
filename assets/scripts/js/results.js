postMacro = document.querySelectorAll('.posts')
// console.log(postMacro)
// postMacro[postMacro.length - 1].style.marginBottom = '1%'
allTabs = document.querySelector('.tab-hold')
tabs = document.querySelectorAll('.tabs')
previewLabel = document.querySelectorAll('.preview-label')
previews = document.querySelectorAll('.previews')
userMatch = document.querySelectorAll('.usermatch')
pageMatch = document.querySelectorAll('.pagematch')
spaceMatch = document.querySelectorAll('.spacematch')
postMatch = document.querySelectorAll('.postmatch')
postsMatch = document.querySelectorAll('.posts-match')

console.log(allTabs.children)
console.log(tabs)
window.onload = function () {
    allTabs.children[0].style.borderBottom = '2px solid rgb(0, 128, 128, .2)'
}

async function resultSwitch(event) {
    
    for (tab=0; tab<tabs.length; tab++) {
        if (event.target.innerHTML == tabs[tab].innerHTML) {
            tabs[tab].style.borderBottom = '2px solid rgb(0, 128, 128, .2)'
            if (event.target.innerHTML=='All') {
                for (label=0; label<previewLabel.length; label++) {
                    previewLabel[label].style.display = 'flex'
                }
                for (preview=0; preview<previews.length; preview++) {
                    previews[preview].style.display = 'flex'
                }
                for (match=0; match<userMatch.length; match++) {
                    console.log(userMatch[match])
                    userMatch[match].style.display= 'none'
                }
                for (page=0; page<pageMatch.length; page++) {
                    pageMatch[page].style.display = 'none'
                }
                for (space=0; space<spaceMatch.length; space++) {
                    spaceMatch[space].style.display = 'none'
                }
                for (post=0; post<postsMatch.length; post++) {
                    postsMatch[post].style.display='block'
                    // postsMatch[post].style.border = '1px solid black'
                }
                for (post=0; post<postMatch.length; post++) {
                    postMatch[post].style.display = 'none'
                }
                // postsMatch.style.flexDirection='column'
            }
            else if (event.target.innerHTML=='People') {
                
                for (label=0; label<previewLabel.length; label++) {
                    previewLabel[label].style.display = 'none'
                }
                for (preview=0; preview<previews.length; preview++) {
                    previews[preview].style.display = 'none'
                }
                console.log(userMatch)
                for (match=0; match<userMatch.length; match++) {
                    console.log(userMatch[match])
                    userMatch[match].style.display= 'flex'
                }
                for (page=0; page<pageMatch.length; page++) {
                    pageMatch[page].style.display = 'none'
                }
                for (space=0; space<spaceMatch.length; space++) {
                    spaceMatch[space].style.display = 'none'
                }
                for (post=0; post<postMatch.length; post++) {
                    postMatch[post].style.display = 'none'
                }
                postsMatch.style.display='none'
            }
            else if (event.target.innerHTML=='Posts') {
                
                for (label=0; label<previewLabel.length; label++) {
                    previewLabel[label].style.display = 'none'
                }
                for (preview=0; preview<previews.length; preview++) {
                    previews[preview].style.display = 'none'
                }
                console.log(userMatch)
                for (match=0; match<userMatch.length; match++) {
                    userMatch[match].style.display= 'none'
                }
                for (page=0; page<pageMatch.length; page++) {
                    pageMatch[page].style.display = 'none'
                }
                for (space=0; space<spaceMatch.length; space++) {
                    spaceMatch[space].style.display = 'none'
                }
                for (post=0; post<postsMatch.length; post++) {
                    postsMatch[post].style.display='none'
                }
                for (post=0; post<postMatch.length; post++) {
                    postMatch[post].style.display = 'flex'
                }
            }
            else if (event.target.innerHTML=='Pages') {
                
                for (label=0; label<previewLabel.length; label++) {
                    previewLabel[label].style.display = 'none'
                }
                for (preview=0; preview<previews.length; preview++) {
                    previews[preview].style.display = 'none'
                }
                console.log(userMatch)
                for (match=0; match<userMatch.length; match++) {
                    userMatch[match].style.display= 'none'
                }
                for (page=0; page<pageMatch.length; page++) {
                    pageMatch[page].style.display = 'flex'
                }
                for (space=0; space<spaceMatch.length; space++) {
                    spaceMatch[space].style.display = 'none'
                }
                for (post=0; post<postMatch.length; post++) {
                    postMatch[post].style.display = 'none'
                }
                postsMatch.style.display='none'
            }
            else if (event.target.innerHTML=='Spaces') {
                
                for (label=0; label<previewLabel.length; label++) {
                    previewLabel[label].style.display = 'none'
                }
                for (preview=0; preview<previews.length; preview++) {
                    previews[preview].style.display = 'none'
                }
                console.log(userMatch)
                for (match=0; match<userMatch.length; match++) {
                    userMatch[match].style.display= 'none'
                }
                for (page=0; page<pageMatch.length; page++) {
                    pageMatch[page].style.display = 'none'
                }
                for (space=0; space<spaceMatch.length; space++) {
                    spaceMatch[space].style.display = 'flex'
                }
                for (post=0; post<postMatch.length; post++) {
                    postMatch[post].style.display = 'none'
                }
                postsMatch.style.display='none'
            }
        } else {
            tabs[tab].style.borderBottom = '1px solid rgb(0, 128, 128, .2)'
        }
    }
}
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
        location = `/search/results/${sQuery}`
    }
}