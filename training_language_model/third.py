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
    freq_4gram = defaultdict(int)
    context_freq_4gram = defaultdict(int)
    contexts_4gram = defaultdict(set)
    discount_4gram = defaultdict(float)
    numofcontextwithfrequency_4gram = defaultdict(int)

    freq_3gram = defaultdict(int)
    context_freq_3gram = defaultdict(int)
    contexts_3gram = defaultdict(set)
    discount_3gram = defaultdict(float)
    numofcontextwithfrequency_3gram = defaultdict(int)

    freq_2gram = defaultdict(int)
    context_freq_2gram = defaultdict(int)
    contexts_2gram = defaultdict(set)
    discount_2gram = defaultdict(float)
    numofcontextwithfrequency_2gram = defaultdict(int)
    # if verbose:
        # print("Calculating fourgram count")




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
            if(words[i+3] == '' or words[i+3] == ' ' or words[i+3] == None):
                words.remove(words[i+3])
                continue
            total_words +=1 
            if(frequency_of_word[words[i+3]]<3):
                words[i+3]="<unk>"
            if(words[i+3] == '</s>'):
                continue
            context = tuple(words[i:i+3])
            word = words[i+3]
            freq_4gram[(context, word)] += 1
            context_freq_4gram[context] += 1
            contexts_4gram[word].add(context) 
        

        #data for 3 gram
        words = sentence.split()
        words = ['<s>'] * 2 + words + ['</s>']
        
        if words[0] == '<s>'and words[1]=='<s>' and words[2] == '</s>':
            words.remove(words[0])
            words.remove(words[0])
            words.remove(words[0])
        # print(words)
        if(len(sentence) == 0):
            continue
        # words = [word for word in words if word != '']
        for i in range(len(words)-2):
            if(words[i+2] == ''  or words[i+2] == ' ' or words[i+2] == None):
                words.remove(words[i+2])
                continue
            if(frequency_of_word[words[i+2]]<3):
                words[i+2]="<unk>"
            if(words[i+2] == '</s>'):
                continue
            context = tuple(words[i:i+2])
            word = words[i+2]
            print("***************")
            print(context , word )
            # freq_3gram.setdefault((context, word), 0)
            freq_3gram[(context, word)] += 1
            print(freq_3gram[(context, word)])
            context_freq_3gram[context] += 1
            contexts_3gram[word].add(context)



        #data for 2 gram
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


        
        for i in range(len(words)-1):
            if(words[i+1] == '' or words[i+1] == ' ' or words[i+1] == None):
                words.remove(words[i+1])
                continue 
            if(frequency_of_word[words[i+1]]<3):
                words[i+1]="<unk>"
            if(words[i+1] == '</s>'):
                continue
            context = tuple(words[i:i+1])
            word = words[i+1]
            freq_2gram[(context, word)] += 1
            context_freq_2gram[context] += 1
            contexts_2gram[word].add(context)
    
    
    #caclculating valuof numofcontextwithfrequency_4gram
    for context in context_freq_4gram:
        count = context_freq_4gram[context]
        numofcontextwithfrequency_4gram[count] += 1

    #caclculating valuof numofcontextwithfrequency_3gram
    for context in context_freq_3gram:
        count = context_freq_3gram[context]
        numofcontextwithfrequency_3gram[count] += 1

    #caclculating valuof numofcontextwithfrequency_2gram
    for context in context_freq_2gram:
        count = context_freq_2gram[context]
        numofcontextwithfrequency_2gram[count] += 1

    #calculating discount value for 4-gram
    
   
        # count = context_freq_4gram[context]
    a = numofcontextwithfrequency_4gram[1]/(numofcontextwithfrequency_4gram[1]+2*numofcontextwithfrequency_4gram[2])
        #discount value for 4-gram
    
    discount_4gram_constant = min(1 , 4 - (5*a* numofcontextwithfrequency_4gram[5]/numofcontextwithfrequency_4gram[4]))


    #calculating discount value for 3-gram
    
    b = numofcontextwithfrequency_3gram[1]/(numofcontextwithfrequency_3gram[1]+2*numofcontextwithfrequency_3gram[2])
    discount_3gram_constant = min(1 , 3 - (4*b* numofcontextwithfrequency_3gram[4]/numofcontextwithfrequency_3gram[3]))

    #calculating discount value for 2-gram
    c = numofcontextwithfrequency_2gram[1]/(numofcontextwithfrequency_2gram[1]+2*numofcontextwithfrequency_2gram[2])
    discount_2gram_constant = min(1 , 2 - (3*c* numofcontextwithfrequency_2gram[3]/numofcontextwithfrequency_2gram[2]))

    #calculating discount value for 4-gram
    

    for context in context_freq_3gram:
        count = context_freq_3gram[context]
        discount_3gram[context] = min(1 , count/count +2.0)
        
        #calculating discount value for 2-gram  

    for context in context_freq_2gram:
        count = context_freq_2gram[context]
        discount_2gram[context] = min(1 , count/count +2.0*freq_2gram[(context,)])    


        

    # print(contexts_4gram)
    # print(discount_4gram)
    # print(freq_4gram)
    # print(context_freq_4gram)
    # print(contexts_3gram)
    # print(discount_3gram)
    print(freq_3gram)
    # print(context_freq_3gram)
    # print(contexts_2gram)
    # print(discount_2gram)

    # print(freq_2gram)
    # print(total_words)

    def kn_4gram_prob(context, word):
        numerator = freq_4gram[(context, word)] - discount_4gram_constant
        denominator = context_freq_4gram[context]
        lamda = discount_4gram_constant / context_freq_4gram[context]
        if denominator == 0:
            return discount_4gram_constant* kn_3gram_backoff(context[1:], word)
        return numerator/denominator + lamda *kn_3gram_backoff(context[1:], word)
            # print(context ,word)
    def kn_3gram_backoff(context, word):
        numerator = freq_3gram[(context, word)] - discount_3gram_constant
        denominator = context_freq_3gram[context]
        lamda = discount_3gram_constant / context_freq_3gram[context]
        if denominator == 0:
            return discount_3gram_constant* kn_2gram_backoff(context[1:], word)
        return numerator/denominator + lamda *kn_2gram_backoff(context[1:], word)
    


    def kn_2gram_backoff(context, word):
        numerator = freq_2gram[(context, word)] - discount_2gram_constant
        denominator = context_freq_2gram[context]
        lamda = discount_2gram[context] / context_freq_2gram[context]
        if denominator == 0:
            return discount_2gram_constant* kn_1gram_backoff(word)
        return numerator/denominator + lamda *kn_1gram_backoff(word)
    
    def kn_1gram_backoff(word):
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
    # def perplexity_kneser():
    #     perplexity = 0
    #     for sentence in sentences:
            


            
    #     return perplexity
    
    return kn_4gram_prob , perplexity_kneser


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


    sentences , freq , tokens = tokenize("Corpus/Ulysses - James Joyce.txt")
    # sentences , freq , tokens = tokenize("sample.txt")

    # sentences = tokenize("Corpus/Ulysses - James Joyce.txt")['sentences']
    # freq = tokenize("Corpus/Ulysses - James Joyce.txt")['freq']
    # tokens = tokenize("Corpus/Ulysses - James Joyce.txt")['tokens']
    kn_4gram_prob=fourgram_prob(sentences,freq,tokens )

    print(kn_4gram_prob(('<s>', 'i', 'like'), 'to'))
    print(kn_4gram_prob(('<s>', '<s>', '<s>'), 'the'))

