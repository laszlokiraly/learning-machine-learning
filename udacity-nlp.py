from __future__ import division

sample_memo = '''
Milt, we're gonna need to go ahead and move you downstairs into storage B. We have some new people coming in, and we need all the space we can get. So if you could just go ahead and pack up your stuff and move it down there, that would be terrific, OK?
Oh, and remember: next Friday... is Hawaiian shirt day. So, you know, if you want to, go ahead and wear a Hawaiian shirt and jeans.
Oh, oh, and I almost forgot. Ahh, I'm also gonna need you to go ahead and come in on Sunday, too...
Hello Peter, whats happening? Ummm, I'm gonna need you to go ahead and come in tomorrow. So if you could be here around 9 that would be great, mmmk... oh oh! and I almost forgot ahh, I'm also gonna need you to go ahead and come in on Sunday too, kay. We ahh lost some people this week and ah, we sorta need to play catch up.
'''

#
#   Maximum Likelihood Hypothesis
#
#
#   In this quiz we will find the maximum likelihood word based on the preceding word
#
#   Fill in the NextWordProbability procedure so that it takes in sample text and a word,
#   and returns a dictionary with keys the set of words that come after, whose values are
#   the number of times the key comes after that word.
#
# Just use .split() to split the sample_memo text into words separated by
# spaces.

corrupted_memo = '''
Yeah, I'm gonna --- you to go ahead --- --- complain about this. Oh, and if you could --- --- and sit at the kids' table, that'd be ---
'''

data_list = sample_memo.strip().split()

words_to_guess = ["ahead", "could"]


def NextWordProbability(sampletext, word, distance=1):

    nextWordCountDict = {}

    foundWord = 0

    totalCount = 0

    for sampleWord in sampletext.split():
        if foundWord == distance:
            count = nextWordCountDict.get(sampleWord, 0)
            nextWordCountDict[sampleWord] = count + 1
            totalCount += 1
            # print (sampleWord + " " + str(nextWordCountDict[sampleWord]))
            foundWord = 0
        if sampleWord == word:
            foundWord = 1
        else:
            if foundWord > 0:
                foundWord += 1

    for key, value in nextWordCountDict.items():
        nextWordCountDict[key] = value / totalCount

    return nextWordCountDict

# TODO: make this work with distance > 2


def LaterWords(sample, word, distance):
    '''@param sample: a sample of text to draw from
    @param word: a word occuring before a corrupted sequence
    @param distance: how many words later to estimate (i.e. 1 for the next word, 2 for the word after that), currently only works with distance up to 2
    @returns: a single word which is the most likely possibility
    '''

    # TODO: Given a word, collect the relative probabilities of possible following words
    # from @sample. You may want to import your code from the maximum
    # likelihood exercise.
    next_word_probability = NextWordProbability(sample, word)

    # TODO: Repeat the above process--for each distance beyond 1, evaluate the words that
    # might come after each word, and combine them weighting by relative probability
    # into an estimate of what might appear next.

    result = {}

    if distance > 1:
        for key, value in next_word_probability.items():
            # print (key + ": " + str(value))
            next_next_word_probality = NextWordProbability(sample, word, 2)
            for next_key, next_value in next_next_word_probality.items():
                result[next_key] = next_value * value
                # print (next_key + ": " + str(result[next_key]))
    else:
        result = next_word_probability

    # http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
    return sorted(result, key=result.get, reverse=True)[0]

print LaterWords(sample_memo, "ahead", 2)

test_memo = '''
She was first in a software engineering job where she did some software optimization work and then again in a software processing job
'''
test_words = LaterWords(test_memo, "software", 2)
print(test_words)
# for key, value in test_words.items():
#     print (key + ": " + str(value))
