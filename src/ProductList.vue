<template>
    <div>
        <search :title="title"
                :restapi="url + '/list?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    </div>
</template>

<script>
import Search from './components/Search.vue'
export default {
    props: {
        title: String,
        url: String,
        cols: Array,
    },
    name: 'product-list',
    components: {
        'search': Search
    },
    data () {
        return {
            buttons: ['edit', 'info'],
            callbacks: {
                edit: function (row) {
                    location.href= this.url + "/edit/" + row.id;
                },
                info: function (row) {
                    location.href= this.url + "/product/" + row.id;
                },
            }
        }
    }
}
</script>