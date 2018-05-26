Vue.component('dynamic-table', {
    delimiters: ['[[', ']]'],
    props: {
        rows: Array,
        cols: Array,
        buttons: Array,
        callbacks: Object
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
    },
    filters: {
      capitalize: function (str) {
        return str.charAt(0).toUpperCase() + str.slice(1)
      }
    },
    template: `
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
    `
})