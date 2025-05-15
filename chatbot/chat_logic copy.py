from sentence_transformers import SentenceTransformer, util
# from firebase_service import db

# Firebase
import firebase_admin
from firebase_admin import credentials, firestore
db = firestore.client()

model = SentenceTransformer('all-MiniLM-L6-v2')

def save_conversation(user_msg, bot_reply):
    db.collection("conversations").add({
        "user": user_msg,
        "bot": bot_reply,
        "embedding": model.encode(user_msg).tolist()
    })

def get_best_response(user_msg):
    user_embedding = model.encode(user_msg)

    docs = db.collection("conversations").stream()
    similarities = []
    for doc in docs:
        data = doc.to_dict()
        emb = data.get("embedding")
        if emb:
            score = util.cos_sim(user_embedding, emb)[0][0].item()
            similarities.append((score, data["bot"]))

    if similarities:
        similarities.sort(reverse=True)
        best_score, best_reply = similarities[0]
        if best_score > 0.7:
            return best_reply
    return "Maaf, saya belum tahu jawabannya."

def learn_and_reply(user_msg):
    reply = get_best_response(user_msg)
    if reply == "Maaf, saya belum tahu jawabannya.":
        # Di dunia nyata, bisa tambahkan input manual atau AI generatif
        reply = "Boleh ajarkan saya jawaban yang benar (ya/tidak)?"
    save_conversation(user_msg, reply)
    return reply



# def test_save_conversation():
#     """
#     Fungsi testing untuk memastikan percakapan berhasil disimpan.
#     """
#     user_message = "Apa itu Python?"
#     bot_reply = "Python adalah bahasa pemrograman yang sangat populer."
    
#     # Simulasi penyimpanan percakapan
#     save_conversation(user_message, bot_reply)
#     print(f"Percakapan disimpan: {user_message} -> {bot_reply}")
    
#     # Verifikasi data yang telah disimpan di Firestore
#     docs = db.collection("conversations").stream()
#     for doc in docs:
#         print(doc.id, doc.to_dict())

# # Jalankan fungsi test
# test_save_conversation()
