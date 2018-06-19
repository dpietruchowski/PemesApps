var psearch = new Vue({
    el: '#product_search',
    components: {
        'product-search': product_search_component
    },
    data: {
        cols: [
            {name: 'id', display: 'Id'},
            {name: 'name', display: 'Nazwa'},
            {name: 'price', display: 'Cena'},
            {name: 'group', display: 'Grupa'},
        ],
        buttons: ['edit'],
        callbacks: {
            edit: function (row) {
                location.href="/pricing/product/edit/" + row.id;
            },
            /*info: function (row) {
                location.href="/pricing/product/" + row.id;
            },*/
        }
    }
})