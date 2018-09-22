<template>
    <edit-form  url="/pricing/product"
                :title="title"
                :pk="pk"
                :csrftoken="csrftoken"
                :cols="cols">
    </edit-form>
</template>

<script>
import EditFrom from 'components/EditForm.vue'
export default {
    props: {
        csrftoken: String,
        pk: Number,
        form: Array,
        formset: Array
    },
    components: {
        'edit-form': EditFrom
    },
    data: function() {
        return {
            title: 'Nowy produkt',
            cols: {
                name: {display: 'Nazwa', type: 'text'},
                brand: {display: 'Marka', type: 'text'},
                price: {display: 'Cena', type: 'number'},
                group: {display: 'Grupa', type: 'select', options: [
                        {display: 'Mechanical', value: 'Mechanika'},
                        {display: 'Electrical', value: 'Elektryka'},
                        {display: 'Pneymatics', value: 'Pneumatyka'},
                    ]},
            }
        }
    },
    created: function() {
        if(this.pk)
            this.title = 'Edytuj produkt (id:' + this.pk + ')';
        console.log(this.cols);
        for(var item in this.form) {
            Object.keys(this.form[item]).forEach(function(key,index) {
                console.log(key);
                console.log(this.form[item][key]);
                this.cols[key].value = this.form[item][key];
            }, this);
        }
    },
}
</script>

