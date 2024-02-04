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
    if (user == 'AnonymousUser') {
        updateCookieData(bookId, action, place)
    } else {
        updateUserData(bookId, action, place)
    }
}

function updateCookieData(bookId, action, place) {
    const now = Date.now()

    if (place == 'cart'){
        if (action == 'add' && cart[bookId] == undefined) {
            cart[bookId] = {'quantity': 1, 'date_added': now}
            // Don't reload when adding to cart
            reload = () => { return }
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

    reload()
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
