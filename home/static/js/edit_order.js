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
            { name: 'id', display: 'id', type: 'hidden' },
            { name: 'name', display: 'Nazwa', type: 'hidden' },
            { name: 'amount', display: 'Ilość', type: 'hidden'},
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
})

var dtable = new Vue({
    el: '#dynamic_table',
    data: {
        rows: [],
        cols: [
            { name: 'id', },
            { name: 'name', display: 'Nazwa'},
            { name: 'price', display: 'Cena detaliczna'},
            { name: 'amount', display: 'Ilość'},
            { name: 'sum_price', display: 'Całkowita cena'},
        ],
        buttons: [],
        callbacks: {}
    }
})

var pricing = new Vue({
    delimiters: ['[[', ']]'],
    el: '#pricing',
    data: {
        price: 0,
        products: new Map(), // id: {row}
    },
    methods: {
        update_price: function(row) {
            var old_price = parseFloat(row.sum_price);
            var new_price = parseInt(row.amount) * parseFloat(row.price);
            var diff_price = new_price - old_price;
            row.sum_price = new_price.toFixed(2);
            this.price +=  diff_price.toFixed(2);
        },
        add: function(id, name, amount, price) {
            if (this.products.has(id)) {
                this.products.get(id).amount += amount;
                this.update_price(this.products.get(id));
            } else {
                var new_row = {name: name, 
                               price: price, 
                               amount: amount, 
                               sum_price: price * amount}
                this.products.set(id, new_row);
                dtable.rows.push(new_row);
                this.price += new_row.sum_price;
            }
        },
        remove: function(id, amount) {
            if (this.products.has(id)) {
                if (this.products.get(id).amount < amount)
                    this.products.get(id).amount = 0;
                else
                    this.products.get(id).amount -= amount;
                this.update_price(this.products.get(id));
                if (this.products.get(id).amount <= 0) {
                    var idx = dtable.rows.indexOf(this.products.get(id));
                    dtable.rows.splice(idx, 1);
                    this.products.delete(id);
                }
            }
        }
    }
})