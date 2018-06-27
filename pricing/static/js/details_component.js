var table = new Vue({
    el: '#details_component',
    data: {
      cols: [
        { name: 'id', canBeGrouped: true, isValue: false, display: "id" },
        { name: 'name', canBeGrouped: true, isValue: false, display: "nazwa" },
        { name: 'group', canBeGrouped: true, isValue: false, display: "grupa"  },
        { name: 'component', canBeGrouped: true, isValue: false, display: "komponent"  },
        { name: 'detail_price', canBeGrouped: false, isValue: false, display: "cena detaliczna"  },
        { name: 'amount', canBeGrouped: false, isValue: false, display: "ilosc"  },
        { name: 'price', canBeGrouped: false, isValue: true, display: "cena"  },
      ],
      rows: [
      ]
    },
    methods: {
        add(row) {
            row.detail_price = row.detail_price.toFixed(2);
            row.price = row.detail_price * row.amount;
            row.price = row.price.toFixed(2)
            this.rows.push(row);
        }
    }
  })