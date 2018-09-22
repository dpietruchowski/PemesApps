<template>
    <div>
        <search-list edit info title="Lista komponentów"
                  url="/pricing/component"
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
    name: 'component-list',
    components: {
        'search-list': SearchList
    },
}
</script>