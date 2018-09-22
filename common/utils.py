def get_all_fields(instance):
    fields = list(instance().base_fields)
    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields