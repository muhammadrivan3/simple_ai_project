from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

from .models import ProfileMatch

# Firebase
import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase hanya sekali
# if not firebase_admin._apps:
#     cred = credentials.Certificate("path/to/your/serviceAccountKey.json")  # <- ganti path ini
#     firebase_admin.initialize_app(cred)

db = firestore.client()

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            
            # Proses file Excel menggunakan pandas
            df = pd.read_excel(uploaded_file)
            
            # Pastikan kolom valid
            df.columns = df.columns.fillna('').astype(str)

            # Lakukan proses profile matching
            result = perform_matching(df)

            # Simpan hasil ke Firebase
            db.collection("profile_matches").add(result)

            # Simpan ke database Django (optional)
            ProfileMatch.objects.create(
                name="Example Match",
                score=95.5,
                matched_data=result
            )

            return JsonResponse({"message": "File processed and saved successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"message": "No file uploaded."}, status=400)


def perform_matching(df):
    # Simulasi logika matching sederhana
    # Ubah dataframe jadi list of dict (aman untuk Firestore)
    data_list = df.to_dict(orient='records')

    result = {
        "status": "matched",
        "data": data_list
    }
    print("=== Data yang akan dikirim ke Firestore ===")
    print(result)

    return result
