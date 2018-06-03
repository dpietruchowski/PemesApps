Vue.component('modal', {
    delimiters: ['[[', ']]'],
    props: {
        id: String
    },
    data: function () {
        return {
        }
    },
    methods: {
    },
    template: `
        <div class="modal fade" role="dialog" :id="id">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <slot name="header"></slot>
                    </div>
                    <div class="modal-body">
                        id
                        <slot></slot>
                    </div>
                </div>
            </div>
        </div>
    `
})