import json


def findkey(key, dictionary, path):
    for k, v in dictionary.items():
        if k == key:
            yield path + [k]
        elif isinstance(v, dict):
            for result in findkey(key, v, path + [k]):
                yield result
        elif isinstance(v, list):
            for d in v:
                index = v.index(d)
                for result in findkey(key, d, path + [k] + [index]):
                    yield result


def findvalue(value, dictionary, path):
    for k, v in dictionary.items():
        if v == value:
            yield path + [k]
        elif isinstance(v, dict):
            for result in findvalue(value, v, path + [k]):
                yield result
        elif isinstance(v, list):
            for d in v:
                index = v.index(d)
                for result in findvalue(value, d, path + [k] + [index]):
                    yield result


def findkeyvalue(key, dictionary, path, value):
    for k, v in dictionary.items():
        if key == k and v == value:
            yield path + [k]
        elif isinstance(v, dict):
            for result in findkeyvalue(key, v, path + [k], value):
                yield result
        elif isinstance(v, list):
            for d in v:
                index = v.index(d)
                for result in findkeyvalue(key, d, path + [k] + [index], value):
                    yield result


def getFromDict(dataDict, mapList):
    for k in mapList:
        dataDict = dataDict[k]
    return dataDict


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


def findallvalues(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in findallvalues(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in findallvalues(key, d):
                    yield result


# f = open('sample.json', "r")

# # Reading from file
# data = json.loads(f.read())
# with open('sample.json') as json_file:
#     data = json.load(json_file)

# print(list(findkey('title', data, [])))
# temp = list(findkey('title', data, []))[0]
# print(list(findkeyvalue("title", data, [], "Sayings of the Century")))
# print(list(findallvalues('title', data)))
