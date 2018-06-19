Vue.component('search', {
    delimiters: ['[[', ']]'],
    props: {
        title: String,
        restapi: String,
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    data: function () {
        return {
            search: '',
            rows: [
            ],
        }
    },
    methods: {
        getButtonName: function (button) {
            return 'fa-' + button;
        },
        call: function (button, row) {
            if(typeof(this.callbacks) === 'undefined')
                return;
            var cb = this.callbacks[button];
            if (typeof(cb) === 'function')
                cb(row);
        },
        getProducts: function () {
            fetch(this.restapi + this.search)
                .then(resp => resp.json())
                .then(resp => {
                    this.rows = [];
                    for (var product of JSON.parse(resp)) {
                        var new_row = {};
                        for (let col of this.cols) {
                            new_row[col.name] = product[col.name];
                        }
                        this.rows.push(new_row);
                    }
                })
        },
    },
    watch: {
        search: function () {
            this.getProducts();
        }
    },
    mounted: function() {
        this.getProducts();
    },
    filters: {
      capitalize: function (str) {
        return str.charAt(0).toUpperCase() + str.slice(1)
      }
    },
    template: `
        <div class="card bg-light text-center">
            <div class="card-body">
                <h4>[[title]]</h4>
            </div>
            <div class="card-body input-group">
                <input class="form-control input-sm" type="text" maxlength="30" v-model="search"
                       placeholder="Szukaj"></input>
            </div>
            <div class="card-body table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th v-for="col in cols" v-if="col.display">
                                [[col.display | capitalize]]
                            </th>
                            <th v-if="buttons.length > 0"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="row in rows" :key="row.id">
                            <td v-for="col in cols" v-if="col.display">
                                [[ row[col.name] ]]
                            </td>
                            <td v-if="buttons.length > 0">
                              <a v-for="button in buttons" class="btn" v-on:click="call(button, row)">
                                <i class="fas" :class="getButtonName(button)"></i>
                              </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `
})