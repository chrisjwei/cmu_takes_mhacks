# modified RAKE for our purposes

# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010). 
# Automatic keyword extraction from indi-vidual documents. 
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re
import operator
import os

debug = False
example = False


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    return getSmartStopList()


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list

def get_concise_keywords(fullPhraseList):
    # limit to 2 word keywords
    shortPhrase = []
    checkUnique = set()
    for phrase in fullPhraseList:
        if phrase.count(' ') < 2: 
            words = set(phrase.split())
            if words & checkUnique == set(): 
              # if some words overlap, dont add others; will under count
              checkUnique |= words
              shortPhrase.append(phrase)
    return shortPhrase

def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class CategorizeNewsArticle(object):
    def __init__(self, stop_words_path="SmartStoplist.txt"):
        self.stop_words_path = stop_words_path
        self.stop_words_pattern = build_stop_word_regex(stop_words_path)
        pass

    def run(self, text="", max_keywords=3):
        if text == "":
            text = u"Bryan R. Smith/AP The former mayor took issue with de Blasio\u2019s comment that homelessness rose 40% during the Giuliani administration \u2014 saying that actually the shelter population rose only 32%.\n\nIt all depends on what you mean by \u201chomeless.\u201d\n\nRudy Giuliani, defending his City Hall record in an ongoing spat with Mayor de Blasio, said Friday shelter residents don\u2019t count as homeless \u2014 a definition that would surprise the Department of Homeless Services.\n\nThe former mayor took issue with de Blasio\u2019s comment that homelessness rose 40% during the Giuliani administration \u2014 saying that actually the shelter population rose only 32%.\n\n\u201cHere's how ignorant Mayor de Blasio is ... people who are in shelters, I would like to inform the mayor, are not homeless,\u201d said Giuliani in an interview on \u201cGood Day New York\u201d before going to the 9/11 Memorial.\n\nSpencer Platt/Getty Images 'Here's how ignorant Mayor de Blasio is ... people who are in shelters, I would like to inform the mayor, are not homeless,' said Rudy Giuliani in an interview.\n\nA spokeswoman for the mayor said name-calling on the 9/11 anniversaries was \u201cinappropriate\u201d and declined further comment.\n\nHomeless advocates were incensed. \u201cOf course people in homeless shelters are homeless,\u201d said Jennifer Flynn of Vocal-NY."
        try: 
            text = text.encode('ascii', 'ignore')
            text.replace('\n',' ')
        except:
            pass

        sentence_list = split_sentences(text)

        full_phrase_list = generate_candidate_keywords(sentence_list, self.stop_words_pattern)

        phrase_list = get_concise_keywords(full_phrase_list)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.iteritems(), key=operator.itemgetter(1), reverse=True)
        
        total_keywords = len(sorted_keywords)
        show_keywords = min(total_keywords/3,max_keywords)
        final_keywords = []
        for keyword in sorted_keywords[0:show_keywords]:
            final_keywords.append(keyword[0])
        return final_keywords

