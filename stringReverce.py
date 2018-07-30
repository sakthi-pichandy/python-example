#Reverse a sentence

def reverseSentence(str):
    words = str.split(" ")   # Spliting the Sentence into list of words.
    
    # Reversing each word and creating
    # a new list of words
    # List Comprehension Technique
    newWords = [word[::-1] for word in words]
    
    # Joining the new list of words
    # to for a new Sentence
    newSentence = " ".join(newWords)
    return newSentence

str = input("Please enter the string to reverse :  ")
print (reverseSentence(str))
