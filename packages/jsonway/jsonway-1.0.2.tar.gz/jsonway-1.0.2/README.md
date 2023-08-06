# JSONWAY

Jsonway is the one stop to manage the JSON using the python . All the operations can be done using the JSONway .

### Installation

```
pip install jsonway
```

### Usage 

Sample JSON
```
{
  "store": {
    "book": [
      {
        "category": "reference",
        "author": "Nigel Rees",
        "title": "Sayings of the Century",
        "price": 8.95
      },
      {
        "category": "fiction",
        "author": "Evelyn Waugh",
        "title": "Sword of Honour",
        "price": 12.99
      }
    ],
    "bicycle": {
      "color": "red",
      "price": 19.95
    }
  },
  "expensive": 10
}
```

Lets say , we have to find the nested key author in the above JSON 

```
import json
from jsonway.mainjsonway import *
with open('sample.json') as json_file:
    data = json.load(json_file)

print(list(findkey('author', data, []))) 
# output :[['store', 'book', 0, 'author'], ['store', 'book', 1, 'author'], ['store', 'book', 2, 'author'], ['store', 'book', 3, 'author']]

```


if you want to find the key and  value then 

```
print(list(findkeyvalue("title", data, [], "Sayings of the Century")))
```

if you want to find value then 

```
print(list(findvalue("Sayings of the Century", data, [])))
```

if you want to get the value from a path  then 
the path must be in the list form

```
getFromDict(data, ['store', 'book', 0, 'author'])
```
if you want to set the value at a particular key  then 
```
setInDict(dataDict, mapList, value)
```
to find all the keys  values then

```
print(list(findallvalues('title', data)))
output : ['Sayings of the Century', 'Sword of Honour', 'Moby Dick', 'The Lord of the Rings']
```


