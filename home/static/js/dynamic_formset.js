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
            this.rows.push(row);
            this.existed_rows.add(row.pk);
            ++this.total_forms;
        },
        remove: function(row) {
            if (this.total_forms == 0)
                return;
            if (!this.existed_rows.has(row.pk))
                return;
            var idx = this.getIdx(row);
            this.rows.splice(idx, 1);
            this.existed_rows.delete(row.pk)
            --this.total_forms;
        }
    },
    mounted() {
        console.log("mounted");
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
            dform_set.add({name: row.name, pk: parseInt(row.id), amount: 0});
        },
        getProducts: function() {
            console.log("getProducts");
            this.rows = [];
            fetch('/pricing/products?query=' + this.search)
                .then(resp => resp.json())
                .then(resp => {
                    for (var product of JSON.parse(resp)) {
                        this.rows.push({name: product.name, id: product.id, price: product.price, active:true})
                    }
                    console.log(this.rows);
                })
        },
    },
    watch: {
        search: function() {
            this.getProducts();
        }
    }
});