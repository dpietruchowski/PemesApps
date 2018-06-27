Vue.component('search-input', {
    delimiters: ['[[', ']]'],
    props: {
        form_name: String,
        name: String,
        restapi: String
    },
    data: function () {
        return {
            inputValue: '',
            choosen: '',
            data: []
        }
    },
    computed: {
        names: function() {
            return this.data.map(function(obj) {
                return obj.name;
            })
        },
        form_id: function() {
            return 'id_' + this.form_name;
        },
    },
    methods: {
        clear: function() {
            this.inputValue = '';
            this.choosen = null;
        },
        getList: function () {
            fetch(this.restapi + this.inputValue)
                .then(resp => resp.json())
                .then(resp => {
                    this.data = [];
                    for (var obj of JSON.parse(resp)) {
                        var new_obj = {id: obj.id, name: obj.name};
                        this.data.push(new_obj);
                    }
                })
        },
        check: function() {
            if(this.names.indexOf(this.inputValue) == -1) {
                this.clear();
            } else {
                var objects = this.data.filter(function(obj) {
                    return obj.name === this.inputValue;
                }, this)
                if(objects.length > 0)
                    this.choosen = objects[0].id;
                else
                    this.clear();
            }
        }
    },
    watch: {
        inputValue: function() {
            this.getList();
        }
    },
    template: `
        <div>
            <input :name="form_name" :id="form_id" type="hidden" v-model="choosen">
            <input :list="name" v-model="inputValue" @blur="check">
            <datalist :id="name">
                <option v-for="name in names" :value="name" />
            </datalist>
        </div>
    `
})