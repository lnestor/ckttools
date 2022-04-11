def extract(model, to_extract, completion=False):
    values = {}

    for input_ in model:
        if str(input_) in to_extract:
            values[str(input_)] = model[input_]

    if completion:
        remaining = [i for i in to_extract if i not in values.keys()]
        for r in remaining:
            values[r] = False

    return values
