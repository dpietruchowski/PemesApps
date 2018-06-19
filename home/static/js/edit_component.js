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
            {name: 'project_name', display: 'Projekt'},
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

function delete_component(id) {
    fetch("/pricing/component/edit/" + id, {
        method: 'DELETE',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(resp => resp.json())
    .then(resp => {
        location.href="/pricing/component/list";
    })
}
    