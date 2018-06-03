Vue.component('dynamic-formset', {
    delimiters: ['[[', ']]'],
    props: {
        form_prefix: String,
        cols: Array,
    },
    data: function () {
        return {
            total_forms: 0,
            initial_forms: 0,
            min_num_forms: 0,
            max_num_forms: 1000,
            rows: [
            ],
            existed_rows: new Set()
        }
    },
    methods: {
        getIdx: function(row) {
            return this.rows.indexOf(row);
        },
        getFormId: function(row, col) {
            return 'id_' + this.form_prefix + '-' + this.getIdx(row) + '-' + col.name;
        },
        getFormName: function(row, col) {
            return this.form_prefix + '-' + this.getIdx(row) + '-' + col.name;
        },
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
        add: function(row) {
            if (this.total_forms >= this.max_num_forms) {
                console.log("max total forms")
                return;
            }
            if (!Number.isInteger(row.id)) {
                console.log("row.id is not an integer")
                return;
            }
            if (this.existed_rows.has(row.id)) {
                console.log("row with this id already exists")
                return;
            }
            row.active = false;
            this.rows.push(row);
            this.existed_rows.add(row.id);
            ++this.total_forms;
        },
        remove: function(row) {
            if (this.total_forms == 0)
                return;
            if (!this.existed_rows.has(row.id))
                return;
            var idx = this.getIdx(row);
            this.rows.splice(idx, 1);
            this.existed_rows.delete(row.id)
            --this.total_forms;
        }
    },
    filters: {
      capitalize: function (str) {
        return str.charAt(0).toUpperCase() + str.slice(1)
      }
    },
    template: `
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th v-for="col in cols" v-if="col.display"">
                        [[col.display | capitalize]]
                    </th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in rows" :key="row.id">
                    <td v-for="col in cols" v-if="col.display">
                        <span v-if="col.type == 'hidden' || col.type == 'none'">[[ row[col.name] ]]</span>
                        <input v-if="col.type != 'none'"
                            :id="getFormId(row, col)"
                            :name="getFormName(row, col)"
                            :type="col.type" v-model="row[col.name]" :min=col.min />
                    </td>
                    <td>
                        <a class="btn" v-on:click="remove(row)">
                            <i class="fas fa-trash"></i>
                        </a>
                    </td>
                </tr>
            </tbody>
        </table>
        <input type="hidden" name="form-TOTAL_FORMS" :value="total_forms" id="id_form-TOTAL_FORMS" />
        <input type="hidden" name="form-INITIAL_FORMS" :value="initial_forms" id="id_form-INITIAL_FORMS" />
        <input type="hidden" name="form-MIN_NUM_FORMS" :value="min_num_forms" id="id_form-MIN_NUM_FORMS" />
        <input type="hidden" name="form-MAX_NUM_FORMS" :value="max_num_forms" id="id_form-MAX_NUM_FORMS" />
    </div>
    `
})