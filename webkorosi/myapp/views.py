from django.shortcuts import render
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
import tensorflow 
# Import fungsi load_model dari TensorFlow Keras
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import pandas as pd
import joblib
from django.conf import settings
import os
import joblib
import json

import re
import random
#import pickle

from .models import Compounds

# Mendapatkan jalur lengkap ke direktori model
model_path = os.path.join(settings.STATICFILES_DIRS[0], 'modelgbr_6040_denganpoly2.joblib')

def home(request):
    return render(request, 'home.html')
    # return HttpResponse("ini home")

def search_compound(request):
    if request.method == 'POST':
        drugs_q = request.POST.get('search_input', '')
        try:
            data = serializers.serialize("python", Compounds.objects.filter(common_name__icontains = drugs_q))
            p = Paginator(data, 9)
            page_num = request.GET.get('page', 1)

            try:
                page = p.page(page_num)
            except:
                page = p.page(1)

            context = {
                'data': page,
            }

            return render(request, "search.html", context)
        except Compounds.DoesNotExist:
            messages.error(
                request, 'Drugs not found, enter appropriate name!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def search(request) :
    data = serializers.serialize("python", Compounds.objects.order_by('IE_EXP'))
    p = Paginator(data, 9)

    page_num = request.GET.get('page', 1)

    try:
        page = p.page(page_num)
    except:
        page = p.page(1)

    context = {
        'data': page,
    }

    return render(request, "search.html", context)


def team(request):
    return render(request, 'team.html')
    # return HttpResponse("ini home")

def journal(request):
    return render(request, 'journal.html')
    # return HttpResponse("ini home")

def predict(request) :
    prediction = [0]

    # Memuat model
    print("Memuat Model GBR")
    # Memuat model
    print("Memuat Model GBR")
    # with open(model_path, 'rb') as f:
    #     model = pickle.load(f)
    model = joblib.load(model_path)
    
    # Jika model berhasil dimuat, cetak pesan ke konsol
    print("Model berhasil dimuat.")
    # Jika model berhasil dimuat, cetak pesan ke konsol
    print("Model berhasil dimuat.")

    if request.method == 'POST' :
        input_dict = {
            'Molecular_weight MW (g/mol)' : float(request.POST['MW']),
            'pKa' : float(request.POST['pKa']),
            'Log P' : float(request.POST['logP']),
            'Log S' : float(request.POST['logS']),
            'Polar Surface Area (Å2)' : float(request.POST['PSA']),
            'Polarizability (Å3)' : float(request.POST['polarizability']),
            'HOMO (eV)' : float(request.POST['E-HOMO']),
            'LUMO (eV)' : float(request.POST['E-LUMO']),
            'Electronegativity (eV)' : float(request.POST['electrophilicity']),
            ' ΔN_Fe ' : float(request.POST['fraction_electron_shared'])
        }

        # Define columns to scale
        columns_to_scale = ['Molecular_weight MW (g/mol)', 'pKa', 'Log P', 'Log S', 'Polar Surface Area (Å2)',
                                    'Polarizability (Å3)', 'HOMO (eV)', 'LUMO (eV)', 'Electronegativity (eV)', ' ΔN_Fe ']
        
        normalization_path = os.path.join(settings.STATICFILES_DIRS[0], 'min_max_values.json')
        # Load normalization parameters from JSON
        with open(normalization_path, 'r') as file:
            normalization_params = json.load(file)

        for feature in columns_to_scale:
            min_value = normalization_params[feature]["min"]
            max_value = normalization_params[feature]["max"]
            input_dict[feature] = (
                input_dict[feature] - min_value) / (max_value - min_value)
            
        
        prediction = model.predict(
            [
                [ 
                    input_dict['Molecular_weight MW (g/mol)'],
                    input_dict['pKa'],
                    input_dict['Log P'],
                    input_dict['Log S'],
                    input_dict['Polar Surface Area (Å2)'],
                    input_dict['Polarizability (Å3)'],
                    input_dict['HOMO (eV)'],
                    input_dict['LUMO (eV)'],
                    input_dict['Electronegativity (eV)'],
                    input_dict[' ΔN_Fe '],
                ]
            ]
        )
    
        _max = 99.00
        _min = 67.70
        # pred_invers = (prediction[0] * (_max - _min)) + _min
        # y_new_pred_best = str(y_new_pred_best[0].round(2))
    print(prediction[0])
    prediction = f'{round(prediction[0],2)} %'
    output = {"output": prediction }

    return render(request, 'app.html', output)

    # context = {
    #     'prediction_result' : prediction,
    # }
    # return render(request, 'app.html', output)

def ml_ops(request) :
    result = ""
    model_name = "ml_models/"+ str(request.POST.get('algorithm_option')) +"_"+ str(request.POST.get('split_option')) +"_"+ str(request.POST.get('normalization_option')) + ".joblib"

    if request.method == 'POST' :
        model = joblib.load(model_name)
        input_dict = {
            'Molecular_weight MW (g/mol)' : float(request.POST['MW']),
            'pKa' : float(request.POST['pKa']),
            'Log P' : float(request.POST['logP']),
            'Log S' : float(request.POST['logS']),
            'Polar Surface Area (Å2)' : float(request.POST['PSA']),
            'Polarizability (Å3)' : float(request.POST['polarizability']),
            'HOMO (eV)' : float(request.POST['E-HOMO']),
            'LUMO (eV)' : float(request.POST['E-LUMO']),
            'Electronegativity (eV)' : float(request.POST['electrophilicity']),
            ' ΔN_Fe ' : float(request.POST['fraction_electron_shared'])
        }

        # Define columns to scale
        columns_to_scale = ['Molecular_weight MW (g/mol)', 'pKa', 'Log P', 'Log S', 'Polar Surface Area (Å2)',
                                    'Polarizability (Å3)', 'HOMO (eV)', 'LUMO (eV)', 'Electronegativity (eV)', ' ΔN_Fe ']
        
        input_normalization = str(request.POST.get('normalization_option'))

        if input_normalization != "None" :
            normalization_path = "ml_models/normalization_scalers/" + input_normalization

            # Load normalization parameters from JSON
            with open(f"{normalization_path}.json", 'r') as file:
                normalization_params = json.load(file)

            if input_normalization == "MinMaxScaler()" :
                for feature in columns_to_scale:
                    min_value = normalization_params[feature]["min"]
                    max_value = normalization_params[feature]["max"]
                    input_dict[feature] = (
                        input_dict[feature] - min_value) / (max_value - min_value)
                    
            elif input_normalization == "StandardScaler()" :
                for feature in columns_to_scale:
                    mean_value = normalization_params[feature]["mean"]
                    std_value = normalization_params[feature]["std"]
                    input_dict[feature] = (
                        input_dict[feature] - mean_value) / std_value
                    
            elif input_normalization == "RobustScaler()" :
                for feature in columns_to_scale:
                    center_value = normalization_params[feature]["center"]
                    scale_value = normalization_params[feature]["scale"]
                    input_dict[feature] = (
                        input_dict[feature] - center_value) / scale_value
            
        prediction = model.predict(
            [
                [ 
                    input_dict['Molecular_weight MW (g/mol)'],
                    input_dict['pKa'],
                    input_dict['Log P'],
                    input_dict['Log S'],
                    input_dict['Polar Surface Area (Å2)'],
                    input_dict['Polarizability (Å3)'],
                    input_dict['HOMO (eV)'],
                    input_dict['LUMO (eV)'],
                    input_dict['Electronegativity (eV)'],
                    input_dict[' ΔN_Fe '],
                ]
            ]
        )

        result = f'{float(prediction[0])} %'
    context = {"result" : result }

    return render(request, 'manual_app.html', context)

def view_pdf(request,orang):
    if orang == "Nicholaus":
        pdf_path = "/static/filepdf/Nicholaus.pdf"
    elif orang =="Dzaki":
        pdf_path = "/static/filepdf/Dzaki.pdf"
    elif orang =="Nibras":
        pdf_path = "/static/filepdf/Nibras.pdf"
    elif orang =="Cornell":
        pdf_path = "/static/filepdf/Cornell.pdf"
    elif orang=="paktotok1":
        pdf_path = "/static/filepdf/paktotok1.pdf"
    elif orang=="pakakrom1":
        pdf_path = "/static/filepdf/pakakrom1.pdf"
    elif orang=="pakakrom2":
        pdf_path = "/static/filepdf/pakakrom2.pdf"
    elif orang=="pakbudi1":
        pdf_path = "/static/filepdf/pakbudi1.pdf"
    elif orang=="2022 - Experimental investigation":
        pdf_path = "/static/filepdf/2022 - Experimental investigation.pdf"
    elif orang=="2023 - CTC":
        pdf_path = "/static/filepdf/2023 - CTC.pdf" 
    elif orang=="2023 - Jommit":
        pdf_path = "/static/filepdf/2023 - Jommit.pdf" 
    elif orang=="2023 - JPCS":
        pdf_path = "/static/filepdf/2023 - JPCS.pdf" 
    elif orang=="2023 - MTC":
        pdf_path = "/static/filepdf/2023 - MTC.pdf" 

    return render(request, 'view_pdf.html', {'pdf_path': pdf_path})
    # return HttpResponse("ini home")

def chatbot(request):
    return render(request, 'chatbot.html')
    
def inputan_user(request):
    with open('ml_models/model_chatbot/intents english.json', 'r', encoding="utf-8") as f:
        data = json.load(f)  # Membaca data dari file JSON

    # Membuat DataFrame dari data JSON
    df_chatbot = pd.DataFrame(data['intents'])

    # Membuat dictionary kosong untuk menyimpan data yang akan diubah ke DataFrame
    dic = {"tag": [], "patterns": [], "responses": []}
    for i in range(len(df_chatbot)):
        # Mengambil pola (patterns) dari DataFrame
        ptrns = df_chatbot[df_chatbot.index == i]['patterns'].values[0]
        # Mengambil respons dari DataFrame
        rspns = df_chatbot[df_chatbot.index == i]['responses'].values[0]
        # Mengambil tag dari DataFrame
        tag = df_chatbot[df_chatbot.index == i]['tag'].values[0]
        for j in range(len(ptrns)):
            dic['tag'].append(tag)  # Menambahkan tag ke dalam dictionary
            # Menambahkan pola ke dalam dictionary
            dic['patterns'].append(ptrns[j])
            # Menambahkan respons ke dalam dictionary
            dic['responses'].append(rspns)

    # Membuat DataFrame baru dari dictionary
    df_chatbot = pd.DataFrame.from_dict(dic)

    # Membuat objek Tokenizer dengan parameter tertentu
    tokenizer = Tokenizer(lower=True, split=' ')
    # Mengonversi teks pola menjadi urutan angka
    tokenizer.fit_on_texts(df_chatbot['patterns'])

    # Mengonversi teks pola menjadi urutan angka
    ptrn2seq = tokenizer.texts_to_sequences(df_chatbot['patterns'])
    # Melakukan padding terhadap urutan angka
    X = pad_sequences(ptrn2seq, padding='post')

    lbl_enc = LabelEncoder()  # Membuat objek LabelEncoder
    # Mengonversi label kelas menjadi angka
    y = lbl_enc.fit_transform(df_chatbot['tag'])

    # Memuat model yang telah dilatih sebelumnya
    model_path = 'ml_models/model_chatbot/my_model_English.keras'  # Perbarui dengan path yang benar
    loaded_model = load_model(model_path)  # Memuat model yang telah dilatih

    response_user = []  # List untuk menyimpan respons dari pengguna
    response_bot = []  # List untuk menyimpan respons dari bot

    # menampilkan hasil histori dari chat sebelumnya
    # if "messages" not in st.session_state:
        # Membuat session state untuk menyimpan histori chat sebelumnya
        # st.session_state.messages = []
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         # Menampilkan histori chat sebelumnya
    #         st.markdown(message["content"])

    # Dapatkan input pengguna

    # Proses input pengguna dan tampilkan respons
    if request.method == 'POST':
        text = []
        # Menghapus karakter selain huruf dan tanda kutip dari request
        txt = re.sub('[^a-zA-Z\']', ' ', request)
        txt = txt.lower()  # Mengonversi request menjadi huruf kecil
        txt = txt.split()  # Membagi request menjadi kata-kata
        txt = " ".join(txt)  # Menggabungkan kata-kata kembali menjadi teks
        text.append(txt)  # Menambahkan teks ke dalam list

        # Mengonversi teks input pengguna menjadi urutan angka
        x_test = tokenizer.texts_to_sequences(text)
        # Melakukan padding terhadap urutan angka
        x_test = pad_sequences(x_test, padding='post', maxlen=X.shape[1])
        # Memprediksi kelas dengan model yang telah dilatih
        y_pred = loaded_model.predict(x_test)
        y_pred = y_pred.argmax()  # Mengambil indeks kelas dengan nilai probabilitas tertinggi
        # Mengonversi indeks kelas kembali menjadi label kelas
        tag = lbl_enc.inverse_transform([y_pred])[0]
        # Mengambil respons berdasarkan label kelas
        responses = df_chatbot[df_chatbot['tag'] == tag]['responses'].values[0]

        # Gunakan respons tetap daripada random.choice(responses)
        # Memilih respons bot atau respons default jika tidak ada respons yang sesuai
        bot_response = random.choice(
            responses) if responses else "I cant understand what u say."
        

    return render(request, 'base.html', bot_response)
        
    #     return JsonResponse({"bot_response": bot_response})
    # else:
    #     return JsonResponse({"Error": "Bot tidak jalan"}, status=405)
    
# def inputan_user(request):
#     if request.method == 'POST':
#         # Proses input pengguna dan tampilkan respons
#         with open('ml_models/model_chatbot/intents_english.json', 'r', encoding="utf-8") as f:
#             data = json.load(f)  # Membaca data dari file JSON

#         # Membuat DataFrame dari data JSON
#         df_chatbot = pd.DataFrame(data['intents'])

#         # Membuat dictionary kosong untuk menyimpan data yang akan diubah ke DataFrame
#         dic = {"tag": [], "patterns": [], "responses": []}
#         for i in range(len(df_chatbot)):
#             # Mengambil pola (patterns) dari DataFrame
#             ptrns = df_chatbot[df_chatbot.index == i]['patterns'].values[0]
#             # Mengambil respons dari DataFrame
#             rspns = df_chatbot[df_chatbot.index == i]['responses'].values[0]
#             # Mengambil tag dari DataFrame
#             tag = df_chatbot[df_chatbot.index == i]['tag'].values[0]
#             for j in range(len(ptrns)):
#                 dic['tag'].append(tag)  # Menambahkan tag ke dalam dictionary
#                 # Menambahkan pola ke dalam dictionary
#                 dic['patterns'].append(ptrns[j])
#                 # Menambahkan respons ke dalam dictionary
#                 dic['responses'].append(rspns)

#         # Membuat DataFrame baru dari dictionary
#         df_chatbot = pd.DataFrame.from_dict(dic)

#         # Membuat objek Tokenizer dengan parameter tertentu
#         tokenizer = Tokenizer(lower=True, split=' ')
#         # Mengonversi teks pola menjadi urutan angka
#         tokenizer.fit_on_texts(df_chatbot['patterns'])

#         # Mengonversi teks pola menjadi urutan angka
#         ptrn2seq = tokenizer.texts_to_sequences(df_chatbot['patterns'])
#         # Melakukan padding terhadap urutan angka
#         X = pad_sequences(ptrn2seq, padding='post')

#         lbl_enc = LabelEncoder()  # Membuat objek LabelEncoder
#         # Mengonversi label kelas menjadi angka
#         y = lbl_enc.fit_transform(df_chatbot['tag'])

#         # Memuat model yang telah dilatih sebelumnya
#         model_path = 'ml_models/model_chatbot/my_model_English.keras'  # Perbarui dengan path yang benar
#         loaded_model = load_model(model_path)  # Memuat model yang telah dilatih

#         # Dapatkan teks input pengguna dari permintaan POST
#         text = request.POST.get('message', '')

#         # Menghapus karakter selain huruf dan tanda kutip dari teks input pengguna
#         txt = re.sub('[^a-zA-Z\']', ' ', text)
#         txt = txt.lower()  # Mengonversi teks menjadi huruf kecil
#         txt = txt.split()  # Membagi teks menjadi kata-kata
#         txt = " ".join(txt)  # Menggabungkan kata-kata kembali menjadi teks

#         # Menambahkan teks input ke dalam list
#         text = [txt]

#         # Mengonversi teks input pengguna menjadi urutan angka
#         x_test = tokenizer.texts_to_sequences(text)
#         # Melakukan padding terhadap urutan angka
#         x_test = pad_sequences(x_test, padding='post', maxlen=X.shape[1])
#         # Memprediksi kelas dengan model yang telah dilatih
#         y_pred = loaded_model.predict(x_test)
#         y_pred = y_pred.argmax()  # Mengambil indeks kelas dengan nilai probabilitas tertinggi
#         # Mengonversi indeks kelas kembali menjadi label kelas
#         tag = lbl_enc.inverse_transform([y_pred])[0]
#         # Mengambil respons berdasarkan label kelas
#         responses = df_chatbot[df_chatbot['tag'] == tag]['responses'].values[0]

#         # Gunakan respons tetap daripada random.choice(responses)
#         # Memilih respons bot atau respons default jika tidak ada respons yang sesuai
#         bot_response = random.choice(
#             responses) if responses else "I cant understand what u say."
        
#         return JsonResponse({"bot_response": bot_response})
#     else:
#         return JsonResponse({"Error": "Metode permintaan tidak didukung"}, status=405)

    
# Create your views here.