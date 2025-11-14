# 📊 MAT 271E: Olasılık ve İstatistik Ödev Çözümleri

Bu depo, **[MAT 271E] Olasılık ve İstatistik** dersi kapsamında tamamladığım 6 farklı ödev sorusunun Python ile yazılmış çözümlerini içermektedir.

Her bir dosya, bir problem setini veya ders konusunu ele almakta, teorik olasılık ve istatistik kavramlarının **simülasyon** ve **veri analizi** yoluyla uygulanışını göstermektedir.

## 📌 İçerik ve Konular

Aşağıdaki tabloda, her bir Python dosyasının hangi ödev sorusuna ait olduğu ve ele aldığı ana konular listelenmiştir:

| Dosya Adı | Ödev Sorusu | Ana Konular |
| :--- | :--- | :--- |
| `HW1_Q2.py` | Soru 2 | **Olasılık Simülasyonu (Monte Carlo):** İki oyunculu bir oyunun kazanma olasılıklarının simülasyonu. |
| `HW1_Q3.py` | Soru 3 | **Bağımlılık ve Koşullu Olasılık:** Genetik veri setinde Marjinal ve Koşullu Olasılık hesaplamaları ($P(T|G_i)$). Bağımlılık/Bağımsızlık kararı. |
| `HW1_Q4.py` | Soru 4 | **Bayes Teoremi ve Poker:** Kart oyununda (Ace olup olmama durumu) "Tell" durumuna göre kazanma olasılığının Bayes kuralı ile simülasyonu. |
| `HW1_Q5.py` | Soru 5 | **Bayes Ağları/Bayes Güncellemesi:** Prior ve Koşullu Olasılık matrisleri kullanarak Posterior olasılığın hesaplanması ($P(L_i|O)$). |
| `HW1_Q6.py` | Soru 6 | **Rastgele Değişken Simülasyonları:** Bernoulli, Binom, Geometrik, Negatif Binom, Poisson ve Üstel (Exponential) dağılımların simülasyonu ve histogram ile görselleştirilmesi. |
| `HW1_Q7.py` | Soru 7 | **Rastgelelik Testi (Runs Testi):** Gerçek rastgele bir dizi ile insan tarafından üretilen (önyargılı) bir diziyi Koşma (Run) sayısı ve En Uzun Koşma uzunluğuna göre ayırt etme. |

## ⚙️ Gereksinimler

Kodların çalıştırılması için temel Python kütüphaneleri gereklidir:

* **Python 3.x**
* **NumPy** (Veri manipülasyonu ve matematiksel işlemler için)
* **Matplotlib** (Soru 6'daki dağılım histogramları için)

### Kurulum

```bash
pip install numpy matplotlib