import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from io import BytesIO

nltk.download('stopwords')
nltk.download('punkt')

# Fungsi membersihkan teks komentar
def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r'http\S+|www\S+|@\S+|#\S+', '', teks)
    teks = re.sub(r'[^\w\s]', '', teks)
    teks = word_tokenize(teks)
    teks = [kata for kata in teks if kata not in stopwords.words('indonesian')]
    return ' '.join(teks)

# Load model sentimen
with open("model_sentimen.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🚦 Analisis Sentimen Komentar tentang ETLE")
st.write("Unggah file CSV yang berisi komentar untuk dianalisis.")

uploaded_file = st.file_uploader("📂 Pilih file CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Normalisasi nama kolom
    df.columns = df.columns.str.strip().str.lower()
    st.write("✅ Kolom yang terdeteksi:", df.columns.tolist())

    if 'komentar' in df.columns:
        # Proses pembersihan dan prediksi
        df['komentar_bersih'] = df['komentar'].apply(bersihkan_teks)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['komentar_bersih'])
        df['sentimen'] = model.predict(X)

        st.write("📊 **Hasil Analisis Sentimen:**")
        st.write(df[['komentar', 'sentimen']])

        # Tampilkan chart
        st.bar_chart(df['sentimen'].value_counts())

        # Tombol untuk mengunduh hasil analisis sebagai CSV
        def convert_df_to_csv(df):
            return df.to_csv(index=False).encode('utf-8')

        csv_data = convert_df_to_csv(df)
        st.download_button(
            label="📥 Unduh Hasil sebagai CSV",
            data=csv_data,
            file_name='hasil_analisis_sentimen.csv',
            mime='text/csv'
        )
    else:
        st.error("❌ Kolom 'komentar' tidak ditemukan. Pastikan kolom di file kamu bernama 'Komentar' (dengan huruf besar-kecil bisa diabaikan).")

st.write("🚀 Aplikasi ini membantu dalam memahami opini publik terhadap ETLE!")
