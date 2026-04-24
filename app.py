import pandas as pd
import streamlit as st

EXCEL_FILE = "final_trendyol_yorumlari_950.xlsx"

st.set_page_config(page_title="Trendyol Yorum Kontrol Paneli", layout="wide")

def clean(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

df = pd.read_excel(EXCEL_FILE)

st.title("Trendyol Yorum Kontrol Paneli")

# Boş yorumları ayır
df["Yorum"] = df["Yorum"].apply(clean)
df["Ürün Adı"] = df["Ürün Adı"].apply(clean)

# Arama
search = st.text_input("Ürün ara")

products = df["Ürün Adı"].dropna().unique()

if search:
    products = [p for p in products if search.lower() in p.lower()]

if len(products) == 0:
    st.warning("Ürün bulunamadı.")
    st.stop()

selected_product = st.selectbox("Ürün seç", products)

filtered = df[df["Ürün Adı"] == selected_product].copy()

link = clean(filtered["Trendyol.com Linki"].iloc[0])
st.markdown(f"[🔗 Trendyol Sayfasını Aç]({link})")

# Sadece gerçek yorumlar
reviews = filtered[
    filtered["Yorum"].notna()
    & (filtered["Yorum"].astype(str).str.strip() != "")
    & (filtered["Yorum"].astype(str).str.lower() != "nan")
]

st.write(f"Toplam yorum: {len(reviews)}")

if len(reviews) == 0:
    st.info("Bu ürün için kayıtlı yorum yok.")
else:
    for _, row in reviews.iterrows():
        st.markdown("---")
        st.write(f"👤 {clean(row.get('Yorumcu', ''))}")
        st.write(f"📅 {clean(row.get('Tarih', ''))}")

        details = []
        if clean(row.get("Boy", "")):
            details.append(f"Boy: {clean(row.get('Boy'))}")
        if clean(row.get("Kilo", "")):
            details.append(f"Kilo: {clean(row.get('Kilo'))}")
        if clean(row.get("Beden", "")):
            details.append(f"Beden: {clean(row.get('Beden'))}")

        if details:
            st.write(" | ".join(details))

        st.write(f"💬 {clean(row.get('Yorum', ''))}")