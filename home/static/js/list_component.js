var component_search_component = {
    delimiters: ['[[', ']]'],
    props: {
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    template: ` 
        <search :title="'Lista komponentów'"
                :restapi="'/pricing/component?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    `
}

var csearch = new Vue({
    el: '#component_search',
    components: {
        'component-search': component_search_component
    },
    data: {
        cols: [
            {name: 'id', display: 'Id'},
            {name: 'name', display: 'Nazwa'},
            {name: 'project_name', display: 'Projekt'},
            {name: 'group', display: 'Grupa'},
        ],
        buttons: ['edit'],
        callbacks: {
            edit: function (row) {
                console.log(JSON.stringify(row));
                location.href="/pricing/component/" + row.id;
            },
        }
    }
})