
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title= "Kişisel Finans Yönetimi Uygulaması", layout= "wide")

st.markdown("""
<style>

.kutu{
    background-color: white;
    border: 1px solid #d7dde5;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}      

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #1f3a5f 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}


[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}


[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
}


div[role="radiogroup"] label {
    font-weight: 500 !important;
    color: #cbd5f5 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    transition: all 0.2s ease !important;
    position: relative;
}


div[role="radiogroup"] label:hover {
    background-color: rgba(255, 255, 255, 0.06) !important;
    color: #ffffff !important;
}


div[role="radiogroup"] label[data-baseweb="radio"] {
    background-color: rgba(59, 130, 246, 0.15) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}


div[role="radiogroup"] label[data-baseweb="radio"]::before {
    content: "";
    position: absolute;
    left: 0;
    top: 6px;
    bottom: 6px;
    width: 4px;
    background: linear-gradient(180deg, #3b82f6, #2563eb);
    border-radius: 2px;
}


div[role="radiogroup"] input:checked + div {
    border-color: #3b82f6 !important;
}


[data-testid="stSidebar"] h1 {
    margin-bottom: 10px !important;
}

</style>
""", unsafe_allow_html=True)


veritabani = "finans.db"


def tablo_olustur():
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        category TEXT,
        note TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def veri_ekle(islem_turu, tutar, kategori, not_metni, tarih):
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (type, amount, category, note, date) VALUES (?, ?, ?, ?, ?)",
        (islem_turu, tutar, kategori, not_metni, str(tarih))
    )

    conn.commit()
    conn.close()


def verileri_getir():
    conn = sqlite3.connect(veritabani)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    conn.close()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df


def veri_sil(kayit_id):
    conn = sqlite3.connect(veritabani)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (kayit_id,))
    conn.commit()
    conn.close()


tablo_olustur()
veriler = verileri_getir()


if "secim" not in st.session_state:
    st.session_state.secim = "🏠 Ana Sayfa"

with st.sidebar:
    st.title("Menü")

    secenekler = ["🏠 Ana Sayfa", "➕ İşlem Ekle", "📊 Analiz", "🗂️ Veri Listesi"]

    if st.session_state.secim not in secenekler:
        st.session_state.secim = "🏠 Ana Sayfa"

    secim = st.radio(
         "Sayfa Seçiniz",
          secenekler,
         index= secenekler.index(st.session_state.secim)
     )

    st.session_state.secim = secim
    secim = st.session_state.secim




