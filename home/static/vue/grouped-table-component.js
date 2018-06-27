Vue.component('grouped-table', {
  delimiters: ['[[', ']]'],
  props: {
    rows: Array,
    cols: Array,
  },
  data: function () {
      return {
        groupBy: ''
    }
  },
  computed: {
    groupByCol: function() {
      var groupBy = this.groupBy;
      return this.groupedCols.find(function(col) {
        return col.name === groupBy;
      });
    },
    sortedCols: function() {
      return this.cols.slice().sort(function(a, b){
        a = a.isValue;
        b = b.isValue;
        return a === b ? 0 : a < b ? -1 : 1;
      });
    },
    groupedCols: function () {
      return this.sortedCols.filter(function(col){
        return col.canBeGrouped;
      })
    },
    notValuedCols: function() {
      return this.sortedCols.filter(function(row){
        return !row.isValue;
      })
    },
    valuedCols: function () {
      return this.sortedCols.filter(function(row){
        return row.isValue;
      })
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }
  },
  methods: {
    filteredRows: function() {
    	var groupedMap = this.groupedMap();
      var rows = [];
      groupedMap.forEach(function(value, key) {
        if(this.groupBy !== 'id')
          rows.push(key);
        rows = rows.concat(value);
      }, this)
      return rows;
    },
    groupedMap: function () {
      var cols = this.cols;
      var rows = this.rows;
      var groupedMap = new Map();
      if (!this.groupBy)
        this.groupBy = 'id'
      var groupBy = this.groupBy;
      if (groupBy && this.groupByCol) {
        rows = rows.slice().sort(function (a, b) {
          a = a[groupBy]
          b = b[groupBy]
          return (a === b ? 0 : a > b ? 1 : -1)
        })
        var groupRow = '';
        var setGroupRow = function(row) {
        	if(row)
          	groupedMap.set(row, [])
        }
        rows.forEach(function(row) {
        	if(groupRow[groupBy] === row[groupBy]) {
          	this.valuedCols.forEach(function(col) {
							groupRow[col.name] = parseFloat(groupRow[col.name]) + parseFloat(row[col.name]);
          	})
          } else {
          	groupRow = Object.assign({isHeader: true}, row)
            setGroupRow(groupRow);
            cols.forEach(function(col) {
            	if(!col.isValue && col.name !== groupBy)
                groupRow[col.name] = "----"
            })
          }
          groupedMap.get(groupRow).push(row);
        }, this);
      }
      return groupedMap;
    },
    rowStyle: function(row) {
      if(row.isHeader)
        return "background-color: #ccccb3;";
      return "color: black;";
    }
  },
  template: `
    <div>
      <span>Grouped by: </span>
      <select v-model="groupBy">
        <option  v-for="col in groupedCols" :value="col.name">
          [[ col.display | capitalize ]]
        </option>
      </select>
      <table class="table table-striped">
        <thead>
          <tr>
            <th v-for="col in cols">
              [[ col.display | capitalize ]]
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in filteredRows()" :style="rowStyle(row)">
            <td v-for="col in sortedCols" v-if="!row.isHeader">
              [[ row[col.name] ]]
            </td>
            <td v-if="row.isHeader" :colspan="notValuedCols.length">
              [[ row[groupBy] ]]
            </td>
            <td v-for="col in valuedCols" v-if="row.isHeader">
              [[ row[col.name] ]]
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})