var dorder = new Vue({
    delimiters: ['[[', ']]'],
    el: '#order',
    data: {
        price: 0,
        products: new Map(), // id: {row}
        rows: [] // {pk, name, amount, price}   
    },
    methods: {
        update_price: function(row) {
            var old_price = row.sum_price;
            row.sum_price = row.amount * row.price;
            this.price += row.sum_price - old_price;
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
                this.rows.push(new_row);
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
                    var idx = this.rows.indexOf(this.products.get(id));
                    this.rows.splice(idx, 1);
                    this.products.delete(id);
                }
            }
        }
    }
})

var dform_set = new Vue({
    delimiters: ['[[',']]'],
    el: '#form_set',
    data: {
        form_prefix: "form",
        cols: ['name', 'product_id', 'amount'],

        total_forms: 0,
        initial_forms: 0,
        min_num_forms: 0,
        max_num_forms: 1000,

        rows: [
        ],
        existed_rows: new Set()
    },
    methods: {
        amountChange(row) {
            if (isNaN(parseInt(row.amount)))
                row.amount = "0";
            var difference_amount = parseInt(row.amount) - row.prev_amount;
            this.updateDependency(row.pk, difference_amount);
            row.prev_amount = parseInt(row.amount);
        },
        updateDependency: function(id, amount) {
            fetch('/pricing/dependency?id=' + id + "&&amount=" + Math.abs(amount))
                .then(resp => resp.json())
                .then(resp => {
                    for (var product of JSON.parse(resp)) {                            
                        if (amount < 0)
                            dorder.remove(parseInt(product.pk), 
                                          parseInt(product.amount));
                        else if (amount > 0)
                            dorder.add(parseInt(product.pk),
                                       product.name,
                                       parseInt(product.amount),
                                       parseFloat(product.price));
                    }
                })
        },
        checkForm: function(e) {
            for (var row of this.rows) {
                if(!row.amount) {                    
                    e.preventDefault();
                    break;
                }
            }
        },
        getIdx: function(row) {
            return this.rows.indexOf(row);
        },
        getFormId: function(row, col) {
            return 'id_' + this.form_prefix + '-' + this.getIdx(row) + '-' + col;
        },
        getFormName: function(row, col) {
            return this.form_prefix + '-' + this.getIdx(row) + '-' + col;
        },
        add: function(row) {
            if (this.total_forms >= this.max_num_forms)
                return;
            if (!Number.isInteger(row.pk))
                return;
            if (this.existed_rows.has(row.pk))
                return;
            row.active = false;
            row.prev_amount = 0;
            this.rows.push(row);
            this.existed_rows.add(row.pk);
            ++this.total_forms;
        },
        remove: function(row) {
            if (this.total_forms == 0)
                return;
            if (!this.existed_rows.has(row.pk))
                return;
            row.amount = 0;
            this.amountChange(row);
            var idx = this.getIdx(row);
            this.rows.splice(idx, 1);
            this.existed_rows.delete(row.pk)
            --this.total_forms;
        }
    },
    mounted() {
    },
});

var dsearch = new Vue({
    delimiters: ['[[',']]'],
    el: '#product_search',
    data: {
        search: '',
        rows: [
        ],
        active: true
    },
    methods: {
        setActive: function(row, active) {
            row.active = active;
        },
        add: function(row) {
            dform_set.add({name: row.name, pk: parseInt(row.id), amount: 0, price: parseInt(row.price)});
        },
        getProducts: function() {
            this.rows = [];
            fetch('/pricing/products?query=' + this.search)
                .then(resp => resp.json())
                .then(resp => {
                    for (var product of JSON.parse(resp)) {
                        this.rows.push({name: product.name, id: product.id, price: product.price, active:true})
                    }
                })
        },
    },
    watch: {
        search: function() {
            this.getProducts();
        }
    }
});