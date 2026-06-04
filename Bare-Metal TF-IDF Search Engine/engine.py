import re
from collections import Counter
import math 

class MiniSearchEngine():
    def __init__(self):
        #volab
        self.vocab = {}
        # term frequency vectorized
        self.TF = []
        #inverse document frequency vectorized
        self.IDF = []
        
        # term frequency inverse document frequency vectorized 
        self.TF_IDF = []
        
    def clean(self,corpus: list[str]) -> list[list[str]]:
        clean_corpus = []
        
        for sentence in corpus:
            #googled the regex
            clean_text = re.sub(r"^\w\s","",sentence)
            clean_text = clean_text.lower()
            clean_corpus.append(clean_text)
        
        return clean_corpus
    
    def build_vocab(self, clean_corpus: list[str]) -> dict:
        count = 0
        vocab = {}

        for sentence in clean_corpus:
            words = sentence.split()

            for word in words:
                if word not in vocab:
                    vocab[word] = count
                    count += 1

        return vocab   

    def build_tf(self, clean_corpus: list[str]) -> list[list[int]]:
        #term frequency
        TF = []
        
        for sentence in clean_corpus:
            words = sentence.split()
            words_count = Counter(words)
            length = len(words)
            temp_vector = []
            for word in words:
                temp_vector.append(words_count[word]/length)
            TF.append(temp_vector)
            
        return TF
    
    def build_idf(self, clean_corpus: list[str]) -> list[list[float]]:
        IDF = []
        self.idf_dict = {}
        documents = len(clean_corpus)
        
        document_sets = [set(sen.split()) for sen in clean_corpus]
        
        for sentence in clean_corpus:
            temp_vector = []
            for word in sentence.split():
                if word not in self.idf_dict:
                    count = 0
                    for doc_set in document_sets:
                        if word in doc_set:
                            count += 1
                    
                    self.idf_dict[word] = math.log(documents / count)
                
                temp_vector.append(self.idf_dict[word])
            IDF.append(temp_vector)
            
        return IDF
    
    def tf_idf(self, TF: list[str], IDF: list[str]) -> list[list[int]]:
        #term frequency + inverse term frequency
        TF_IDF = []
        
        for sentence in range(len(TF)):
            temp_sentence = []
            for word in range(len(TF[sentence])):
                temp_sentence.append(TF[sentence][word] * IDF[sentence][word])
            TF_IDF.append(temp_sentence)
        
        final_tfidf = []
        
        for doc_idx, sentence in enumerate(self.clean_corpus):
            vec = [0] * len(self.vocab)

            words = sentence.split()

            for word_idx, word in enumerate(words):
                vec[self.vocab[word]] = TF_IDF[doc_idx][word_idx]

            final_tfidf.append(vec)
        
        return final_tfidf
    
    def fit(self,corpus: list[str]) -> None:
        self.corpus = corpus
            
        clean_corpus = self.clean(corpus)
        self.clean_corpus = clean_corpus
        
        self.vocab = self.build_vocab(clean_corpus)
        
        tf = self.build_tf(clean_corpus)
        idf = self.build_idf(clean_corpus)
        tf_idf = self.tf_idf(tf,idf)
        
        self.TF, self.IDF,self.TF_IDF = tf, idf, tf_idf
        
        return
    
    def get_vector(self, text:str) -> dict[str,float]:
        #term frequency
        tf = []
        words = text.split()
        word_count = Counter(words)
        length_text = len(words)
        for word in words:
            tf.append(word_count[word]/length_text)
        
        tf_idf = []
        
        for t_f in range(len(tf)):
            tf_idf.append(tf[t_f] * self.idf_dict[words[t_f]])
        
        vector = [0] * len(self.vocab)
        
        for val in range(len(tf_idf)):
            #print(val)
            vector[self.vocab[words[val]]] = tf_idf[val]
        
        return vector
    
    #googled the formula and how to do dot product calculation
    def cosine_similarity(self, vec1: list[float] , vec2: list[float]) -> float:
        print(vec1,vec2)
        
        dot_product = sum(a * b for a,b in zip(vec1, vec2))
        
        mag_vec1 = math.sqrt(sum(a ** 2 for a in vec1))
        mag_vec2 = math.sqrt(sum(a ** 2 for a in vec2))
        
        return dot_product / (mag_vec1 * mag_vec2)
        
    def search(self, query: str, top_k: int = 1) -> list[tuple[str, float]]:
        clean_query = re.sub(r"[^\w\s]", "", query).lower()
        
        query_vector = self.get_vector(clean_query)
        
        raw_results = []
        for doc_idx in range(len(self.TF_IDF)):
            score = self.cosine_similarity(query_vector, self.TF_IDF[doc_idx])
            document = self.corpus[doc_idx]
            
            raw_results.append((score, document))
            
        raw_results.sort(key=lambda x: x[0], reverse=True)
        
        final_results = []
        for score, document in raw_results[:top_k]:
            final_results.append((document, score))
            
        return final_results