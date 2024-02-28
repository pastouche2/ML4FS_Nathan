import ast
import sys
import nltk
import flag
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize



# to get you started, here is sample code that reads the file and outputs an output file that is 0% correct (all empty arrays). You don't need to use this skeleton, feel free to start over and do it another way.

def parse_language(user_input):
    '''
    Description:
    This method is designed to parse a single user input regarding language proficiencies. It processes free-form inputs provided by users and categorizes their language proficiency into different levels based on the Common European Framework of Reference for Languages (CEFR). The method extracts information about the user's native languages and their proficiency levels in various languages.
    Parameters:
    user_input: A string representing the user's input regarding their language proficiencies.
    Returns:
    native_langs: A list containing the user's native languages.
    C2: A list containing languages in which the user is proficient at the C2 level.
    C1: A list containing languages in which the user is proficient at the C1 level.
    B2: A list containing languages in which the user is proficient at the B2 level.
    B1: A list containing languages in which the user is proficient at the B1 level.
    A2: A list containing languages in which the user is proficient at the A2 level.
    A1: A list containing languages in which the user is proficient at the A1 level.
    '''


    N = []
    C2 = []
    C1 = []
    B2 = []
    B1 = []
    A2 = []
    A1 = []
    # YOUR CODE HERE
    df_languages = pd.read_csv("countries_to_langs.csv")
    df_ISO = pd.read_csv("iso_codes.csv")
    balises = ["n", "c2", "c1", "b2", "b1", "a2", "a1"]
    corpus = preprocess_text_tokenisation(str(user_input))
    corpus_final = []

    for word in corpus:
        word_inter = flag.dflagize(word).split(":")
        word_inter = [w for w in word_inter if w]
        corpus_final.extend(word_inter)
    # if len(corpus_final) == 0:
    #     corpus_final = corpus
    # Determine the direction of the balises
    balises_on_right = corpus_final[-1] in balises

    seen_elements = []
    last_balise = None

    # Iterate over corpus_final in the appropriate direction
    iterable = reversed(corpus_final) if not balises_on_right else corpus_final
    for element in iterable:
        if element in balises:
            # Add the seen elements to the appropriate list
            last_balise = element
            if last_balise == "n":
                N.extend(seen_elements)
            elif last_balise == "c2":
                C2.extend(seen_elements)
            elif last_balise == "c1":
                C1.extend(seen_elements)
            elif last_balise == "b2":
                B2.extend(seen_elements)
            elif last_balise == "b1":
                B1.extend(seen_elements)
            elif last_balise == "a2":
                A2.extend(seen_elements)
            elif last_balise == "a1":
                A1.extend(seen_elements)
            # Clear the seen elements list and update the last balise
            seen_elements = []

        else:
            # Add the element to the seen elements list
            seen_elements.append(element)

    # Add any remaining seen elements to the appropriate list
    if last_balise == "n":
        N.extend(seen_elements)
    elif last_balise == "c2":
        C2.extend(seen_elements)
    elif last_balise == "c1":
        C1.extend(seen_elements)
    elif last_balise == "b2":
        B2.extend(seen_elements)
    elif last_balise == "b1":
        B1.extend(seen_elements)
    elif last_balise == "a2":
        A2.extend(seen_elements)
    elif last_balise == "a1":
        A1.extend(seen_elements)
    tuple_final = (N, C2, C1, B2, B1, A2, A1)
    tuple_final = [get_official_languages(countries, df_languages, df_ISO) for countries in tuple_final]
    return tuple_final
    
def preprocess_text_tokenisation(text):
    '''
    Description:
    This method is designed to preprocess a given text by removing punctuation, converting the text to lowercase, and removing stop words. It also converts the given text to a bag of word.
    Parameters:
    text: A string representing the text to be preprocessed.
    Returns:
    preprocessed_text: A string representing the preprocessed text.
    '''
    preprocessed_text = "".join([char.lower() for char in str(text) if char not in string.punctuation])
    word_corpus = word_tokenize(preprocessed_text, language='english')
    en_stopwords = nltk.corpus.stopwords.words('english')
    corpus_clean = [word for word in word_corpus if word not in en_stopwords]
    return corpus_clean


def get_official_languages(countries, df_languages, df_ISO):
    languages = []
    for country in countries:
        #if len(country) >2 :
            #filtered_df = df_ISO[df_ISO["Name-en"] == country.capitalize()]
            #if not filtered_df.empty:
                #country = filtered_df["ISO-Code"].iloc[0]
            #else:
                #print(f"No ISO code found for country: {country}")
                # Handle the case where no ISO code is found for the country
        country_languages = df_languages[df_languages["country"] == country].dropna(axis=1, how="all")
        column_names = country_languages.columns[1:]
        for language in column_names:
            language_dict = country_languages[language].iloc[0]
            dict_language = ast.literal_eval(language_dict)
            if int(dict_language['percent']) >=70 :
                languages.append(language)
    return languages


if __name__ == "__main__":
    # Check if filename argument is provided
    if len(sys.argv) != 3:
        print("Usage: python3 language_parser_lastname.py input_file.csv output_file.csv")
        sys.exit(1)

        # Get filename from command line argument
    infile = sys.argv[1]
    outfile = sys.argv[2]

    # read in the file, line by line
    with open(outfile, 'w') as out:
        out.write('username,N,C2,C1,B2,B1,A2,A1\n')
        with open(infile, 'r') as file:
            headers = next(file) # 'username,user_input'
            for line in file:
                line = line.strip().split(',') # ['username','user_input']
                username = line[0]
                user_input = line[1]
                parsed = parse_language(user_input) # 'user_input'
                print(username, parsed)
                # convert parsed to a string
                s = ','.join(str(lang_level) for lang_level in parsed) + '\n'
                out.write(username + ',' + s)
    
