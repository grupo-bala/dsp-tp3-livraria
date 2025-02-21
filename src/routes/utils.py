def get_response_object(items, page, size, total_count):
    return {
        "data": items,
        "pagination": {
            "page": page,
            "size": size,
            "total": total_count,
            "total_pages": (total_count + size - 1) // size,
            "has_next": page * size < total_count,
            "has_previous": page > 1,
        },
    }


def generate_filters(params):
    ignored_items = ["page", "size", "sort_by", "sort_order"]
    filters = {k: v for k, v in params if v is not None and k not in ignored_items}

    for key, value in filters.items():
        if type(value) is str and key != "id":
            filters[key] = {"$regex": value, "$options": "i"}

    return filters
