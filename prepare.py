# read the index.txt and each problem description and prepare documents, vocab , idf
# "idf-values" file stores in how many documents the word occurred
# documents is a list of lists where in each list it stores all the words concerned to a problem(may include duplicates)
import os
import re

def get_kth_line(file_path, k):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            if line_number == k:
                return line.strip()  # Remove leading and trailing whitespace, including '\n'
    return None  # Handle case where the line number is out of range

def get_words2(document_text):
    # remove the leading numbers from the string, remove not alpha numeric characters, make everything lowercase
    terms = [term.lower() for term in document_text.strip().split()[1:]]
    return terms

def get_words1(paragraph):
    words = []
    lines = paragraph.split("\n")  # Split the paragraph into lines
    for line in lines:
        line = line.strip()  # Remove leading and trailing whitespace including '\n'
        line_words = line.split()  # Split the line into words
        for word in line_words:
            word = re.sub(r'[.,]+$', '', word)  # Remove full stops and commas from the end
            words.append(word.lower())  # Convert word to lowercase and add it to the list
    return words

# search in every problem till you reach the word "Example" and add the list of words to the documents
target_word = "Example"
QDATA_FOLDER = "../Qdata"
# we store the list of words of every problem in documents
documents = []
body=""
vocab = {}    # vocab stores each unique word to the number of documents it is present in
file_path2 = os.path.join(QDATA_FOLDER, "index.txt")
for index in range(1,2156):
    file_name = str(index)
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    # file_path of every problem description
    file_path1 = os.path.join(folder_path, file_name + ".txt")
    with open(file_path1, "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if target_word not in line:
                body += line
            else:
                break
    line2 = get_kth_line(file_path2, index)     # get the title of that problem
    words_from_title = get_words2(line2)        # get the words from the title
    words_from_body = get_words1(body)                   # get the words from the problem's body
    total_words = words_from_title + words_from_body
    documents.append(total_words)               # appends all the words(duplicates can be present) of a problem
    total_words = set(total_words)              # removing the duplicates
    body = ""
    for word in total_words:
        if word not in vocab:
            vocab[word] = 1
        else:
            vocab[word] += 1


# reverse sort the vocab by the values
vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))

# save the vocab(list of all unique words) in a text file
with open('./vocab.txt', 'w', encoding='utf-8') as f:
    for key in vocab.keys():
        f.write("%s\n" % key)

# save the idf values in a text file
with open('./idf-values.txt', 'w', encoding='utf-8') as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

# save the documents in a text file
with open('./documents.txt', 'w', encoding='utf-8') as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))


inverted_index = {}      # a dictionary which stores every word to the list of documents it is occurring in
for index, document in enumerate(documents):    # duplicates may be present in document
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

# save the inverted index in a text file
with open('./inverted-index.txt', 'w', encoding='utf-8') as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))