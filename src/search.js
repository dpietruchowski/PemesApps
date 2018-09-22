import Vue from 'vue'
import ProductList from './ProductList.vue'

var pl = new Vue({
  el: '#product-list',
  components: {
      'product-list': ProductList
  }
})