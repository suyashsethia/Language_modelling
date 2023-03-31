from Tokenizer import *
from collections import defaultdict
import math
import argparse

all_kn_prob = []

def fourgram_prob(sentences,frequency_of_word,arg,verbose =False  ):
    


    #divide the data into trainig and test randomly 

    training_data_sentences = sentences[:int(len(sentences)*0.5)]
    test_data_sentences = sentences[int(len(sentences)*0.5):]
    
    fourgram_count = {}
    frequency_of_word["<s>"] = 3*len(training_data_sentences)
    frequency_of_word["</s>"] = len(training_data_sentences)
    # print(frequency_of_word["<UNK>"])
    vocab_size = len(frequency_of_word)
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
    # training_data_sentences = sentences[:int(len(sentences)*0.8)]

    for sentence in training_data_sentences:


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
            training_data_sentences.remove(sentence)
            continue


        words = [word for word in words if word != '']

        for i in range(len(words)-3):
            if(words[i+3] == '' or words[i+3] == ' ' or words[i+3] == None):
                words.remove(words[i+3])
                continue
            total_words +=1 
            if(words[i+3] == '</s>'):
                continue
            context = tuple(words[i:i+3])
            word = words[i+3]
            freq_4gram[(context, word)] += 1
            context_freq_4gram[context] += 1
            contexts_4gram[context].add(word) 
        

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
            if(words[i+2] == '</s>'):
                continue
            context = tuple(words[i:i+2])
            word = words[i+2]
            # print("***************")
            # print(context , word )
            # freq_3gram.setdefault((context, word), 0)
            freq_3gram[(context, word)] += 1
            # print(freq_3gram[(context, word)])
            context_freq_3gram[context] += 1
            contexts_3gram[context].add(word)



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
            if(words[i+1] == '</s>'):
                continue
            context = tuple(words[i:i+1])
            word = words[i+1]
            freq_2gram[(context, word)] += 1
            context_freq_2gram[context] += 1
            contexts_2gram[context].add(word)
    
    
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

    d = numofcontextwithfrequency_2gram[1]/(numofcontextwithfrequency_2gram[1]+2*numofcontextwithfrequency_2gram[2])
    discount_1gram_constant = min(1 , 1 - (2*d* numofcontextwithfrequency_2gram[2]/numofcontextwithfrequency_2gram[1]))
    #calculating discount value for 4-gram
    
    if(arg=="kn"):


        def kn_4gram_prob(context, word):
            numerator = max(freq_4gram[(context, word)] - discount_4gram_constant,0)
            denominator = context_freq_4gram[context]
            if denominator == 0:
                return (discount_4gram_constant/len(frequency_of_word))* kn_3gram_backoff(context[1:], word)
            lamda = len(contexts_4gram[context])*discount_4gram_constant / context_freq_4gram[context]
            return numerator/denominator + lamda *kn_3gram_backoff(context[1:], word)
                # print(context ,word)
        def kn_3gram_backoff(context, word):
            numerator =  max(0 ,freq_3gram[(context, word)] - discount_3gram_constant)
            denominator = context_freq_3gram[context]
            if denominator == 0:
                return (discount_3gram_constant/len(frequency_of_word))* kn_2gram_backoff(context[1:], word)
            lamda = discount_3gram_constant*len(contexts_3gram[context]) / context_freq_3gram[context]
            return numerator/denominator + lamda *kn_2gram_backoff(context[1:], word)
        


        def kn_2gram_backoff(context, word):
            numerator = max(0,freq_2gram[(context, word)] - discount_2gram_constant)
            denominator = context_freq_2gram[context]
            if denominator == 0:
                return (discount_2gram_constant/len(frequency_of_word))* kn_1gram_backoff(word)
            lamda = discount_2gram_constant*len(contexts_2gram[context]) / context_freq_2gram[context]
            return numerator/denominator + lamda *kn_1gram_backoff(word)
        
        def kn_1gram_backoff( word):
            

            if(word not in frequency_of_word):
                return 0.000000009
                # return frequency_of_word['<UNK>']/total_words
            else:
                
                return  frequency_of_word[word]/total_words
        return kn_4gram_prob 
    if(arg=="wb"):
        #written -bell smoothing

        def wb_4_gram(context,word):
            numerator = freq_4gram[(context, word)]
            denominator = context_freq_4gram[context] 
            if denominator+ len(contexts_4gram[context]) == 0:
                lamda = 0 
                return (1-lamda)*wb_3gram_backoff(context[1:], word)
            g = (len(contexts_4gram[context])/((len(contexts_4gram[context])) + denominator ))
            lamda = 1 - g
            return lamda*numerator/denominator + (1-lamda)*wb_3gram_backoff(context[1:], word) 


        def wb_3gram_backoff(context, word):
            numerator = freq_3gram[(context, word)]
            denominator = context_freq_3gram[context] 
            if denominator + len(contexts_3gram[context]) == 0:
                lamda = 0 
                return (1-lamda)*wb_2gram_backoff(context[1:], word)
            lamda = 1 -(len(contexts_3gram[context])/((len(contexts_3gram[context])) + denominator ))
            return (lamda*numerator/denominator) + (1-lamda)*wb_2gram_backoff(context[1:], word)
        
        def wb_2gram_backoff(context, word):
            numerator = freq_2gram[(context, word)]
            denominator = context_freq_2gram[context] 
            if denominator + len(contexts_2gram[context]) == 0:
                lamda = 0 
                return (1-lamda)*wb_1gram_backoff(word)
            lamda = 1 -(len(contexts_2gram[context])/((len(contexts_2gram[context])) + denominator ))
            return (lamda*numerator/denominator) + (1-lamda)*wb_1gram_backoff(word)


        def wb_1gram_backoff(word):
            c_of_word = frequency_of_word[word]
            prob_ml = c_of_word/total_words
            n_0 = len(frequency_of_word)
            prob = (prob_ml*total_words)/(total_words+ n_0) + (1/(c_of_word+n_0))
            return prob 
            

        return wb_4_gram
    
    

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
    # 


    # def perplexity_kneser():
    #     perplexity = 0
    #     for sentence in training_data_sentences:
    #         print("fd")
            


    #     hi = 0 
    #         return perplexity
    

