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
})