# 📊 Metriklerin ve Analizlerin Anlamı

**The Memory Pulse**, size ham veriden fazlasını sunar. Bu rehber, ekranda gördüğünüz verilerin ne anlama geldiğini ve neleri işaret ettiğini açıklar.

## 1. Uçucu Bellek (RAM) Tablosu

*   **Toplam (Total)**: Sisteminizdeki fiziksel yüklü RAM miktarı.
*   **Kullanılabilir (Available)**: İşletim sistemi tarafından uygulamalara hemen verilebilecek bellek. Bu, "Boş" (Free) bellekten farklıdır; çünkü önbellekleri (cache) de içerir.
    *   *Kritik Seviye*: %10'un altına düşerse sistem yavaşlamaya başlar.
*   **Kullanılan (Used)**: Aktif olarak işlemler tarafından tutulan bellek.

## 2. Takas Alanı (Swap) Durumu

Swap, RAM dolduğunda işletim sisteminin sabit diski RAM gibi kullanmasıdır.
*   **Kullanım Oranı > %0**: Sisteminiz RAM yetersizliği çekmeye başlamış olabilir.
*   **Kullanım Oranı > %50**: Ciddi performans kaybı yaşanır (Thrashing). Disk G/Ç'si tavan yapar, bilgisayar donabilir.

## 3. Korteks Analizi (The Cortex Analysis)

Bu bölüm, **The Memory Pulse**'ın "beyni"dir.

### Trend (Eğilim)
Bellek kullanımının zaman içindeki değişim yönünü gösterir.
*   **YÜKSELİYOR (RISING)**: Bellek kullanımı istikrarlı bir şekilde artıyor.
    *   *Anlamı*: Çalışan bir uygulama bellek sızdırıyor (Memory Leak) olabilir veya iş yükü artıyor.
*   **DURAĞAN (STABLE)**: Bellek kullanımı dengeli. İdeal durum budur.
*   **DÜŞÜYOR (FALLING)**: İşlemler bellek iade ediyor veya kapanıyor.

### Eğim (Slope)
Matematiksel olarak trendin "şiddetini" gösterir.
*   `0.00`: Tamamen düz çizgi.
*   `> 0.10`: Çok hızlı artış. Acil müdahale gerekebilir (örneğin bir `while True` döngüsünde liste şişmesi).

### Z-Skoru ve Anomaliler
Sistem, son ölçümlerin ortalamasını alır. Eğer anlık bir ölçüm, ortalamadan çok saparsa bu bir "Anomali"dir.
*   *Örnek*: Ortalama kullanım %40 iken aniden %80'e çıkıp inmesi. Bu, bir uygulamanın (örneğin Chrome'un yeni bir sekme açması veya bir derleme işlemi) anlık yükünü gösterir.

## 4. G/Ç Vekili (IO Proxy)

Bellek sadece depolama değil, akıştır.
*   **Ağ Alınan (Net Recv)**: İndirme trafiği. Büyük indirmeler bellekte tampon (buffer) oluşturur.
*   **Disk Okuma (Disk Read)**: Uygulamalar açılırken veya büyük dosyalar okunurken artar. Yüksek "Page Fault" ile birlikteyse Swap kullanımı anlamına gelebilir.