def perplexity_kn(n , tokenised_curpus ,all_probs,log_prob_kn):
    all_perplexity =[]
    for sentence in tokenised_curpus:
        per = 0
        for i in range(len(sentence)-n+1):
            if(tuple(sentence[i:i+n]) in all_probs.keys()):
                per+=log_prob_kn[tuple(sentence[i:i+n])]
            else:
                per=101
        
        per/=(len(sentence) - n+1)
        per*=-1
        per = math.exp(per)
        print(per)
        all_perplexity.append(per)
    return all_perplexity

def perplexity_wb(n , tokenised_curpus ,all_probs,log_prob_wb):
    all_perplexity =[]
    for sentence in tokenised_curpus:
        per = 0
        for i in range(len(sentence)-n+1):
            if(tuple(sentence[i:i+n]) in all_probs.keys()):
                per+=log_prob_wb[tuple(sentence[i:i+n])]
            else:
                per=101
        
        per/=(len(sentence) - n+1)
        per*=-1
        per = math.exp(per)
        print(per)
        all_perplexity.append(per)
    return all_perplexity



#main function
if __name__ == "__main__":


    sentences , freq , tokens = tokenize("Corpus/Ulysses - James Joyce.txt")
    # sentences , freq , tokens = tokenize("sample.txt")

    log_pb ={}
    log_pb_wb ={}
    f ={}
    f_wb ={}


    

    gram_prob=fourgram_prob(sentences,freq,"kn" )
    # gram_prob_wb=fourgram_prob(sentences,freq,"wb" )

     
    # print(gram_prob(('<s>', 'i', 'like'), 'to'))
    training_data_sentences = sentences[:int(len(sentences)*0.5)]
    
    list = []
    for sentence in training_data_sentences:

        #make a list of list of words

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
        list.append(words)

        if(len(sentence) == 0):
            training_data_sentences.remove(sentence)
                    # continue
        words = [word for word in words if word != '']
        import math 
        for i in range(len(words)-3):
            if(words[i+3] == '' or words[i+3] == ' ' or words[i+3] == None):
                words.remove(words[i+3])
                continue
            if(words[i+3] == '</s>'):
                continue
            context = tuple(words[i:i+3])
            word = words[i+3]
            # print(context,word)
            # print(gram_prob(context,word))
            list_k = []
            for k in context:
                list_k.append(k)
            list_k.append(word)
            t_kn = gram_prob(context,word)
            # t_wb = gram_prob_wb(context,word)

            # print(t)
            f.update({tuple(list_k):t_kn})
            # f_wb.update({tuple(list_k):t_wb})
            log_pb.update({tuple(list_k):math.log(t_kn)})
            # log_pb_wb.update({tuple(list_k):math.log(t_wb)})

            

            # prob = {"context":context , "word":word, "probability":gram_prob(context ,words) }
            # print(prob)
            # all_kn_prob.append(prob)


    
    # print(f.keys())
    perplexity_kn = perplexity_kn(4,list,f,log_pb)
    # perplexity_wb = perplexity_wb(4,list,f_wb,log_pb_wb)
    # print(perplexity_kn)
    print(perplexity_wb)
    print('perplexity of the corpus for kn ', sum(perplexity_kn)/len(perplexity_kn))
    # print('perplexity of the corpus for wb ', sum(perplexity_wb)/len(perplexity_wb))

    # print((log_pb))


    # print(gram_prob(('<fcs>', '<fs>', 'gfd'), 'gfd' ))

    
