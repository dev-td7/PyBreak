sentence_tokens = []
question_to_id_mapping, id_to_question_mapping, ans_id_mappings = {}, {'title': {}, 'body': {}}, {}
tfidf_vectorizer, tfidf_values = [], []
CHUNK_SIZE = 15000

def fetch_question_data():
    global question_to_id_mapping, id_to_question_mapping
    import pandas as pd, nltk, re

    print(' ' * 40 + '\r' + '[1/7] Fetching question data..', end='\r')
    
    corpus = ""
    i = 0
    for questions in pd.read_csv('data/Questions.csv', encoding='iso-8859-1', chunksize=CHUNK_SIZE):
        force_start, questions_scanned_in_chunk = True, 0
        while (force_start or i % CHUNK_SIZE != 0) and questions_scanned_in_chunk < len(questions):
            force_start = False
            question = str(questions['Title'][i]).lower()
            question = nltk.sent_tokenize(question)[0]
            question_to_id_mapping[question] = int(questions['Id'][i])
            
            question_id = int(questions['Id'][i])
            id_to_question_mapping[question_id] = {}
            id_to_question_mapping[question_id]['title'] = str(questions['Title'][i])
            id_to_question_mapping[question_id]['body'] = str(questions['Body'][i])
            id_to_question_mapping[question_id]['author'] = str(questions['OwnerUserId'][i])
            corpus += question + '. '
            i += 1
            questions_scanned_in_chunk += 1

        print(' ' * 40 + '\r' + '[1/7] Fetched %-6d questions...' % i, end='\r')

    print(' ' * 40 + '\r' + 'Fetched %-6d questions' % i)
    return corpus

def fetch_answer_data():
    print(' ' * 40 + '\r' + '[4/7] Fetching answer data..', end='\r')
    global ans_id_mappings
    import pandas as pd

    i = 0
    for answers in pd.read_csv('data/Answers.csv', encoding='iso-8859-1', chunksize=CHUNK_SIZE):
        force_start, answers_scanned_in_chunk = True, 0
        while (force_start or i % CHUNK_SIZE != 0) and answers_scanned_in_chunk < len(answers):
            force_start = False
            answer = {
                'body': str( answers['Body'][i] ),
                'score': int( answers['Score'][i] ),
                'author': str(answers['OwnerUserId'][i])
            }
            
            question_id = int(answers['ParentId'][i])
            if question_id not in ans_id_mappings:
                ans_id_mappings[question_id] = []
            
            ans_id_mappings[question_id].append(answer)
            i += 1
            answers_scanned_in_chunk += 1

        print(' ' * 40 + '\r' + '[4/7] Fetched %-6d answers...' % i, end='\r')
    
    print(' ' * 40 + '\r' + 'Fetched %-6d answers' % i)
    return ans_id_mappings


def prepare_tfidf_vector():
    global sentence_tokens, tfidf_vectorizer, tfidf_values 
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    
    print(' ' * 40 + '\r' + '[6/7] Extracting features from data...', end='\r')
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_values = tfidf_vectorizer.fit_transform(sentence_tokens)

def dump_data(data_to_dump, file_name):
    import pickle
    pickle.dump(data_to_dump, open('data/'+file_name+'.pickle', 'wb'), protocol=-1)

if __name__ == "__main__":
    import nltk, time

    print('[Preprocessing data. The whole process may take upto 5 minutes to finish. But its for the best and will save time later]', end='\n\n')
        
    start = time.time()
    corpus = fetch_question_data()
    print(' ' * 40 + '\r' + '[2/7] Saving question data..', end='\r')
    dump_data([question_to_id_mapping, id_to_question_mapping], 'question_data')
    del question_to_id_mapping
    del id_to_question_mapping

    print(' ' * 40 + '\r' + '[3/7] Tokenizing...', end='\r')
    sentence_tokens = nltk.sent_tokenize(corpus)
    del corpus

    ans_id_mappings = fetch_answer_data()
    print(' ' * 40 + '\r' + '[5/7] Saving answer data...', end='\r')
    dump_data([ans_id_mappings, sentence_tokens], 'answer_data')

    prepare_tfidf_vector()
    print(' ' * 40 + '\r' + '[7/7] Saving model...', end='\r')
    dump_data([tfidf_vectorizer, tfidf_values], 'model')

    end = time.time()
    print(' ' * 50 + '\rFinished in ' + str((end * 1. - start * 1.) / 60) + ' min(s)')
