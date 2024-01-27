const updateBtns = document.querySelectorAll('.update-item')
const changeItem = document.querySelectorAll('.change-item')

updateBtns.forEach((button) => {
    button.addEventListener('click', () => {
        var bookId = button.dataset.book
        var place = button.dataset.place
        var action = button.dataset.action
        updateData(bookId, action, place)

    })
});

changeItem.forEach((input) => {
    input.addEventListener('change', () => {
        var bookId = input.dataset.book
        var value = input.value

        updateData(bookId, `set-to-${value}`, 'cart')
    })
});

function updateData(bookId, action, place) {
    if (user === 'AnonymousUser') {
        console.log('User is not logged in')
    } else {
        updateUserData(bookId, action, place)
    }
}

function updateUserData(bookId, action, place) {
    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'bookId': bookId,
            'action': action,
            'place': place})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        reload()
    })
}
