import json


def find(key, dictionary, path):
    for k, v in dictionary.items():
        if k == key:
            yield path + [k]
            # yield(path + [k])
        elif isinstance(v, dict):
            for result in find(key, v, path + [k]):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d, path + [k]):
                    yield result


# f = open('sample.json', "r")

# # Reading from file
# data = json.loads(f.read())
with open('sample.json') as json_file:
    data = json.load(json_file)

print(list(find('color', data, [])))
