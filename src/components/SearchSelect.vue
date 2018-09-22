<template>
    <div>
        <div>
            <input :list="name" v-model="inputValue" placeholder="Wyszukaj projekt" @blur="check">
        </div>
        <div>
            <select :name="form_name" :id="form_id" required="required" v-model="choosen" style="width: 100%">
                <option v-for="d in data" :value="d.id">[[ d.name ]]</option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        form_name: String,
        name: String,
        restapi: String,
    },
    data: function () {
        return {
            inputValue: '',
            choosen: '',
            selected: {},
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
        select: function(obj) {
            this.selected = obj;
            this.data.push(obj);
            this.choosen = this.selected.id;
        },
        clear: function() {
            this.inputValue = '';
            this.choosen = null;
        },
        getList: function () {
            fetch(this.restapi + this.inputValue)
                .then(resp => resp.json())
                .then(resp => {
                    this.data = [this.selected];
                    for (var obj of JSON.parse(resp)) {
                        var new_obj = {id: obj.id, name: obj.name};
                        if(this.selected.id != new_obj.id)
                            this.data.push(new_obj);
                    }
                })
        },
        check: function() {
            console.log(this.choosen);
        },
        findChoosen: function() {
            return this.data.find(function(obj) {
                return obj.id == this.choosen;
            }, this)
        },
        check2: function() {
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
        },
        choosen: function() {
            var obj = this.findChoosen();
            this.selected = obj;
        }
    },
}
</script>