def getSmartStopList():
    return ["a",
            "a's",
            "able",
            "about",
            "above",
            "according",
            "accordingly",
            "across",
            "actually",
            "after",
            "afterwards",
            "again",
            "against",
            "ain't",
            "all",
            "allow",
            "allows",
            "almost",
            "alone",
            "along",
            "already",
            "also",
            "although",
            "always",
            "am",
            "among",
            "amongst",
            "an",
            "and",
            "another",
            "any",
            "anybody",
            "anyhow",
            "anyone",
            "anything",
            "anyway",
            "anyways",
            "anywhere",
            "apart",
            "appear",
            "appreciate",
            "appropriate",
            "are",
            "aren't",
            "around",
            "as",
            "aside",
            "ask",
            "asking",
            "associated",
            "at",
            "available",
            "away",
            "awfully",
            "b",
            "be",
            "became",
            "because",
            "become",
            "becomes",
            "becoming",
            "been",
            "before",
            "beforehand",
            "behind",
            "being",
            "believe",
            "below",
            "beside",
            "besides",
            "best",
            "better",
            "between",
            "beyond",
            "both",
            "brief",
            "but",
            "by",
            "c",
            "c'mon",
            "c's",
            "came",
            "can",
            "can't",
            "cannot",
            "cant",
            "cause",
            "causes",
            "certain",
            "certainly",
            "changes",
            "clearly",
            "co",
            "com",
            "come",
            "comes",
            "concerning",
            "consequently",
            "consider",
            "considering",
            "contain",
            "containing",
            "contains",
            "corresponding",
            "could",
            "couldn't",
            "course",
            "currently",
            "d",
            "definitely",
            "described",
            "despite",
            "did",
            "didn't",
            "different",
            "do",
            "does",
            "doesn't",
            "doing",
            "don't",
            "done",
            "down",
            "downwards",
            "during",
            "e",
            "each",
            "edu",
            "eg",
            "eight",
            "either",
            "else",
            "elsewhere",
            "enough",
            "entirely",
            "especially",
            "et",
            "etc",
            "even",
            "ever",
            "every",
            "everybody",
            "everyone",
            "everything",
            "everywhere",
            "ex",
            "exactly",
            "example",
            "except",
            "f",
            "far",
            "few",
            "fifth",
            "first",
            "five",
            "followed",
            "following",
            "follows",
            "for",
            "former",
            "formerly",
            "forth",
            "four",
            "from",
            "further",
            "furthermore",
            "g",
            "get",
            "gets",
            "getting",
            "given",
            "gives",
            "go",
            "goes",
            "going",
            "gone",
            "got",
            "gotten",
            "greetings",
            "h",
            "had",
            "hadn't",
            "happens",
            "hardly",
            "has",
            "hasn't",
            "have",
            "haven't",
            "having",
            "he",
            "he's",
            "hello",
            "help",
            "hence",
            "her",
            "here",
            "here's",
            "hereafter",
            "hereby",
            "herein",
            "hereupon",
            "hers",
            "herself",
            "hi",
            "him",
            "himself",
            "his",
            "hither",
            "hopefully",
            "how",
            "howbeit",
            "however",
            "i",
            "i'd",
            "i'll",
            "i'm",
            "i've",
            "ie",
            "if",
            "ignored",
            "immediate",
            "in",
            "inasmuch",
            "inc",
            "indeed",
            "indicate",
            "indicated",
            "indicates",
            "inner",
            "insofar",
            "instead",
            "into",
            "inward",
            "is",
            "isn't",
            "it",
            "it'd",
            "it'll",
            "it's",
            "its",
            "itself",
            "j",
            "just",
            "k",
            "keep",
            "keeps",
            "kept",
            "know",
            "knows",
            "known",
            "l",
            "last",
            "lately",
            "later",
            "latter",
            "latterly",
            "least",
            "less",
            "lest",
            "let",
            "let's",
            "like",
            "liked",
            "likely",
            "little",
            "look",
            "looking",
            "looks",
            "ltd",
            "m",
            "mainly",
            "many",
            "may",
            "maybe",
            "me",
            "mean",
            "meanwhile",
            "merely",
            "might",
            "more",
            "moreover",
            "most",
            "mostly",
            "much",
            "must",
            "my",
            "myself",
            "n",
            "name",
            "namely",
            "nd",
            "near",
            "nearly",
            "necessary",
            "need",
            "needs",
            "neither",
            "never",
            "nevertheless",
            "new",
            "next",
            "nine",
            "no",
            "nobody",
            "non",
            "none",
            "noone",
            "nor",
            "normally",
            "not",
            "nothing",
            "novel",
            "now",
            "nowhere",
            "o",
            "obviously",
            "of",
            "off",
            "often",
            "oh",
            "ok",
            "okay",
            "old",
            "on",
            "once",
            "one",
            "ones",
            "only",
            "onto",
            "or",
            "other",
            "others",
            "otherwise",
            "ought",
            "our",
            "ours",
            "ourselves",
            "out",
            "outside",
            "over",
            "overall",
            "own",
            "p",
            "particular",
            "particularly",
            "per",
            "perhaps",
            "placed",
            "please",
            "plus",
            "possible",
            "presumably",
            "probably",
            "provides",
            "q",
            "que",
            "quite",
            "qv",
            "r",
            "rather",
            "rd",
            "re",
            "really",
            "reasonably",
            "regarding",
            "regardless",
            "regards",
            "relatively",
            "respectively",
            "right",
            "s",
            "said",
            "same",
            "saw",
            "say",
            "saying",
            "says",
            "second",
            "secondly",
            "see",
            "seeing",
            "seem",
            "seemed",
            "seeming",
            "seems",
            "seen",
            "self",
            "selves",
            "sensible",
            "sent",
            "serious",
            "seriously",
            "seven",
            "several",
            "shall",
            "she",
            "should",
            "shouldn't",
            "since",
            "six",
            "so",
            "some",
            "somebody",
            "somehow",
            "someone",
            "something",
            "sometime",
            "sometimes",
            "somewhat",
            "somewhere",
            "soon",
            "sorry",
            "specified",
            "specify",
            "specifying",
            "still",
            "sub",
            "such",
            "sup",
            "sure",
            "t",
            "t's",
            "take",
            "taken",
            "tell",
            "tends",
            "th",
            "than",
            "thank",
            "thanks",
            "thanx",
            "that",
            "that's",
            "thats",
            "the",
            "their",
            "theirs",
            "them",
            "themselves",
            "then",
            "thence",
            "there",
            "there's",
            "thereafter",
            "thereby",
            "therefore",
            "therein",
            "theres",
            "thereupon",
            "these",
            "they",
            "they'd",
            "they'll",
            "they're",
            "they've",
            "think",
            "third",
            "this",
            "thorough",
            "thoroughly",
            "those",
            "though",
            "three",
            "through",
            "throughout",
            "thru",
            "thus",
            "to",
            "together",
            "too",
            "took",
            "toward",
            "towards",
            "tried",
            "tries",
            "truly",
            "try",
            "trying",
            "twice",
            "two",
            "u",
            "un",
            "under",
            "unfortunately",
            "unless",
            "unlikely",
            "until",
            "unto",
            "up",
            "upon",
            "us",
            "use",
            "used",
            "useful",
            "uses",
            "using",
            "usually",
            "uucp",
            "v",
            "value",
            "various",
            "very",
            "via",
            "viz",
            "vs",
            "w",
            "want",
            "wants",
            "was",
            "wasn't",
            "way",
            "we",
            "we'd",
            "we'll",
            "we're",
            "we've",
            "welcome",
            "well",
            "went",
            "were",
            "weren't",
            "what",
            "what's",
            "whatever",
            "when",
            "whence",
            "whenever",
            "where",
            "where's",
            "whereafter",
            "whereas",
            "whereby",
            "wherein",
            "whereupon",
            "wherever",
            "whether",
            "which",
            "while",
            "whither",
            "who",
            "who's",
            "whoever",
            "whole",
            "whom",
            "whose",
            "why",
            "will",
            "willing",
            "wish",
            "with",
            "within",
            "without",
            "won't",
            "wonder",
            "would",
            "would",
            "wouldn't",
            "x",
            "y",
            "yes",
            "yet",
            "you",
            "you'd",
            "you'll",
            "you're",
            "you've",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "z",
            "zero"]
