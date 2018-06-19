/*var product_search_component = {
    delimiters: ['[[', ']]'],
    props: {
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    template: ` 
        <search :title="'Lista produktów'"
                :restapi="'/pricing/products?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    `
}

var dform_set = new Vue({
    el: '#product_formset',
    data: {
        prefix: 'form',
        cols: [
            { name: 'id', type: 'hidden', display: 'Id' },
            { name: 'name', type: 'hidden', display: 'Nazwa' },
            { name: 'amount', type: 'number', display: 'Ilość', min: 0 },
        ]
    }
})
var psearch = new Vue({
    el: '#product_search',
    components: {
        'product-search': product_search_component
    },
    data: {
        cols: [
            { name: 'id', display: 'Id' },
            { name: 'name', display: 'Nazwa' },
            { name: 'price', display: 'Cena',},
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

function delete_product(id) {
    fetch("/pricing/product/edit/" + id, {
        method: 'DELETE',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(resp => resp.json())
    .then(resp => {
        location.href="/pricing/product/list";
    })
}