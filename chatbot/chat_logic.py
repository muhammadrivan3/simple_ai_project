from sentence_transformers import SentenceTransformer, util
import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase
db = firestore.client()

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Memory training per sesi (untuk produksi sebaiknya simpan di DB per user)
training_sessions = {}  # session_id -> last_question

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
    return None  # agar bisa dibedakan

def learn_and_reply(user_msg, session_id="default"):
    # Cek jika sedang training (minta jawaban)
    if session_id in training_sessions:
        last_question = training_sessions.pop(session_id)
        save_conversation(last_question, user_msg)
        return "Terima kasih! Saya sudah belajar jawabannya."

    # Cari jawaban dari database
    response = get_best_response(user_msg)
    if response:
        save_conversation(user_msg, response)
        return response

    # Jika tidak tahu jawabannya, aktifkan training mode
    training_sessions[session_id] = user_msg
    return "Saya belum tahu jawabannya. Boleh ajarkan saya sekarang?"




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