if secim == "🏠 Ana Sayfa":
    st.markdown("""
    <div class="kutu">
        <h2>Kişisel Finans Yönetim Uygulaması</h2>
        <p>Gelir ve gider kayıtlarının tutulduğu ve grafiklerle analiz edildiği bir uygulamadır.</p>
    </div>
    """, unsafe_allow_html= True)


    buton1, buton2, buton3 = st.columns(3)

    with buton1:
        if st.button("Yeni İşlem Ekle", use_container_width= True):
            st.session_state.secim = "➕ İşlem Ekle"
            st.rerun()

    with buton2:
        if st.button("Analize Git", use_container_width= True):
            st.session_state.secim = "📊 Analiz"
            st.rerun()

    with buton3:
        if st.button("Verileri Görüntüle", use_container_width= True):
            st.session_state.secim = "🗂️ Veri Listesi"
            st.rerun()

    if veriler.empty:
        st.info("Sistemde henüz veri bulunmuyor.")
    else:
        if len(veriler) < 3:
            st.warning("Henüz çok az veri var, daha fazla giriş yapılırsa daha anlamlı olacak.")

        toplam_gelir = veriler[veriler["type"] == "Gelir"]["amount"].sum()
        toplam_gider = veriler[veriler["type"] == "Gider"]["amount"].sum()
        net_bakiye = toplam_gelir - toplam_gider
        toplam_kayit = len(veriler)


        st.subheader("Finansal Durum Özeti")
        if net_bakiye < 0:
            st.error("Giderler gelirden fazla. Harcamaların kontrol edilmesi önerilir.")
        elif net_bakiye == 0:
            st.warning("Gelir ve gider birbirine eşit.")
        else:
            st.success("Gelir giderden fazla, finansal durum olumlu görünüyor.")

        giderler = veriler[veriler["type"] == "Gider"]
        if not giderler.empty:
            en_cok = giderler.groupby("category")["amount"].sum().idxmax()
            st.info(f"En fazla harcama yapılan kategori: {en_cok}")


        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Toplam Gelir", f"{toplam_gelir:.2f} ₺")
        c2.metric("Toplam Gider", f"{toplam_gider:.2f} ₺")
        c3.metric("Net Bakiye", f"{net_bakiye:.2f} ₺")
        c4.metric("Kayıt Sayısı", toplam_kayit)
        st.caption("Bu proje, kişisel finans takibini daha kolay yapmak için geliştirilmiştir.")


        gider_veri = veriler[veriler["type"] == "Gider"]
        if not gider_veri.empty:
            en_cok_kategori = (
                gider_veri.groupby("category")["amount"]
                .sum()
                .idxmax()
            )
            st.success(f"En çok harcama: {en_cok_kategori} kategorisinde yapılmıştır.")

        sol, sag = st.columns(2)

        with sol:
            st.subheader("📅 Aylık Gelir / Gider Özeti")

            aylik_veri = veriler.copy()
            aylik_veri["Ay"] = aylik_veri["date"].dt.strftime("%m-%Y")

            aylik_ozet = (
                aylik_veri.groupby(["Ay", "type"])["amount"]
                .sum()
                .reset_index()
            )

            fig1 = px.bar(
                aylik_ozet,
                x= "Ay",
                y= "amount",
                color= "type",
                barmode= "group",
                title= "Aylık Toplamlar"
            )

            fig1.update_traces(hovertemplate=None, hoverinfo="skip")
            fig1.update_layout(
                xaxis_title= "Ay",
                yaxis_title= "Tutar",
                title_x= 0.3
            )

            st.plotly_chart(
                fig1,
                use_container_width= True,
                config= {"displayModeBar": False}
            )

        with sag:
            st.subheader("🕒 Son 5 Kayıt")

            son_kayitlar = veriler.sort_values("date", ascending= False).head(5)
            if not son_kayitlar.empty:
                son = son_kayitlar.iloc[0]
                st.info(f"Son kayıt: {son['category']} - {son['amount']} ₺")

            st.dataframe(son_kayitlar, use_container_width= True, hide_index= True)


        alt_sol, alt_sag = st.columns(2)

        with alt_sol:
            st.subheader("📈 Finansal Değişim")

            gunluk_toplam = (
                veriler.groupby(["date", "type"])["amount"]
                .sum()
                .reset_index()
            )

            fig2 = px.line(
                gunluk_toplam,
                x="date",
                y="amount",
                color="type",
                markers=True,
                title="Gelir / Gider Değişimi"
            )

            fig2.update_traces(hovertemplate=None, hoverinfo="skip")
            fig2.update_layout(
                xaxis_title="Tarih",
                yaxis_title="Tutar",
                title_x=0.3,
                xaxis_tickformat="%d-%m-%Y"
            )

            fig2.update_xaxes(tickangle=-30)

            st.plotly_chart(
                fig2,
                use_container_width=True,
                config={"displayModeBar": False}
            )



        with alt_sag:
            st.subheader("💸 Gider Kategorileri")

            gider_ozet = gider_veri.groupby("category")["amount"].sum().reset_index()

            if not gider_ozet.empty:
                fig3 = px.pie(
                    gider_ozet,
                    values= "amount",
                    names= "category",
                    hole= 0.4,
                    title= "Kategori Dağılımı"
                )

                fig3.update_traces(hovertemplate= None, hoverinfo= "skip")
                fig3.update_layout(title_x= 0.3)

                st.plotly_chart(
                    fig3,
                    use_container_width= True,
                    config= {"displayModeBar": False}
                )
            else:
                st.info("Gider kaydı bulunmuyor.")


