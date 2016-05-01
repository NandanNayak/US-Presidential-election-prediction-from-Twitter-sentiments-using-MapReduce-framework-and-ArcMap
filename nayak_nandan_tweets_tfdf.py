#import all modules
import MapReduce
import sys
import re
import string

#global variables
mr = MapReduce.MapReduce()
doc1="nayak_nandan_tweet_data.txt"
tweet_count=0
presidentList=['hillary','clinton','bernie','sanders','ted','cruz','kasich','donald','trump']


#define all functions
def sendReducer(word,tweet_count):
    sub_list=[tweet_count,1]        #Keep track of the tweet and term frequency of the word
    mr.emit_intermediate(word,sub_list)

def mapper(each_tweet):
    # Mapper code goes in here
    text=each_tweet["text"]                     #Extract the text from tweet dictionary
    text=re.sub(r'https[\w\d\s.\W]*'," ",text)   #Remove https..... string
    text=re.sub(r' [\d]* '," ",text)            #Remove strings that are only numbers
    text=re.sub(r'@[\w\d]*'," ",text)           #Remove @ followed by word/number
    text=re.sub(r'#[\w\d]*'," ",text)            #Remove Hashtags   
    text=re.sub(r'RT[@\w\d]*'," ",text)        #Remove RT.... words    
    text=text.encode('utf-8').translate(None,string.punctuation)#Remove punctuations    
    text=text.lower()                           #Convert the string to lower
    text=text.split()                           #Convert the string into list of words

    global tweet_count
    tweet_count+=1                              #Keep track of the tweet count
    
    word_dict={}
    for word in text:        
        if word in presidentList and word not in word_dict: 
            total=0
            for i in range(len(text)):
                if(word==text[i]):
                    total+=1                    #Count the no. of times the word has repeated in the tweet
            sub_list=[tweet_count,total]        #Keep track of the tweet and term frequency of the word
            word_dict[word]=total
            mr.emit_intermediate(word,sub_list)
    
    

def reducer(key, list_of_values):
    #reducer code goes in here
    mr.emit((key,len(list_of_values),list_of_values))


#main funtion
if __name__ == '__main__':
    inputdata = open(doc1)
    mr.execute(inputdata, mapper, reducer)

