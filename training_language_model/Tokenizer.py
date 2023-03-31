import re 
# from smoothings import default, kneser_ney, witten_bell

    

def tokenize(file):
    f=open(file, 'r')
    text=f.read()

    #remove all special characters except @,#,.,?!
    text = re.sub(r'[^\@\#\.\w\?\!\s]', '', text)
    #remove all extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n*', '', text)
    text = re.sub(r'\.+', '.', text)

    #remove . from  abbrevations 
    f = re.compile(r'([A-Z]([a-z]){,2}\.)')
    a = re.findall(f, text)
    if(a):
        abbrevations_set = set((list(zip(*a))[0]))

        for word in abbrevations_set:
            text = text.replace(word, word.strip('.'))
        



    # Replace hashtags with <HASHTAG>
    text = re.sub(r'#\w+', '<HASHTAG>', text)

    #replace @ with <MENTION>
    
    text = re.sub(r'@\w+', '<MENTION>', text)


    #replace http with <URL>
    text = re.sub(r'http\S+', '<URL>', text)
    
    #replace www with <URL> 
    text = re.sub(r'www\S+', '<URL>', text)

    #replace Date with <DATE>
    text = re.sub(r'\d{1,2}\/\d{1,2}\/\d{2,4}', '<DATE>', text)

    #replace Time with <TIME>
    text = re.sub(r'\d{1,2}:\d{2}', '<TIME>', text)

    #replace percentage with <PERCENT>
    text = re.sub(r'\d{1,3}\%', '<PERCENT>', text)

    # #replace comma with 
    # text = re.sub(r'\,', '', text)

    #replace number with <NUMBER>
    #replace one or more digits with <NUMBER> but not if it is a part of a word
    text = re.sub(r'\b\d+\b', '<NUMBER>', text)
    # text = re.sub('\d+', r'<NUMBER>', text)


    #replace _ with space
    text = re.sub(r'_', '', text)
    #change to lowercase
    text = text.lower()   

    # Split the text into sentences 
    sentences = re.split(r'[.!?]+', text)
    
    # Tokenize each sentence into words and add <s> and </s>
    tokens = []
    for i in range(len(sentences)):
        #remove punctuations and special characters
        sentence = sentences[i]
        sentence = re.sub(r'[^\w<>]', ' ', sentence)
        sentence = re.sub(r'\s+', ' ', sentence.strip())        
        sentences[i] = sentence
        words = sentence.split()
        words.insert(0, '<s>')
        words.append('</s>')

        tokens.extend(words)

    for i in range(len(tokens)):
        if tokens[i] == '<s>' and tokens[i+1] == '</s>':
            tokens[i] = ''
            tokens[i+1] = ''

    #remove a empty token from the list
    tokens = [token for token in tokens if len(token) > 0]

#replace words with <UNK> if they occur less than 2 times in the corpus

    freq = {}
    k=0
    for i in range(len(tokens)):
        if tokens[i] in freq:
            freq[tokens[i]] += 1
        else:
            freq[tokens[i]] = 1

    for i in range(len(tokens)):
        if freq[tokens[i]] < 3:
            k+=1
            # tokens[i] = '<UNK>'
        # print(tokens[i])    
    
    freq["<UNK>"] = k


    # print(tokens)






    # print(sentences)
    return sentences , freq, tokens

# return {"sentences":sentences , "freq":freq , "tokens":tokens}
# tokenize("Corpus/Ulysses - James Joyce.txt")










































    # Split corpus into sentences
    # sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    #remove empty sentences
    
    # sentences = [sentence for sentence in sentences if len(sentence) > 0]
    # print(sentences)
    #remove commas and question marks and full stops and exclamation marks and brackets and quotes

    #find word starting with http
    # re.findall(r'http\S+', text)
    


    # Split sentences into tokens
    # tokens = [re.split(r'(\W+)?', sentence) for sentence in sentences]

    
    # for sentence in sentences:
    #     for token in tokens:

    #         #find word starting with http
    #         if re.search(r'http\S+', token):
    #             print(token)
    #         #find word starting with www
    #     #find word starting with hashtag
    #         if re.search(r'#\w+', token):
    #             print(token)
    #         #find word starting with @
    #         if re.search(r'@\w+', token):
        
    #             print(token)
    # # Remove empty tokens

    # tokens = [token for token in tokens if len(token) > 0]
    # # print(tokens)

# re.find('jsfgjs')