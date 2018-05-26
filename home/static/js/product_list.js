var product_search_component = {
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
            {name: 'n_dependency', display: 'Liczba produktów'},
        ],
        buttons: ['edit'],
        callbacks: {
            edit: function (row) {
                console.log(JSON.stringify(row));
                location.href="product/" + row.id + "/edit";
            }
        }
    }
})