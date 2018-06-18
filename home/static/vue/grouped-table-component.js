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
    groupedMap: function () {
      var cols = this.cols;
      var rows = this.rows;
      var groupedMap = new Map();
      if (!this.groupBy)
        this.groupBy = 'id'
      var groupBy = this.groupBy;
      if (groupBy && 
      cols.map(function(e) {return e.name}).indexOf(groupBy) >= 0) {
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
          	groupRow = Object.assign({}, row)
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
    filteredRows: function() {
    	var groupedMap = this.groupedMap;
      var rows = [];
      groupedMap.forEach(function(value, key) {
        rows = rows.concat(value);
        console.log(this.groupBy)
        if(this.groupBy !== 'id')
          rows.push(key);
      }, this)
      return rows;
    },
    groupedCols: function () {
        var cols = this.cols;
      cols = cols.filter(function(row){
          return row.canBeGrouped;
      })
      return cols
    },
    valuedCols: function () {
        var cols = this.cols;
      cols = cols.filter(function(row){
          return row.isValue;
      })
      return cols
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
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
          <tr v-for="row in filteredRows">
            <td v-for="col in cols">
              [[ row[col.name] ]]
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})