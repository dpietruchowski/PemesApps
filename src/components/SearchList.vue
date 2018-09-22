<template>
    <div>
        <search :title="title"
                :restapi="url + '/list?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks"
                @selected="$emit('selected', $event);">

        </search>
    </div>
</template>

<script>
import Search from './Search.vue'
export default {
    props: {
        title: String,
        url: String,
        cols: Array,
        edit: Boolean,
        info: Boolean
    },
    name: 'search-list',
    components: {
        'search': Search
    },
    data () {
        var btns = [];
        if (this.edit) btns.push('edit')
        if (this.info) btns.push('info')
        return {
            buttons: btns,
            callbacks: {
                edit: function (url, row) {
                    console.log(row.id)
                    location.href= url + "/edit/" + row.id;
                }.bind(this, this.url),
                info: function (url, row) {
                    console.log(row.id)
                    location.href= url + "/" + row.id;
                }.bind(this, this.url),
            }
        }
    }
}
</script>