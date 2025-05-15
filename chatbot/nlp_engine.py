# import re
# import nltk
# from nltk.tokenize import word_tokenize
# from collections import defaultdict

# nltk.download('punkt')

# class SelfLearningChatBot:
#     def __init__(self):
#         self.knowledge = defaultdict(dict)  # bisa kamu ganti jadi Firebase nanti

#     def clean(self, text):
#         return re.sub(r'[^\w\s]', '', text.lower())

#     def tokenize(self, text):
#         return word_tokenize(self.clean(text))

#     def learn(self, question, answer):
#         tokens = self.tokenize(question)
#         context_key = " ".join(tokens)
#         self.knowledge[context_key] = {"tokens": tokens, "response": answer}
#         return context_key

#     def respond(self, user_input):
#         tokens = self.tokenize(user_input)
#         context_key = " ".join(tokens)
#         return self.knowledge.get(context_key, {}).get("response", "Maaf, saya belum paham konteks ini.")
