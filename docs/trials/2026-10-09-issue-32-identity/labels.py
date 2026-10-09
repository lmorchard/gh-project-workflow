def format_item_count(count):
    noun = "item" if count == 1 else "items"
    return f"{count} {noun}"
