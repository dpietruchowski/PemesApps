var project_input_component = {
    computed: {
        form_id: function() {
            return 'id_' + this.form_name;
        },
    },
    methods: {
        select: function(obj) {
            this.$refs.ss.select(obj);
        }
    },
    template: ` 
        <search-select form_name="project" name="products" ref="ss"
                    restapi="/pricing/projects?query=">
        </search-select>
    `
}