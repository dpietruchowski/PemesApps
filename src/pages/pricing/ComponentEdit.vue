<template>
    <edit-form  url="/pricing/component"
                :title="title"
                :pk="pk"
                :csrftoken="csrftoken"
                :cols="cols"
                :init_form="form">

        <edit-formset ref="formset" form_prefix="form"
                      :cols="formset_cols"
                      :init_formset="formset">

        </edit-formset>
        <modal id="product_list">
            <search-list title="Lista produktów"
                         url="/pricing/product"
                         @selected="onselect"
                         :cols="[
                            {name: 'id', display: 'Id'},
                            {name: 'name', display: 'Nazwa'},
                         ]">

            </search-list>
            <header>
                <button type="button" class="save btn btn-default" @click="add">
                    Dodaj
                </button>
            </header>
        </modal>
        <button type="button" class="save btn btn-default" data-toggle="modal" data-target="#product_list">
            Dodaj product
        </button>
    </edit-form>
</template>

<script>
import EditFrom from 'components/EditForm.vue'
import EditFormset from 'components/EditFormset.vue'
import Modal from 'components/Modal.vue'
import SearchList from 'components/SearchList.vue'
export default {
    props: {
        csrftoken: String,
        pk: Number,
        form: Array,
        formset: Array
    },
    components: {
        'edit-form': EditFrom,
        'edit-formset': EditFormset,
        'modal': Modal,
        'search-list': SearchList
    },
    data: function() {
        return {
            title: 'Nowy komponent',
            cols: {
                name: {display: 'Nazwa', type: 'text'},
            },
            formset_cols: [
                { name: 'id', type: 'hidden', display: 'Id'},
                { name: 'name', type: 'hidden', display: 'Nazwa'},
                { name: 'amount', type: 'number', display: 'Ilość', min: 0},
            ],
            selected: null,
        }
    },
    methods: {
        onselect: function(event) {
            this.selected = event;
        },
        add: function() {
            if(this.selected) {
                console.log("etest")
                var toadd = {
                    id: parseInt(this.selected.id),
                    name: this.selected.name,
                    amount: 0,
                }
              this.$refs.formset.add(toadd);
            }
        }
    },
    created: function() {
        if(this.pk)
            this.title = 'Edytuj komponent (id:' + this.pk + ')';
    },
}
</script>

