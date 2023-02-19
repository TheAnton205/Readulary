from PyDictionary import PyDictionary
dictionary=PyDictionary()

list1 = ["ant","bug","carrot"]
dict = {}

for i in list1:
    mean = dictionary.meaning(i)
    list2 = list(mean.values())[0]
    meaning = list2[0]
    dict[i] = meaning

print(dict.get("ant"))

