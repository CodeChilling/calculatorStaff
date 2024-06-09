def create_list_objects(currentList: list):
    finalList = []
    count = 0
    while count < len(currentList):
        temp = {
            "value": count + 1,
            "label": currentList[count]
        }
        finalList.append(temp)
        count += 1

    return finalList