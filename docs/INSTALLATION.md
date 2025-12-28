# 🛠️ Detaylı Kurulum ve Sorun Giderme Rehberi

**The Memory Pulse** kurulumu genellikle basittir, ancak farklı işletim sistemleri ve Python ortamları için özel adımlar gerekebilir.

## Ön Gereksinimler

Kuruluma başlamadan önce sisteminizde aşağıdakilerin olduğundan emin olun:

1.  **Python 3.8 veya üzeri**:
    *   Kontrol etmek için terminalde: `python --version`
2.  **pip (Python Paket Yöneticisi)**:
    *   Kontrol etmek için: `pip --version`
3.  **Git**:
    *   Repoyu klonlamak için gereklidir.

## İşletim Sistemi Spesifik Kurulumlar

### 🪟 Windows

1.  CMD veya PowerShell'i **Yönetici Olarak** çalıştırın (bazı sistem metrikleri için gereklidir).
2.  Repoyu klonlayın:
    ```powershell
    git clone https://github.com/kullanici-adiniz/The-Memory-Pulse.git
    cd The-Memory-Pulse
    ```
3.  Sanal Ortam (Opsiyonel ama Önerilir):
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
4.  Bağımlılıkları yükleyin:
    ```powershell
    pip install -r requirements.txt
    ```

### 🐧 Linux (Ubuntu/Debian)

1.  Sistem paketlerini güncelleyin:
    ```bash
    sudo apt update && sudo apt install python3-pip python3-venv git
    ```
2.  Klonlayın ve kurun:
    ```bash
    git clone https://github.com/kullanici-adiniz/The-Memory-Pulse.git
    cd The-Memory-Pulse
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### 🍎 macOS

1.  Terminali açın.
2.  Klonlayın ve kurun:
    ```bash
    git clone https://github.com/kullanici-adiniz/The-Memory-Pulse.git
    cd The-Memory-Pulse
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Sık Karşılaşılan Sorunlar (Troubleshooting)

### `psutil` Yükleme Hatası
Eğer `pip install psutil` sırasında hata alıyorsanız, Python geliştirme başlıklarına (python-dev) ihtiyacınız olabilir.
*   **Linux**: `sudo apt install python3-dev`
*   **Windows**: Visual C++ Build Tools'un kurulu olduğundan emin olun.

### İzin Hataları (Permission Denied)
Bazı sistem metriklerini (örneğin süreç bazlı detaylı analizler) okumak için root/yönetici yetkisi gerekebilir.
*   Linux/Mac'te `sudo python src/cli.py` ile çalıştırmayı deneyin.

### Terminalde Renkler Görünmüyor
`rich` kütüphanesi modern bir terminal gerektirir.
*   Windows'ta eski `cmd.exe` yerine **Windows Terminal** veya **PowerShell** kullanın.
*   VS Code entegre terminali tam desteklidir.
