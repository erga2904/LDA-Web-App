import time
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from textblob import TextBlob

# Meminta pengguna memasukkan URL Instagram
instagram_url = input("Masukkan URL postingan Instagram: ")

# Inisialisasi WebDriver untuk Instagram
driver = webdriver.Chrome()
driver.get(instagram_url)
time.sleep(5)  # Tunggu halaman terbuka

# Menunggu konfirmasi sebelum mulai scraping
input("Tekan Enter setelah halaman tujuan terbuka untuk mulai scraping...")

# Klik tombol "Tampilkan komentar lainnya" jika ada
try:
    load_more_button = driver.find_element(By.XPATH, "//div[contains(text(),'View more comments')]")
    load_more_button.click()
    time.sleep(3)  # Tunggu komentar dimuat
except Exception:
    print("Tidak ada tombol 'View more comments', lanjut scraping.")

# Ambil komentar dari Instagram
comments = []
comment_elements = driver.find_elements(By.XPATH, "//span[contains(@class, '')]")
for elem in comment_elements:
    comments.append(elem.text.strip())

driver.quit()

# Pastikan komentar tidak kosong
if not comments:
    print("Tidak ada komentar ditemukan. Pastikan tautan Instagram yang diberikan benar.")
    exit()

# **Hapus kata yang tidak relevan seperti "Balas", "Lihat balasan", dll.**
excluded_words = {"balas", "lihat balasan", "suka", "komentar disembunyikan",
    "reply", "komen", "like", "pas", "habis", "cek", "bang", "live", "iklan",
    "promo", "streaming", "subscribe", "follow", "beli", "gratis", "foto",
    "kamera", "teknologi", "bayar", "jual", "diskon", "order", "dm",
    "gratis", "jualan", "brand", "wkwk", "anjay", "santuy", "gabut", "gue",
    "lu", "bro", "sis", "bestie", "cuy", "gak", "kan", "nih", "dong", "yaudah"
}

# Fungsi untuk membersihkan komentar dari kata tidak relevan
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in excluded_words]
    return " ".join(tokens)

# Membersihkan komentar dengan kata-kata yang tidak relevan
cleaned_comments = [preprocess_text(comment) for comment in comments if comment.strip()]

# Analisis Sentimen
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positif"
    elif sentiment_score < 0:
        return "Negatif"
    else:
        return "Netral"

sentiments = [get_sentiment(comment) for comment in cleaned_comments]

# **Pastikan semua daftar memiliki panjang yang sama**
min_length = min(len(comments), len(cleaned_comments), len(sentiments))
comments = comments[:min_length]
cleaned_comments = cleaned_comments[:min_length]
sentiments = sentiments[:min_length]

# Simpan komentar ke dalam CSV dengan format tabel terstruktur
df = pd.DataFrame({
    "No": range(1, min_length + 1),
    "Original Comment": comments,
    "Cleaned Comment": cleaned_comments,
    "Sentiment": sentiments
})

# Simpan dataset dalam format CSV yang lebih rapi
df.to_csv("instagram_comments_analysis.csv", index=False, encoding='utf-8-sig')

print("Dataset otomatis terstruktur dalam 'instagram_comments_analysis.csv'!")

# Membuat WordCloud dari komentar yang sudah diproses
text_data = " ".join(cleaned_comments)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)

# Simpan WordCloud sebagai file PNG
wordcloud.to_file("instagram_wordcloud.png")
print("WordCloud berhasil diekspor sebagai 'instagram_wordcloud.png'!")
import time
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from textblob import TextBlob

# Meminta pengguna memasukkan URL Instagram
instagram_url = input("Masukkan URL postingan Instagram: ")

# Inisialisasi WebDriver untuk Instagram
driver = webdriver.Chrome()
driver.get(instagram_url)
time.sleep(5)  # Tunggu halaman terbuka

# Menunggu konfirmasi sebelum mulai scraping
input("Tekan Enter setelah halaman tujuan terbuka untuk mulai scraping...")

# Klik tombol "Tampilkan komentar lainnya" jika ada
try:
    load_more_button = driver.find_element(By.XPATH, "//div[contains(text(),'View more comments')]")
    load_more_button.click()
    time.sleep(3)  # Tunggu komentar dimuat
except Exception:
    print("Tidak ada tombol 'View more comments', lanjut scraping.")

# Ambil komentar dari Instagram
comments = []
comment_elements = driver.find_elements(By.XPATH, "//span[contains(@class, '')]")
for elem in comment_elements:
    comments.append(elem.text.strip())

driver.quit()

# Pastikan komentar tidak kosong
if not comments:
    print("Tidak ada komentar ditemukan. Pastikan tautan Instagram yang diberikan benar.")
    exit()

# **Hapus kata yang tidak relevan seperti "Balas", "Lihat balasan", dll.**
excluded_words = {"balas", "lihat balasan", "suka", "komentar disembunyikan",
    "reply", "komen", "like", "pas", "habis", "cek", "bang", "live", "iklan",
    "promo", "streaming", "subscribe", "follow", "beli", "gratis", "foto",
    "kamera", "teknologi", "bayar", "jual", "diskon", "order", "dm",
    "gratis", "jualan", "brand", "wkwk", "anjay", "santuy", "gabut", "gue",
    "lu", "bro", "sis", "bestie", "cuy", "gak", "kan", "nih", "dong", "yaudah"
}

# Fungsi untuk membersihkan komentar dari kata tidak relevan
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in excluded_words]
    return " ".join(tokens)

# Membersihkan komentar dengan kata-kata yang tidak relevan
cleaned_comments = [preprocess_text(comment) for comment in comments if comment.strip()]

# Analisis Sentimen
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positif"
    elif sentiment_score < 0:
        return "Negatif"
    else:
        return "Netral"

sentiments = [get_sentiment(comment) for comment in cleaned_comments]

# **Pastikan semua daftar memiliki panjang yang sama**
min_length = min(len(comments), len(cleaned_comments), len(sentiments))
comments = comments[:min_length]
cleaned_comments = cleaned_comments[:min_length]
sentiments = sentiments[:min_length]

# Simpan komentar ke dalam CSV dengan format tabel terstruktur
df = pd.DataFrame({
    "No": range(1, min_length + 1),
    "Original Comment": comments,
    "Cleaned Comment": cleaned_comments,
    "Sentiment": sentiments
})

# Simpan dataset dalam format CSV yang lebih rapi
df.to_csv("instagram_comments_analysis.csv", index=False, encoding='utf-8-sig')

print("Dataset otomatis terstruktur dalam 'instagram_comments_analysis.csv'!")

# Membuat WordCloud dari komentar yang sudah diproses
text_data = " ".join(cleaned_comments)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)

# Simpan WordCloud sebagai file PNG
wordcloud.to_file("instagram_wordcloud.png")
print("WordCloud berhasil diekspor sebagai 'instagram_wordcloud.png'!")
