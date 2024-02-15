'''Semantic Similarity: starter code

Authors: Shervin Darmanki Farahani, Michael Guerzhoy. Last modified: Dec. 3, 2023.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    intersection = [x for x in vec1 if x in vec2]
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def build_semantic_descriptors(sentences):
    descriptors = {}
    for sentence in sentences:
        already_counted = []
        for word in sentence:
            if word not in already_counted:
                already_counted.append(word)
                if word not in descriptors:
                    descriptors[word] = {}
                co_words = [co_word for co_word in sentence if co_word != word]
                # A co-word is a word that appears in the same sentence as word,
                # aka we don't include it in the list if its the same as word
                for co_word in co_words:
                    if co_word not in descriptors[word]:
                        descriptors[word][co_word] = 0
                    descriptors[word][co_word] += 1
    return descriptors


def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for filename in filenames:
        f = open(filename, "r", encoding="latin1")
        text = f.read().lower()
        f.close()
        text = ''.join(ch for ch in text if ch.isalpha() or ch.isspace() or ch in ['.', '!', '?'])
        # Basically this just conjoins everything thats a space, a letter, or a sentence ender
        for separator in ['.', '!', '?']:
            text = text.replace(separator, '|')
        sentences.extend(text.split('|'))
    sentences = [sentence.split() for sentence in sentences if sentence]
    return build_semantic_descriptors(sentences)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]

    similarities = []
    for choice in choices:
        if choice in semantic_descriptors:
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choice])
        else:
            similarity = -1
        similarities.append(similarity)

    max_similarity = max(similarities)
    if max_similarity == -1:
        return choices[0]
    else:
        return choices[similarities.index(max_similarity)]



def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    num_correct = 0
    for line in lines:
        words = line.strip().split()
        question = words[0]
        answer = words[1]
        choices = words[2:]

        guess = most_similar_word(question, choices, semantic_descriptors, similarity_fn)
        if guess == answer:
            num_correct += 1

    return (num_correct / len(lines)) * 100

# Example usage:
# sem_descriptors = build_semantic_descriptors_from_files(["book1.txt", "book2.txt", ...])
# res = run_similarity_test("TOEFL_questions.txt", sem_descriptors, cosine_similarity)
# print(res, "of the guesses were correct")
