from Tokenizer import *
from collections import defaultdict
import math
import argparse

def fourgram_prob(sentences,frequency_of_word,tokens,verbose =False  ):
    
    fourgram_count = {}
    frequency_of_word["<s>"] = 3*len(sentences)
    frequency_of_word["</s>"] = len(sentences)
    print(frequency_of_word["<UNK>"])
    total_words = 0
    if verbose:
        print("Calculating fourgram count")



    freq = defaultdict(int)
    context_freq = defaultdict(int)
    contexts = defaultdict(set)
    discount = defaultdict(float)


    #data for 4-gram
    for sentence in sentences:


        # print(sentence)

        words = sentence.split()
        words = ['<s>'] * 3 + words + ['</s>']
        if words[0] == '<s>'and words[1]=='<s>' and words[2]=='<s>' and words[3] == '</s>':
        #remove empty strings
        #remove words words at inde x
            words.remove(words[0])
            words.remove(words[0])
            words.remove(words[0])
            words.remove(words[0])
        # print(words)

        if(len(sentence) == 0):
            #remove emtpty sentences
            sentences.remove(sentence)
            continue


        words = [word for word in words if word != '']
        for i in range(len(words)-3):
            total_words +=1 
            if(frequency_of_word[words[i+3]]<2):
                words[i+3]="<unk>"
            if(words[i+3] == '</s>'):
                continue
            context = tuple(words[i:i+3])
            word = words[i+3]
            freq[(context, word)] += 1
            context_freq[context] += 1
            contexts[word].add(context) 
            # print(words[i+3])


    #calculating discount value for 4-gram

    for context in context_freq:
        count = context_freq[context]
        discount[context] = min(1 , count/count +2.0*freq[(context,)])



    #data for 3 gram
    for sentence in sentences:

        words = sentence.split()
        words = ['<s>'] * 2 + words + ['</s>']
        
        if words[0] == '<s>'and words[1]=='<s>' and words[2] == '</s>':
        #remove empty strings
        #remove words words at inde x
            words.remove(words[0])
            words.remove(words[0])
            words.remove(words[0])
        # print(words)

        if(len(sentence) == 0):

            continue


        words = [word for word in words if word != '']
        for i in range(len(words)-2):
            if(words[i+2] == '</s>'):
                continue
            context = tuple(words[i:i+2])
            word = words[i+2]
            freq[(context, word)] += 1
            context_freq[context] += 1
            contexts[word].add(context)

    #calculating discount value for 3-gram
    

    for context in context_freq:
        count = context_freq[context]
        discount[context] = min(1 , count/count +2.0*freq[(context,)])
        
    #data for 2 gram
    for sentence in sentences:    

        words = sentence.split()
        words = ['<s>'] + words + ['</s>']
        if words[0] == '<s>' and words[1] == '</s>':
        #remove empty strings
        #remove words words at inde x
            words.remove(words[0])
            words.remove(words[0])
        # print(words)

        if(len(sentence) == 0):
            continue


        words = [word for word in words if word != '']
        for i in range(len(words)-1):
            if(words[i+1] == '</s>'):
                continue
            context = tuple(words[i:i+1])
            word = words[i+1]
            freq[(context, word)] += 1
            context_freq[context] += 1
            contexts[word].add(context)

        #calculating discount value for 2-gram  
        # discount = defaultdict(float) 

        for context in context_freq:
            count = context_freq[context]
            discount[context] = min(1 , count/count +2.0*freq[(context,)])     

        #data for unigram 
        for sentence in sentences:

            words = sentence.split()
         
            #remove empty strings
            #remove words words at inde x

            if(len(sentence) == 0):
                continue


            words = [word for word in words if word != '']


                # context = tuple(words[i:i])
                # word = words[i]
                # freq[(context, word)] += 1
                # context_freq[context] += 1
                # contexts[word].add(context)


    print(contexts)
    print(discount)
    print(freq)
    print(context_freq)

    def kn_4gram_prob(context, word):
        numerator = freq[(context, word)] - discount[context]
        denominator = context_freq[context]
        lamda = discount[context] / context_freq[context]
        if denominator == 0:
            return discount[context]* kn_3gram_backoff(context[1:], word)
        return numerator/denominator + lamda *kn_3gram_backoff(context[1:], word)
            # print(context ,word)
    def kn_3gram_backoff(context, word):
        numerator = freq[(context, word)] - discount[context]
        denominator = context_freq[context]
        lamda = discount[context] / context_freq[context]
        if denominator == 0:
            return discount[context]* kn_2gram_backoff(context[1:], word)
        return numerator/denominator + lamda *kn_2gram_backoff(context[1:], word)
    


    def kn_2gram_backoff(context, word):
        numerator = freq[(context, word)] - discount[context]
        denominator = context_freq[context]
        lamda = discount[context] / context_freq[context]
        if denominator == 0:
            return discount[context]* kn_1gram_backoff(word)
        return numerator/denominator + lamda *kn_1gram_backoff(word)
    
    def kn_1gram_backoff( word):
        if(word not in frequency_of_word):
            return frequency_of_word['<UNK>']/total_words
        else:
            
            return frequency_of_word[word]/total_words


    # def kn_recurse_backoff(context, word):
    #     # print(context ,word)

    #     if len(context) == 3:
    #         return kn_4gram_prob(context, word)
    #     elif len(context) == 2:
    #         return kn_3gram_backoff(context, word)
    #     elif len(context) == 1:
    #         return kn_2gram_backoff(context, word)
    #     else:
    #         return kn_1gram_backoff(context, word)

    # def kn_4gram_logscore(sentence):
        
    #     tokens = sentence.split()
    #     padded_tokens = ['<s>', '<s>', '<s>'] + tokens + ['</s>']
    #     logprob = 0.0
    #     for i in range(len(padded_tokens) - 3):
    #         context = tuple(padded_tokens[i:i+3])
    #         token = padded_tokens[i+3]
    #         logprob += math.log(kn_recurse_backoff(context, token))
    #     return logprob
    
    return kn_4gram_prob


#written bell smoothing function
def bell_smoothing(sentences, verbose =False ):
        
        fourgram_count = {}
    
        if verbose:
            print("Calculating fourgram count")
    
    
        freq = defaultdict(int)
        context_freq = defaultdict(int)
        contexts = defaultdict(set)
    
        for sentence in sentences:
            # print(sentence)
            words = sentence.split()
            words = ['<s>'] * 3 + words + ['</s>']
    
            #remove consecutive <s> and </s>
            # words = [word for word in words if word != '']
            if words[0] == '<>'and words[1]=='<s>' and words[2]=='<s>' and words[3] == '</s>':
            #remove empty strings
            #remove words words at inde 
                words.remove(words[0])
                words.remove(words[0])
                words.remove(words[0])
                words.remove(words[0])
            print(words)
    
            if(len(sentence) == 0):
                continue
    
    
            words = [word for word in words if word != '']
            for i in range(len(words)-3):
                if(words[i+3] == '</s>'):
                    continue
                context = tuple(words[i:i+3])
                word = words[i+3]
                freq[(context, word)] += 1
                context_freq[context] += 1
                contexts[word].add(context)
                

#main function
if __name__ == "__main__":

    sentences = tokenize("Corpus/Ulysses - James Joyce.txt")['sentences']
    freq = tokenize("Corpus/Ulysses - James Joyce.txt")['freq']
    tokens = tokenize("Corpus/Ulysses - James Joyce.txt")['tokens']
    kn_4gram_prob=fourgram_prob(sentences,freq,tokens )

    print(kn_4gram_prob(('<s>', '<s>', '<s>'), 'the'))
