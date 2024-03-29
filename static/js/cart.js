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

function updateData(bookId, action, place, reload=true) {
    if (user == 'AnonymousUser') {
        updateCookieData(bookId, action, place, reload)
    } else {
        updateUserData(bookId, action, place, reload)
    }
}

function updateCookieData(bookId, action, place, reload) {
    const now = Date.now()

    if (place == 'cart'){
        if (action == 'add' && cart[bookId] == undefined) {
            cart[bookId] = {'quantity': 1, 'date_added': now}
        } else if (action == 'delete') {
            delete cart[bookId]
        } else if (action.startsWith('set-to-')) {
            quantity = parseInt(action.replace('set-to-', ''))

            if (!isNaN(quantity)) {
                cart[bookId]['quantity'] = quantity
            }
        }
    } else if (place == 'wishlist') {
        if (action == 'add' && wishlist[bookId] == undefined) {
            wishlist[bookId] = {'date_added': now}
        } else if (action == 'delete') {
            delete wishlist[bookId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/;'
    document.cookie = 'wishlist=' + JSON.stringify(wishlist) + ';domain=;path=/;'

    if (reload) location.reload()
}

function updateUserData(bookId, action, place, reload) {
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
        if (reload) location.reload()
    })
}
