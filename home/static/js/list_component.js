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