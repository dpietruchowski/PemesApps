<template>
    <div>
        <edit-form  url="/pricing/project"
                    :title="title"
                    :pk="pk"
                    :csrftoken="csrftoken"
                    :cols="cols">

            <edit-formset form_prefix="form"
                          :cols="formset_cols">

            </edit-formset>
        </edit-form>
    </div>
</template>

<script>
import EditForm from 'components/EditForm.vue'
import EditFormset from 'components/EditFormset.vue'
export default {
    props: {
        csrftoken: String,
        pk: Number,
        form: Array
    },
    components: {
        'edit-form': EditForm,
        'edit-formset': EditFormset
    },
    data: function() {
        return {
            title: 'Nowy komponent',
            formset_cols: [
                { name: 'id', type: 'hidden', display: 'Id'},
                { name: 'name', type: 'hidden', display: 'Nazwa'},
                { name: 'amount', type: 'number', display: 'Ilość', min: 0},
            ],
            cols: {
                name: {display: 'Nazwa', type: 'text'},
                leader: {display: 'Lider', type: 'text'},
                description: {display: 'Opis', type: 'textarea'},
            }
        }
    },
    created: function() {
        if(this.pk)
            this.title = 'Edytuj komponent (id:' + this.pk + ')';
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

