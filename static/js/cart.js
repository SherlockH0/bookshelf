const addToBtns = document.querySelectorAll('.add-to')
const changeItem = document.querySelectorAll('.change-item')
const deleteItem = document.querySelectorAll('.delete-item')

addToBtns.forEach((button) => {
    button.addEventListener('click', () => {
        var bookId = button.dataset.book
        var place = button.dataset.place
        console.log(bookId, place)
    })
});

changeItem.forEach((input) => {
    input.addEventListener('change', () => {
        var itemId = input.dataset.item
        var value = input.value
        console.log(itemId, value)
    })
});

deleteItem.forEach((input) => {
    input.addEventListener('click', () => {
        var itemId = input.dataset.item
        console.log('Delete', itemId)
    })
})
