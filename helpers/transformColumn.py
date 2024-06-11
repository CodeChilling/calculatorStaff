
def transform_column(column: list[str], separators: list[str]) -> list[str]:
    new_list = column.copy()

    for separator in separators:
        temp_list = []
        for item in new_list:
            if separator in item:
                temp_list.extend(item.split(separator))
            else:
                temp_list.append(item)
        new_list = temp_list

    return new_list
