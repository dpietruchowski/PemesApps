var dform_set = new Vue({
    el: '#element_formset',
    data: {
        prefix: 'form',
        cols: [
            { name: 'id', type: 'hidden', display: 'Id' },
            { name: 'name', type: 'hidden', display: 'Nazwa' },
            { name: 'amount', type: 'number', display: 'Ilość', min: 0},
        ]
    }
})

var psmodal = new Vue({
    el: '#psearch_modal',
    components: {
        'product-search': product_search_component
    },
    data: {
        cols: [
            {name: 'id', display: 'Id'},
            {name: 'name', display: 'Nazwa'},
            {name: 'price', display: 'Cena'},
            {name: 'group', display: 'Grupa'},
        ],
        buttons: ['plus'],
        callbacks: {
            plus: function (row) {
                dform_set.$refs.df.add({
                    name: row.name,
                    id: parseInt(row.id),
                    amount: 0
                });
            },
        }
    }
})

var csmodal = new Vue({
    el: '#csearch_modal',
    components: {
        'component-search': component_search_component
    },
    data: {
        cols: [
            {name: 'id', display: 'Id'},
            {name: 'name', display: 'Nazwa'},
            {name: 'project', display: 'Projekt'},
        ],
        buttons: ['plus'],
        callbacks: {
            plus: function (row) {
                dform_set.$refs.df.add({
                    name: row.name,
                    id: parseInt(row.id),
                    amount: 0
                });
            },
        }
    }
})

var project_input = new Vue({
    el: '#project_input',
    data: {
        choosen: null
    },
    components: {
        'project-input': project_input_component
    },
});
    