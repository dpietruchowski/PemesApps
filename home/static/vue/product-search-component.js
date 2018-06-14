var product_search_component = {
    delimiters: ['[[', ']]'],
    props: {
        cols: Array,
        buttons: Array,
        callbacks: Object
    },
    template: ` 
        <search :title="'Lista produktów'"
                :restapi="'/pricing/products?query='"
                :cols="cols"
                :buttons="buttons"
                :callbacks="callbacks">

        </search>
    `
}