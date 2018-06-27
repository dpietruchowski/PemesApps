var component_search_component = {
    delimiters: ['[[', ']]'],
    props: {
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    template: ` 
        <search :title="'Lista komponentów'"
                :restapi="'/pricing/components?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    `
}