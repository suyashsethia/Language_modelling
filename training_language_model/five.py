from Tokenizer import *
from collections import defaultdict
from math import log
import argparse
import sys

all_kn_prob = []

frequency_of_word = defaultdict(int)
total_words = 69
freq_4gram = defaultdict(int)
context_freq_4gram = defaultdict(int)
contexts_4gram = defaultdict(set)

freq_3gram = defaultdict(int)
context_freq_3gram = defaultdict(int)
contexts_3gram = defaultdict(set)


freq_2gram = defaultdict(int)
context_freq_2gram = defaultdict(int)
contexts_2gram = defaultdict(set)

discount_4gram_constant  = 0.9
discount_3gram_constant  = 0.8
discount_2gram_constant  = 0.7
 


def create_data(sentences , frequency_of_word,total_words,verbose =False):

    frequency_of_word["<s>"] = 3*len(sentences)
    frequency_of_word["</s>"] = len(sentences)

    vocab_size = len(frequency_of_word)
    # total_words = 0
    discount_4gram = defaultdict(float)
    numofcontextwithfrequency_4gram = defaultdict(int)

    discount_3gram = defaultdict(float)
    numofcontextwithfrequency_3gram = defaultdict(int)

    discount_2gram = defaultdict(float)
    numofcontextwithfrequency_2gram = defaultdict(int)

#data for 4-gram
    # training_data_sentences = sentences[:int(len(sentences)*0.8)]

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


    return total_words
    # #calculating discount value for 4-gram
    
   
    #     # count = context_freq_4gram[context]
    # a = numofcontextwithfrequency_4gram[1]/(numofcontextwithfrequency_4gram[1]+2*numofcontextwithfrequency_4gram[2])
    #     #discount value for 4-gram
    
    # discount_4gram_constant = min(1 , 4 - (5*a* numofcontextwithfrequency_4gram[5]/numofcontextwithfrequency_4gram[4]))


    # #calculating discount value for 3-gram
    
    # b = numofcontextwithfrequency_3gram[1]/(numofcontextwithfrequency_3gram[1]+2*numofcontextwithfrequency_3gram[2])
    # discount_3gram_constant = min(1 , 3 - (4*b* numofcontextwithfrequency_3gram[4]/numofcontextwithfrequency_3gram[3]))

    # #calculating discount value for 2-gram
    # c = numofcontextwithfrequency_2gram[1]/(numofcontextwithfrequency_2gram[1]+2*numofcontextwithfrequency_2gram[2])
    # discount_2gram_constant = min(1 , 2 - (3*c* numofcontextwithfrequency_2gram[3]/numofcontextwithfrequency_2gram[2]))

    # d = numofcontextwithfrequency_2gram[1]/(numofcontextwithfrequency_2gram[1]+2*numofcontextwithfrequency_2gram[2])
    # discount_1gram_constant = min(1 , 1 - (2*d* numofcontextwithfrequency_2gram[2]/numofcontextwithfrequency_2gram[1]))
    # #calculating discount value for 4-gram




def kn_model_4(context , word):
    numerator = max(freq_4gram[(context, word)] - discount_4gram_constant,0)
    denominator = context_freq_4gram[context]
    if denominator == 0:
        return (discount_4gram_constant/len(frequency_of_word))* kn_model_3(context[1:], word)
    lamda = len(contexts_4gram[context])*discount_4gram_constant / context_freq_4gram[context]
    return numerator/denominator + lamda *kn_model_3(context[1:], word)
        # print(context ,word)
def kn_model_3(context , word):
    numerator =  max(0 ,freq_3gram[(context, word)] - discount_3gram_constant)
    denominator = context_freq_3gram[context]
    if denominator == 0:
        return (discount_3gram_constant/len(frequency_of_word))* kn_model_2(context[1:], word)
    lamda = discount_3gram_constant*len(contexts_3gram[context]) / context_freq_3gram[context]
    return numerator/denominator + lamda *kn_model_2(context[1:], word)

def kn_model_2(context , word):
    numerator = max(0,freq_2gram[(context, word)] - discount_2gram_constant)
    denominator = context_freq_2gram[context]
    if denominator == 0:
        return (discount_2gram_constant/len(frequency_of_word))* kn_model_1(word)
    lamda = discount_2gram_constant*len(contexts_2gram[context]) / context_freq_2gram[context]
    return numerator/denominator + lamda *kn_model_1(word)

        
def kn_model_1(word):
        if(word in frequency_of_word):
            return frequency_of_word[word]/total_words 
        else:
            return (1/total_words)


def wb_model_4(context , word):
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
    n_0 = len(frequency_of_word)
    if(word in frequency_of_word.keys()):
        c_of_word = frequency_of_word[word]
        prob_ml = c_of_word/(total_words)
        prob = (prob_ml*total_words)/(total_words + n_0) + (1/(c_of_word+n_0))
        return prob 
    else:
        return 1/n_0

