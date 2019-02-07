sentence_tokens = []
question_to_id_mapping, id_to_question_mapping, ans_id_mappings = {}, {'title': {}, 'body': {}}, {}
tfidf_vectorizer, tfidf_values = [], []

def fetch_question_data():
    global question_to_id_mapping, id_to_question_mapping
    import pandas as pd, nltk, re

    print('Fetching questions..', end='\r')
    
    questions = pd.read_csv('Questions.csv', encoding='iso-8859-1')
    corpus = ""
    for i in range(len(questions)):
        question = str(questions['Title'][i]).lower()        
        question = nltk.sent_tokenize(question)[0]
        question_to_id_mapping[question] = int(questions['Id'][i])
        
        question_id = int(questions['Id'][i])
        id_to_question_mapping[question_id] = {}
        id_to_question_mapping[question_id]['title'] = str(questions['Title'][i])
        id_to_question_mapping[question_id]['body'] = str(questions['Body'][i])
        corpus += question + '. '

    del questions
    return corpus

def fetch_answer_data():
    print('Fetching answers..', end='\r')
    global ans_id_mappings
    import pandas as pd

    answers = pd.read_csv('Answers.csv', encoding='iso-8859-1')
    for i in range(len(answers)):
        try:
            answer = {}
            answer['body'] = str( answers['Body'][i] )
            answer['score'] = int( answers['Score'][i] )
            ans_id_mappings[ int(answers['ParentId'][i]) ].append(answer)
        except:
            ans_id_mappings[ int(answers['ParentId'][i]) ] = []
            answer = {}
            answer['body'] = str( answers['Body'][i] )
            answer['score'] = int( answers['Score'][i] )
            ans_id_mappings[ int(answers['ParentId'][i]) ].append(answer)

    del answers
    return ans_id_mappings


def prepare_tfidf_vector():
    global sentence_tokens, tfidf_vectorizer, tfidf_values 
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    print('Preparing TfIdf vector...', end='\r')
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_values = tfidf_vectorizer.fit_transform(sentence_tokens)

def dump_data():
    global question_to_id_mapping, id_to_question_mapping, ans_id_mappings, sentence_tokens
    import pickle

    print(' '*50+'\rSaving data..', end='\r')
    dump = [question_to_id_mapping, ans_id_mappings, sentence_tokens]
    pickle.dump(dump, open('data/data.pickle', 'wb'), protocol=-1)
    del question_to_id_mapping
    del ans_id_mappings

    pickle.dump(id_to_question_mapping, open('data/mapping.pickle', 'wb'), protocol=-1)
    del id_to_question_mapping

def dump_model():
    global tfidf_vectorizer, tfidf_values
    import pickle

    print(' '*50+'\rSaving model..', end='\r')
    dump = [tfidf_vectorizer, tfidf_values]
    pickle.dump(dump, open('data/model.pickle', 'wb'), protocol=-1)

if __name__ == "__main__":
    import nltk

    corpus = fetch_question_data()
    sentence_tokens = nltk.sent_tokenize(corpus)
    del corpus
    ans_id_mappings = fetch_answer_data()

    dump_data()
    prepare_tfidf_vector()
    dump_model()
    print(' '*50+'\rDone.')