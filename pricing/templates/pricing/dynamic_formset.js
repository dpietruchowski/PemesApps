class DynamicFormset {
    constructor(table_id, empty_id, columns, form_prefix) {
        this.table_id = table_id;           // where appending
        this.empty_id = empty_id; // template row
        this.columns = columns; // columns
        this.form_prefix = form_prefix; //
    }

    add(element_pk, element_values) {
        if ($("#" + this.get_id(element_pk, "tr")).length > 0)
            return;
        var idx = this.total_forms();
        this.set_total_forms(idx + 1);
        var empty_row = $("#" +  this.empty_id).html();
        empty_row = empty_row.replace(/__pk__/g, element_pk);
        empty_row = empty_row.replace(/__prefix__/g, idx);
        $.each(element_values, function(key, value) {
            let reg = new RegExp("__" + key + "__", "g");
            empty_row = empty_row.replace(reg, value);
        });
        $("#" + this.table_id).append(empty_row);
    }

    remove(element_pk) {
        var element = $("#" + this.get_id(element_pk, "tr"));
        if (element.length == 0)
            return;
        var total = this.total_forms();
        this.set_total_forms(total - 1);
        var idx = parseInt(element.data("idx"));
        var next_element = element.next();
        for (let i = idx + 1; i < total; ++i) {
            let new_idx = i - 1;
            this.change_idx(i, new_idx);
            next_element.data("idx", new_idx)
            next_element = next_element.next();
        }
        element.remove();
    }

    total_forms() {
        return parseInt($("#id_" + this.form_prefix + "-TOTAL_FORMS").val());
    }
    set_total_forms(value) {
        $("#id_" + this.form_prefix + "-TOTAL_FORMS").val(value);
    }

    change_idx(old_idx, new_idx) {
        for (let key of this.columns) {
            this.change_form_idx(old_idx, new_idx, key);
        }
    }

    change_form_idx(old_idx, new_idx, name) {
        if($("#" + this.get_id(old_idx, name)).length == 0)
            return;
        $("#" + this.get_id(old_idx, name)).attr("name", this.get_name(new_idx, name));
        $("#" + this.get_id(old_idx, name)).attr("id", this.get_id(new_idx, name));
    }

    get_id(idx, name) {
        return "id_" + this.form_prefix + "-" + idx + "-" + name;
    }

    get_name(idx, name) {
        return this.form_prefix + "-" + idx + "-" + name;
    }
}

////// empty_form example //////////
//<div hidden>
//  <table>
//    <tbody id="empty_form">
//      <tr id="id_form-__pk__-tr" data-idx="__prefix__" data-pk="__pk__">
//        <td>__username__ <input type="hidden" name="form-__prefix__-account_id" maxlength="130" value="__account_id__" id="id_form-__prefix__-account_id"/></td>
//        <td><input type="number" name="form-__prefix__-contribution" step="0.01" value="__contribution__" id="id_form-__prefix__-contribution" /></td>
//        <td><input type="button" value="Remove" class="remove_bt"/></td>
//      </tr>
//    </tbody>
//  </table>
//</div>

////// form example /////////////
//<form method="POST" class="post-form">
//  <table class="table table-striped" id="beneficiary_table">
//    <thead>
//      <tr>
//        <th scope="col">Nazwa</th>
//        <th scope="col">Ilosc</th>
//      </tr>
//    </thead>
//    <tbody id="form_set">
//
//    </tbody>
//  </table>
//    <button type="submit" class="save btn btn-default">Zapisz</button>
//  <input name="form-TOTAL_FORMS" value="0" id="id_form-TOTAL_FORMS" /><input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS" /><input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS" /><input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS" />
//</form>

//$(document).ready(function() {
//    var dtable = new DynamicFormset(
//        "form_set",
//        "empty_form",
//        ["account_id", "contribution"],
//        "form"
//    );
//    $("#add").click(function() {
//        var num = $("#num").val();
//        var username = $("#username").val();
//        var pk = $("#pk").val();
//        dtable.add(parseInt(pk), {"username": username, "account_id": pk, "contribution": num});
//    })
//
//    $("#show").click(function() {
//        console.log($("#form_set").html())
//    })
//
//    $('#form_set').off().on('click', '.remove_bt', function() {
//        var pk = $(this).closest("tr").data("pk");
//        dtable.remove(pk);
//    });
//});