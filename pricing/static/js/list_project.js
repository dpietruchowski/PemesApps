var psearch = new Vue({
    el: '#project_search',
    components: {
        'project-search': project_search_component
    },
    data: {
        cols: [
            {name: 'id', display: 'Id'},
            {name: 'name', display: 'Nazwa'},
            {name: 'leader', display: 'Lider'},
        ],
        buttons: ['edit', 'info'],
        callbacks: {
            edit: function (row) {
                location.href="/pricing/project/edit/" + row.id;
            },
            info: function (row) {
                location.href="/pricing/project/" + row.id;
            },
        }
    }
})