# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>
consumer_key = 'ktLmeMlEnE0QedN1bkypZaZOg'
consumer_secret = '2PWIDTnrwEZHvASgfBAAAKDLv649DMHhCtvkdpPJO9IvyQej2B'
access_token = '2807535638-bf6iLNgyvL1LAWGbBA8h5D0yYnoq9Fu1U0RjXnt'
access_token_secret = 'IqhvHN2kCgSrUGWPFvT7a3jDiY0uh5Xgv4YzVueyvyQpZ'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

userName = sys.argv[1]
numberOfTweets = sys.argv[2]

tweetsByUser = api.user_timeline(screen_name = userName, count = numberOfTweets, include_rts = True);
tweetDetails = {"user": userName,
                "tweetCount": numberOfTweets,
                "originalTweets":0,
                "originalTweetsFav":0,
                "originalTweetsRts":0,
                "statuses":"",
                "partsOfSpeech":{}
                };

# "stop words": ignore any words that do not start with an alphabetic character [a-zA-Z], and also ignore 'http', 'https', and 'RT'
def formatTweets(tweets):
    words = tweets.split();
    formattedWords = tweets.split();
    for word in words:
        if( not word[0].isalpha() or word.startswith('http') or word.startswith('RT')):
            formattedWords.remove(word)
    return ' '.join(formattedWords);

#group and count by parts of speech
def getTagFrequency(tagPrefix, taggedText):
    conditionalFreqD = nltk.ConditionalFreqDist((tagPrefix, word) for (word, tag) in taggedText if tag.startswith(tagPrefix))
    results = dict(conditionalFreqD[tagPrefix])
    sorted_d = sorted(results.items(), key=lambda v: (v[0].upper(), v[0][0].islower()))
    sorted_d.sort(key=lambda x: x[1], reverse=True)
    return sorted_d[:5]

# get nouns, verbs, adjs
def analyzePartsOfSpeech(text):
    analyzedTweets = {};
    tagged_words =  nltk.pos_tag(text);
    analyzedTweets['nouns'] = getTagFrequency('NN', tagged_words)
    analyzedTweets['verbs'] = getTagFrequency('VB', tagged_words)
    analyzedTweets['adjectives'] = getTagFrequency('JJ', tagged_words)
    return analyzedTweets


def analyzeTweets(tweets, tweetDetails):
    for tweet in tweets:
        #if(tweet.text.startswith("RT @") == False):
        if not hasattr(tweet, 'retweeted_status'):
            tweetDetails['originalTweets'] += 1;
            tweetDetails['originalTweetsFav'] += tweet.favorite_count;
            tweetDetails['originalTweetsRts'] += tweet.retweet_count;
        tweetDetails['statuses'] += " " + tweet.text

    filterTweets = formatTweets(tweetDetails['statuses'])
    # print filterTweets
    #textToAnalyze = nltk.word_tokenize(filterTweets);
    textToAnalyze = filterTweets.split(" ");
    tweetDetails['partsOfSpeech'] = analyzePartsOfSpeech(textToAnalyze);
    printResults(tweetDetails);


def printResults(rawData):
    #print "*********"
    verbs = '';
    nouns = '';
    adjectives = '';
    for verb, freq in rawData['partsOfSpeech']['verbs']:
            verbs += " " + verb + "(" + str(freq) + ")"

    for noun, freq in rawData['partsOfSpeech']['nouns']:
            nouns += " " + noun + "(" + str(freq) + ")"

    for adjective, freq in rawData['partsOfSpeech']['adjectives']:
            adjectives += " " + adjective + "(" + str(freq) + ")"

    print ("USER: "+ rawData['user'])
    print ("TWEETS ANALYZED: " + str(rawData['tweetCount']))
    print ("ORIGINAL TWEETS: " + str(rawData['originalTweets']))
    print ("VERBS:" + verbs)
    print ("NOUNS:" + nouns)
    print ("ADJECTIVES" + adjectives)
    print ("TIMES FAVORITED (ORIGINAL TWEETS ONLY): " + str(rawData['originalTweetsFav']))
    print ("TIMES RETWEETED (ORIGINAL TWEETS ONLY): " + str(rawData['originalTweetsRts']))

def outputCsv(data):
    csvData = "Noun,Number\n"
    for noun, freq in data:
        csvData += str(noun) +","+str(freq)+"\n"
    sys.stdout=open("noun_data.csv","w")
    print (csvData)
    sys.stdout.close()


analyzeTweets(tweetsByUser, tweetDetails);
outputCsv(tweetDetails['partsOfSpeech']['nouns'])
