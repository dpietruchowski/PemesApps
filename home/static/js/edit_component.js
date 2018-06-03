/*var psearch = new Vue({
    el: '#product_search',
    components: {
        'product-search': product_search_component
    },
    data: {
        cols: [
            { name: 'id', },
            { name: 'name', display: 'Nazwa'},
            { name: 'price', display: 'Cena'},
        ],
        buttons: ['plus'],
        callbacks: {
            plus: function (row) {
                dform_set.$refs.df.add({
                    name: row.name,
                    id: parseInt(row.id),
                    amount: 1
                });
            }
        }
    }
})*/

var dform_set = new Vue({
    el: '#element_formset',
    data: {
        prefix: 'form',
        cols: [
            { name: 'id', type: 'hidden', display: 'Id' },
            { name: 'name', type: 'none', display: 'Nazwa' },
            { name: 'amount', type: 'number', display: 'Ilość', min: 0},
        ]
    }
})

var smodal = new Vue({
    el: '#search_modal'
})

function getCookie(input) {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var name = cookies[i].split('=')[0].toLowerCase();
        var value = cookies[i].split('=')[1];
        if (name === input) {
            return value;
        } else if (value === input) {
            return name;
        }
    }
    return "";
};

function delete_component(id) {
    fetch("/pricing/component/" + id, {
        method: 'DELETE',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(resp => resp.json())
    .then(resp => {
        location.href="/pricing/component/list";
    })
}

function add_element() {
    
}