def perplexity_kn(n , tokenised_curpus , all_probs,log_prob_kn):
    all_perplexity =[]
    for sentence in tokenised_curpus:
        per = 0
        for i in range(len(sentence)-n+1):
            # print first 1000 keys of all_probs dictionary
            # if(i==0):
            # print(all_probs.keys()[:1000])
            if(tuple(sentence[i:i+n]) in all_probs.keys()):
                per+=log_prob_kn[tuple(sentence[i:i+n])]
            else:
                log_prob_kn.setdefault(tuple(sentence[i:i+n]), 0)
                log_prob_kn[tuple(sentence[i:i+n])] = math.log(kn_model_4(context=tuple(sentence[i:i+n-1]), word=sentence[i+n-1]))
                per+= log_prob_kn[tuple(sentence[i:i+n])]
        
        per/=(len(sentence) - n+1)
        per*=-1
        per = math.exp(per)
        # print(per)
        all_perplexity.append(per)
    return all_perplexity

def perplexity_wb(n , tokenised_curpus , all_probs,log_prob_wb):
    all_perplexity =[]
    for sentence in tokenised_curpus:
        per = 0

        for i in range(len(sentence)-n+1):
            if(tuple(sentence[i:i+n]) in all_probs.keys()):
                per+=log_prob_wb[tuple(sentence[i:i+n])]
            else:
                log_prob_wb.setdefault(tuple(sentence[i:i+n]), 0)
                log_prob_wb[tuple(sentence[i:i+n])] = math.log(wb_model_4(context=tuple(sentence[i:i+n-1]), word=sentence[i+n-1]))
                per+= log_prob_wb[tuple(sentence[i:i+n])]

        
        per/=(len(sentence) - n+1)
        per*=-1
        per = math.exp(per)
        all_perplexity.append(per)    
    return all_perplexity 


if __name__ == "__main__":

    args = sys.argv
    model = args[1]
    file = args[2]
    file_path = "Corpus/" + file
    if(file == 'Ulysses'):
        file_path = "Corpus/Ulysses - James Joyce.txt"
    elif(file == 'Pride'):
        file_path = "Corpus/Pride and Prejudice - Jane Austen.txt"


    sentences  , frequency_of_word , tokens = tokenize(file_path)
    training_data_sentences = sentences[:int(len(sentences)*0.8)]
    test_data_sentences = sentences[int(len(sentences)*0.2):]

    k= create_data(training_data_sentences , frequency_of_word,0)
    total_words = k
     

    #data for perplexity
    list = []
    log_pb ={}
    log_pb_wb ={}
    f ={}
    f_wb ={}

    list_test = []
    log_pb_test ={}
    log_pb_wb_test ={}
    f_test ={}
    f_wb_test ={}
    for sentence in test_data_sentences:

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
        list_test.append(words)
        
        if(len(sentence) == 0):
            test_data_sentences.remove(sentence)
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
            list_k_test = []
            for k in context:
                list_k_test.append(k)
            list_k_test.append(word)
            t_kn_test = kn_model_4(context,word)
            # t_wb = gram_prob_wb(context,word)

            # print(t)
            f.update({tuple(list_k_test):t_kn_test})
            # f_wb.update({tuple(list_k):t_wb})
            log_pb.update({tuple(list_k_test):math.log(t_kn_test)})
            # log_pb_wb.update({tuple(list_k):math.log(t_wb)})

    LM1_test_perplexity = open("2021114010_LM1_test-perplexity.txt", "w")
    perplexity_kn4_test = perplexity_kn(4 , list , f ,log_pb)
    avg_perplexity_test =  sum(perplexity_kn4_test)/len(perplexity_kn4_test)
    # print(perplexity_kn4)
    print("avg_perplexity: ",avg_perplexity_test , file = LM1_test_perplexity)
    for i in range(len(list)):
        print(list[i],perplexity_kn4_test[i], file = LM1_test_perplexity)
        
 


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
            t_kn = kn_model_4(context,word)
            # t_wb = gram_prob_wb(context,word)

            # print(t)
            f.update({tuple(list_k):t_kn})
            # f_wb.update({tuple(list_k):t_wb})
            log_pb.update({tuple(list_k):math.log(t_kn)})
            # log_pb_wb.update({tuple(list_k):math.log(t_wb)})

    # LM1_train_perplexity = open("2021114010_LM4_train-perplexity.txt", "w")

    # perplexity_kn4 = perplexity_kn(4 , list , f ,log_pb)
    # avg_perplexity =  sum(perplexity_kn4)/len(perplexity_kn4)
    # # print(perplexity_kn4)
    # print("avg_perplexity: ",avg_perplexity , file = LM1_train_perplexity)
    # for i in range(len(list)):
    #     print(list[i],perplexity_kn4[i], file = LM1_train_perplexity)
    input_sentence = input("Enter a sentence: ")
    if(model =="k"):
        tokens = input_sentence.split()
        tokens = ['<s>'] * 3 + tokens + ['</s>']
        ans = 1
        for i in range(len(tokens)-3):
            context = tuple(tokens[i:i+3])
            word = tokens[i+3]
            # print(context,word)
            ans*=kn_model_4(context,word)
        print("probability: ",ans)
    elif(model == "w"):
        tokens = input_sentence.split()
        tokens = ['<s>'] * 3 + tokens + ['</s>']
        ans = 1
        for i in range(len(tokens)-3):
            context = tuple(tokens[i:i+3])
            word = tokens[i+3]
            # print(context,word)
            ans*=wb_model_4(context,word)
        print("probability: ",ans)

        

