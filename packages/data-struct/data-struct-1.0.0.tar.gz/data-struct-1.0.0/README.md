# data-struct

structLib is essentially a module which contains the _Struct_ class. This class is specifically
aimed at making your life easier when working with JSON-like objects (meaning nested
_dict_ / _list_ objects)

## Installation

To install structLib on your python setup, run the following:
```bash
pip install data-struct
```
On linux or mac you will probably need to run this command instead:
```bash
python3 -m pip install data-struct
```
Please note that version 3.8 (or higher) of python is required to run this library!

## Usage

Let's have closer look at what we can do with this library and how...
If you take a look at the code or the help module you will notice that the _Struct_ class isn't the only element in there.
There is indeed a bunch of other functions defined. The only reason these functions are not part of the class is because 
they work using recursive algorithms, therefore it was way easier to implement them outside and then simply call them from 
the class methods when needed. Note that you **should not** be using those functions, the _Struct_ class handles all of that for you.

### Example

Now let's look at some code shall we? The following code can be found in the examples folder.
```python
# This code aims to illustrate how we can use structLib
from structLib import Struct

# You will notice I only import the Struct class, the reason in because it's the only thing actually useful for
# us

with open("actors.json") as f_in:
    data = Struct.load(f_in)  # First we load the data into a Struct object.

print(data, '\n')

"""Let's say I want to see if "Tom Cruise" is present in the data structure
I could use the Struct.isValueIn() method but if I want to know where the value is, there is a better option
"""

path = data.pathToValue("Tom Cruise")  # If the value doesn't exist in the Struct, the result will be None
print(path)

# Now I want to get his age:

age = data["Actors", 0, 'age']
print(age, '\n')

# The value is wrong let's fix that
data["Actors", 0, "age"] = 58

# Let's add Jonny Depp in there
jonny = {
    "name": "Jonny Depp",
    "age": 57,
    "Born At": "Owensboro, Kentucky",
    "Birthdate": "June 9, 1963",
    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Johnny_Depp_Deauville_2019.jpg/390px"
             "-Johnny_Depp_Deauville_2019.jpg",
}

data['Actors'].append(jonny)

print(data, '\n')

# Let's say I want to print the ages of everyone:
for a in data.getAll("age"):
    print(a)

# Now let's sort them by age
data['Actors'] = Struct(data['Actors']).sorted(path="age").data
# Here I have to do this complicated mess because the list isn't at the top level of the structure but rather 
# under the "Actors" key
print(data)

# Finally let's write that back into the file
with open("sorted_actors.json", 'w') as f_out:
    data.dump(f_out, indent=4)
```
### Iterating through a Struct

The `for` syntax works perfectly with _Struct_ objects but the behavior depends on what type of data we have. If `self.data` is a list,
`for element in struct_object` will work exact way as for a regular list object, no mystery there.\
However if `self.data` is a dictionary, then `element` will be a tuple containing the key, and the corresponding value.

### The sorted/sort methods

Those are interesting. The only difference between the two is that the `sort` method modifies the object directly and returns nothing, while the `sorted` method 
returns the sorted version of the object but leaves the original as is. Aside from that the behavior is exactly the same. With that out of the way, let's look at the 
interesting in part

Usage:
```python
struct_object.sort(path=None, function=lambda x:x)
```

The `path` argument specifies which value should be prioritized to run the sort.\
The `function` is a function that will be executed on the value. The default is `lambda x:x`, which is a function that does explicitly nothing to the value it receives.

The behavior of the sort will depend on what type of data you have. Indeed, the `self.data` attribute can either be a _list_ or a _dict_ object.\
We then have four possible situations:
- If it's a list and `path` is `None`, the list will be sorted directly based on the values it contains.
- If it's a list and `path` is specified, the list will be sorted based on the value which corresponds to `path` in each element on the list. 
- If it's a dict and `path` is `None`, the dict will be sorted based on the **keys**.
- If it's a dict and `path` is specified, the dict will be sorted based on the value corresponding to the path in each element of the dict.

Let's give an example:
````python
from structLib import Struct
from datetime import datetime

def parseDate(string):
    content = [int(x) for x in string.split('-')]
    return datetime(year=content[2], month=content[1], day=content[0])

data = Struct({
    "10-08-2020": {'id': 2},
    "7-08-2020": {'id': 1},
    "1-07-2020": {'id': 3}
})

def test1():
    # Sort by date
    data.sort(function=parseDate)
    assert data.getAll("id") == [3, 1, 2]

def test2():
    # Sort by id
    data.sort('id')
    assert data.getAll("id") == [1, 2, 3]

# now if it's a list
data2 = Struct([1, 8, 3])

def test3():
    # Note that using Struct for a simple list like this is pointless
    assert [x for x in data2.sorted()] == [1, 3, 8]

data3 = Struct(
    [
        {"date": "10-08-2020"},
        {"date": "7-08-2020"},
        {"date": "1-07-2020"}
    ]
)

def test4():
    data3.sort("date", parseDate)
    assert [x["date"] for x in data3] == ["1-07-2020", "7-08-2020", "10-08-2020"]
````
## Requirements

None! That's also what is cool about it! 

## Authors

[EddieBreeg](https://github.com/EddieBreeg)
