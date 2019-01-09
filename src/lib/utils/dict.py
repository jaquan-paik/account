def update_only_existed_keys(first: dict, second: dict):
    for key in first.keys():
        if key in second:
            first[key] = second[key]
