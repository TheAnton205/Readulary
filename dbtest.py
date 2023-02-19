from pymongo import MongoClient
import random

client = MongoClient("mongodb+srv://anthonysharonov:awesome132@cluster0.kyrgb3n.mongodb.net/?retryWrites=true&w=majority")

db = client.get_database('vocabulary')
words = db.words

new_word = {
    'word':'test1',
    'meaning':'test2'
}

new_word2 = {
    'word':'test3',
    'meaning':'test4'
}

# #print(words.find_one(new_word2))
# #print(type(words.find_one(new_word2)))


# if words.find_one(new_word2) is None:
#     print("sending")

# else:
#     print("exists!")

#words.insert_one(new_word)
#a = words.find_one({'word':'asdasdasd'})
#print(a)

#b = a.get('meaning')

#print(b)

count = words.count_documents({})
a = words.find()[random.randrange(count)]
b = a.get('meaning')
print(b)
