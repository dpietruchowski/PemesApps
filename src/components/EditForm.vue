<template>
    <div class="card bg-light mx-auto">
      <div class="text-center">
        <form method="POST" class="post-form">
          <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken" />
          <div class="card-body">
            <h4 class="card-title">{{ title }}</h4>
          </div>
          <div v-for="(col, col_name) in cols" class="card-body">
            <div style="float:left;"><p class="card-text" >{{ col.display }}</p></div>
            <div style="float:right;">
                <p class="card-text" >
                    <input v-if="get_type(col) == 0" :type="col.type" :name="col_name" maxlength="30" required :id="'id_' + col_name" v-model="col.value"/>
                    <select v-if="get_type(col) == 1" :name="col_name" :id="'id_' + col_name" v-model="col.value">  
                        <option selected disabled>Wybierz</option>
                        <option v-for="option in col.options" :value="option.value">{{ option.display }}</option>
                    </select>
                    <textarea v-if="get_type(col) == 2" :name="col_name" cols="40" rows="10" required="" :id="get_id(col_name)" style="height: 231px;" v-model="col.value"></textarea>
                </p>
            </div>
          </div>
          <div class="card-body">
            <slot></slot>
          </div>
          <div class="card-body">
            <button type="submit" class="save btn btn-default">Zapisz</button>
            <button v-if="pk" type="button" class="save btn btn-default" onclick="delete_product">Usuń</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script>
export default {
    props: {
        url: String,
        title: String,
        pk: Number,
        csrftoken: String,
        cols: Object,
        init_form: Array
    },
    data: function() {
        return {
        }
    },
    methods: {
        delete_product: function() {
            fetch(this.url + '/edit/' + this.pk, {
                method: 'DELETE',
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": this.csrftoken,
                },
            })
            .then(resp => resp.json())
            .then(resp => {
                console.log(resp);
                location.href=this.url + '/list';
            })
        },
        get_type: function(col) {
            if(col.type == 'select') return 1
            if(col.type == 'textarea') return 2
            return 0
        },
        get_id: function(col_name) {
            return 'id' + col_name;
        }
    },
    created: function() {
        for(var item in this.init_form) {
            Object.keys(this.init_form[item]).forEach(function(key,index) {
                this.cols[key].value = this.init_form[item][key];
            }, this);
        }
    },
}
</script>

