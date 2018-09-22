<template>
    <div>
        <search-list edit info title="Lista projektów"
                  url="/pricing/project"
                  :cols="[
                  {name: 'id', display: 'Id'},
                  {name: 'name', display: 'Nazwa'},
                  {name: 'leader', display: 'lider'},
                    ]">

        </search-list>
    </div>
</template>

<script>
import SearchList from 'components/SearchList.vue'
export default {
    components: {
        'search-list': SearchList
    },
}
</script>