<template>
    <div class="modal fade" role="dialog" :id="id">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <slot name="header"></slot>
                </div>
                <div class="modal-body">
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
export default {
    props: {
        id: String
    },
    data: function () {
        return {
        }
    },
    computed: {
        id_selector: function() {
            return "#"+this.id;
        }
    },
    methods: {
        show: function() {
            this.modal('show');
        },
        hide: function() {
            this.modal('hide');
        },
        toggle: function() {
            this.modal('toggle');

        },
        modal: function(action) {
            $(this.id_selector).modal(action);
        }
    },
}
</script>