elif secim == "➕ İşlem Ekle":
    st.markdown("""
    <div class="kutu">
        <h2>Yeni İşlem Ekle</h2>
        <p>Gelir veya gider kaydı oluşturabilirsiniz.</p>
    </div>
    """, unsafe_allow_html= True)

    if st.button("Ana Sayfaya Dön"):
        st.session_state.secim = "🏠 Ana Sayfa"
        st.rerun()

    with st.form("kayit_formu", clear_on_submit= True):
        col1, col2 = st.columns(2)

        with col1:
            islem_turu = st.selectbox("İşlem Türü", ["Gelir", "Gider"])
            tutar = st.number_input("Tutar", min_value= 0.0, step= 1.0)

        with col2:
            kategori = st.selectbox(
                "Kategori",
                ["Maaş", "Gıda", "Kira", "Faturalar", "Ulaşım", "Eğitim", "Sağlık", "Diğer"]
            )
            tarih = st.date_input("Tarih", date.today())

        not_metni = st.text_area("Not")

        kaydet = st.form_submit_button("Kaydet", use_container_width= True)

        if kaydet:
            if tutar <= 0:
                st.warning("Lütfen geçerli bir tutar giriniz.")
            else:
                veri_ekle(islem_turu, tutar, kategori, not_metni, tarih)
                st.success("Kayıt başarıyla eklendi.")
                st.balloons()
                st.rerun()

    if not veriler.empty:
        bilgi1, bilgi2 = st.columns(2)

        with bilgi1:
            st.subheader("Mevcut Kayıt Sayısı")
            st.write(len(veriler))

        with bilgi2:
            st.subheader("Son Kayıt Tarihi")
            st.write(veriler["date"].max().date())


elif secim == "📊 Analiz":
    st.markdown("""
    <div class="kutu">
        <h2>Analiz</h2>
        <p>Veriler filtrelenerek gelir ve gider dağılımı grafikler üzerinden incelenebilir.</p>
    </div>
    """, unsafe_allow_html= True)

    if st.button("Ana Sayfaya Dön"):
        st.session_state.secim = "🏠 Ana Sayfa"
        st.rerun()

    if veriler.empty:
        st.info("Henüz kayıt girilmedi.")
    else:
        filtre = st.selectbox("İşlem Türü", ["Tümü", "Gelir", "Gider"])

        baslangic_tarihi = st.date_input("Başlangıç Tarihi", veriler["date"].min().date())
        bitis_tarihi = st.date_input("Bitiş Tarihi", veriler["date"].max().date())

        if filtre == "Tümü":
            filtreli_veri = veriler.copy()
        else:
            filtreli_veri = veriler[veriler["type"] == filtre]

        filtreli_veri = filtreli_veri[
            (filtreli_veri["date"] >= pd.to_datetime(baslangic_tarihi)) &
            (filtreli_veri["date"] <= pd.to_datetime(bitis_tarihi))
        ]

        if filtreli_veri.empty:
            st.info("Seçilen filtreye uygun veri bulunmuyor.")
        else:
            st.subheader("Gelir Kategorileri Dağılımı")

            gelir_df = filtreli_veri[filtreli_veri["type"] == "Gelir"]
            if not gelir_df.empty:
                gelir_toplam = gelir_df.groupby("category")["amount"].sum().reset_index()

                en_yuksek_gelir = gelir_toplam.sort_values("amount", ascending= False).iloc[0]
                st.write(
                    f"En yüksek gelir: {en_yuksek_gelir['category']} ({en_yuksek_gelir['amount']:.2f} ₺)"
                )

                fig_gelir = px.pie(
                    gelir_toplam,
                    values= "amount",
                    names= "category",
                    hole= 0.4,
                    title= "Gelir Dağılımı"
                )

                fig_gelir.update_traces(hovertemplate= None, hoverinfo= "skip")
                fig_gelir.update_layout(title_x= 0.3)

                st.plotly_chart(
                    fig_gelir,
                    use_container_width= True,
                    config= {"displayModeBar": False}
                )
            else:
                st.info("Gelir kaydı bulunmuyor.")

            st.subheader("Kategoriye Göre Harcamalar")

            gelir_df = filtreli_veri[filtreli_veri["type"] == "Gelir"]
            gider_df = filtreli_veri[filtreli_veri["type"] == "Gider"]

            c1,c2 = st.columns(2)

            with c1:
                if not gelir_df.empty:
                    st.metric("Ortalama Gelir", f"{gelir_df['amount'].mean():.2f} ₺")
            with c2:
                if not gider_df.empty:
                    st.metric("Ortalama Gider", f"{gider_df['amount'].mean():.2f} ₺")


            toplam = filtreli_veri["amount"].sum()
            st.success(f"Toplam işlem tutarı: {toplam:.2f} ₺")


            grafik_df = (
                filtreli_veri.groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values("amount", ascending=False)
            )

            if not grafik_df.empty:
                en_yuksek = grafik_df.iloc[0]
                st.write(f"En çok harcama: {en_yuksek['category']} ({en_yuksek['amount']:.2f} ₺)")

            fig4 = px.bar(
                grafik_df,
                x= "category",
                y= "amount",
                title= "Kategori Dağılımı",
                color= "category"
            )

            fig4.update_layout(
                xaxis_title= "Kategori",
                yaxis_title= "Toplam Tutar",
                title_x= 0.3
            )
            fig4.update_traces(hovertemplate=None, hoverinfo="skip")

            st.plotly_chart(
                fig4,
                use_container_width=True,
                config={"displayModeBar": False}
            )

            st.subheader("Aylık Gelir - Gider Analizi")

            analiz_df = filtreli_veri.copy()
            analiz_df["Ay"] = analiz_df["date"].dt.strftime("%m-%Y")

            aylik_df = (
                analiz_df.groupby(["Ay", "type"])["amount"]
                .sum()
                .reset_index()
            )

            fig5 = px.line(
                aylik_df,
                x= "Ay",
                y= "amount",
                color= "type",
                markers= True,
                title= "Aylık Trend"
            )

            fig5.update_layout(
                xaxis_title= "Ay",
                yaxis_title= "Toplam Tutar",
                title_x= 0.3,
                xaxis_tickangle= 0
            )

            fig5.update_xaxes(type= "category")
            fig5.update_traces(hovertemplate= None, hoverinfo= "skip")

            st.plotly_chart(
                fig5,
                use_container_width= True,
                config= {"displayModeBar": False}
            )

            st.subheader("Gider Kategorileri Dağılımı")

            gider_df = filtreli_veri[filtreli_veri["type"] == "Gider"]
            if not gider_df.empty:
                gider_toplam = gider_df.groupby("category")["amount"].sum().reset_index()

                en_yuksek_gider = gider_toplam.sort_values("amount", ascending= False).iloc[0]
                st.write(
                    f"En çok harcama: {en_yuksek_gider['category']} ({en_yuksek_gider['amount']:.2f} ₺)"
                )

                fig6 = px.pie(
                    gider_toplam,
                    values= "amount",
                    names= "category",
                    hole= 0.4,
                    title= "Gider Dağılımı"
                )

                fig6.update_traces(hovertemplate= None, hoverinfo= "skip")
                fig6.update_layout(title_x =0.3)

                st.plotly_chart(
                    fig6,
                    use_container_width= True,
                    config= {"displayModeBar": False}
                )
            else:
                st.info("Bu filtrede gider kaydı bulunmuyor.")


