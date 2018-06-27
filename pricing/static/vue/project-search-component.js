var project_search_component = {
    delimiters: ['[[', ']]'],
    props: {
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    template: ` 
        <search :title="'Lista projektów'"
                :restapi="'/pricing/projects?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    `
}