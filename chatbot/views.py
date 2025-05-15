from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .chat_logic import learn_and_reply, save_conversation

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "")
        reply = learn_and_reply(user_msg)
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request."})
@csrf_exempt
def train(user_msg, correct_reply):
    """
    Fungsi untuk melatih chatbot dengan percakapan baru yang diberikan.
    Menyimpan percakapan dan embedding baru ke Firebase.
    """
    # Simpan percakapan yang benar
    save_conversation(user_msg, correct_reply)
    return "Terima kasih, saya telah belajar jawaban yang benar."
