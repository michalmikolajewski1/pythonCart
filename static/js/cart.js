/*jshint esversion: 6 */
/* jshint node: true */
/* jshint loopfunc: true */
/* jshint asi: true */


const updateBtns = document.getElementsByClassName('update-cart');


for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateUserCart(productId, action)
        }
    })
}

function updateUserCart(productId, action) {
    console.log('User is authenticated, sending data...')

    const url = '/update_product/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('data', data)
            location.reload()
        });
}