elif secim == "🗂️ Veri Listesi":
    st.markdown("""
    <div class="kutu">
        <h2>Kayıtlar</h2>
        <p>Kayıtları görüntüleyebilir, aranabilir ve silebilirsiniz.</p>
    </div>
    """, unsafe_allow_html= True)


    k1, k2 = st.columns(2)

    with k1:
        if st.button("Ana Sayfaya Dön", use_container_width= True):
            st.session_state.secim = "🏠 Ana Sayfa"
            st.rerun()

    with k2:
        if st.button("Analize Git", use_container_width= True):
            st.session_state.secim = "📊 Analiz"
            st.rerun()


    if veriler.empty:
        st.info("Henüz kayıt girilmedi.")
    else:
        arama = st.text_input("Kategori Ara")

        if arama:
            filtreli_tablo = veriler[veriler["category"].str.contains(arama, case= False, na= False)]
        else:
            filtreli_tablo = veriler.copy()

        st.dataframe(filtreli_tablo, use_container_width= True, hide_index= True)


        csv_veri = filtreli_tablo.to_csv(index= False).encode("utf-8-sig")
        st.download_button(
            label= "📥 CSV Olarak İndir",
            data= csv_veri,
            file_name= "finans_kayitlari.csv",
            mime= "text/csv"
        )


        alt1, alt2 = st.columns([1, 2])

        with alt1:
            silinecek_id = st.number_input("Silinecek ID", min_value= 1, step= 1)

            if st.button("Seçilen Kaydı Sil", use_container_width= True):
                veri_sil(silinecek_id)
                st.success("Kayıt silindi.")
                st.rerun()

        with alt2:
            st.subheader("Filtrelenmiş Tablo Özeti")
            st.write(f"Kayıt sayısı: {len(filtreli_tablo)}")
            if not filtreli_tablo.empty:
                st.write(f"Toplam tutar: {filtreli_tablo['amount'].sum():.2f} ₺")