<template>
    <div>
        <search-list edit info title="Lista produktów"
                  url="/pricing/product"
                  :cols="[
                  {name: 'id', display: 'Id'},
                  {name: 'name', display: 'Nazwa'},
                    ]">

        </search-list>
    </div>
</template>

<script>
import SearchList from 'components/SearchList.vue'
export default {
    name: 'product-list',
    components: {
        'search-list': SearchList
    },
}
</script>