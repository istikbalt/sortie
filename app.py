import pandas as pd
import streamlit as st

EXCEL_FILE = "FINAL_MASTER_DATA.xlsx"

st.set_page_config(page_title="Trendyol Yorum Kontrol Paneli", layout="wide")

def clean(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

df = pd.read_excel(EXCEL_FILE)

st.title("Trendyol Yorum Kontrol Paneli")

df["Ürün Adı"] = df["Ürün Adı"].apply(clean)
df["Yorum"] = df["Yorum"].apply(clean)

search = st.text_input("Ürün ara")

products = df["Ürün Adı"].dropna().unique()

if search:
    products = [p for p in products if search.lower() in p.lower()]

if len(products) == 0:
    st.warning("Ürün bulunamadı.")
    st.stop()

selected_product = st.selectbox("Ürün seç", products)

filtered = df[df["Ürün Adı"] == selected_product].copy()
first = filtered.iloc[0]

link = clean(first.get("Link", ""))
st.markdown(f"[🔗 Trendyol Sayfasını Aç]({link})")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ortalama Puan", clean(first.get("Ortalama Puan", "")))
col2.metric("Toplam Değerlendirme", clean(first.get("Toplam Değerlendirme", "")))
col3.metric("Toplam Yorum", clean(first.get("Toplam Yorum", "")))
col4.metric("Fotoğraflı Yorum", clean(first.get("Fotoğraflı Yorum", "")))

st.write(
    f"⭐ 5: {clean(first.get('5 Yıldız', 0))} | "
    f"4: {clean(first.get('4 Yıldız', 0))} | "
    f"3: {clean(first.get('3 Yıldız', 0))} | "
    f"2: {clean(first.get('2 Yıldız', 0))} | "
    f"1: {clean(first.get('1 Yıldız', 0))}"
)

reviews = filtered[
    filtered["Yorum"].notna()
    & (filtered["Yorum"].astype(str).str.strip() != "")
    & (filtered["Yorum"].astype(str).str.lower() != "nan")
]

st.subheader(f"Yorumlar ({len(reviews)})")

if len(reviews) == 0:
    st.info("Bu ürün için kayıtlı yorum yok.")
else:
    for _, row in reviews.iterrows():
        st.markdown("---")
        st.write(f"👤 {clean(row.get('Yorumcu', ''))}")
        st.write(f"⭐ {clean(row.get('Yıldız', ''))}")
        
        details = []
        if clean(row.get("Beden", "")):
            details.append(f"Beden: {clean(row.get('Beden'))}")
        if clean(row.get("Boy", "")):
            details.append(f"Boy: {clean(row.get('Boy'))}")
        if clean(row.get("Kilo", "")):
            details.append(f"Kilo: {clean(row.get('Kilo'))}")

        if details:
            st.write(" | ".join(details))

        st.write(f"💬 {clean(row.get('Yorum', ''))}")

        foto_links = clean(row.get("Foto Link", ""))
        if foto_links:
            links = [x.strip() for x in foto_links.split("|") if x.strip()]
            for img in links:
                st.image(img, width=180)