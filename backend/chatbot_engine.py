import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotEngine:
    def __init__(self, kb_path="farming_kb.json"):
        if os.path.exists(kb_path):
            with open(kb_path, "r") as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = []
        
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.questions = [item['question'] for item in self.knowledge_base]
        
        if self.questions:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def get_response(self, user_query):
        if not self.questions:
            return "I'm currently updating my knowledge base. Please ask later."
            
        user_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(user_vec, self.tfidf_matrix)
        
        best_match_idx = np.argmax(similarities)
        best_score = similarities[0][best_match_idx]
        
        if best_score > 0.3:  # Threshold for relevance
            return self.knowledge_base[best_match_idx]['answer']
        else:
            return "I'm sorry, I don't have specific information on that yet. Try asking about 'rice fertilizer', 'soil acidity', or 'NPK'."

if __name__ == "__main__":
    bot = ChatbotEngine()
    print(bot.get_response("best fertilizer for rice"))
