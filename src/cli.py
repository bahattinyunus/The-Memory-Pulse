import time
import argparse
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.pulse_monitor import MemoryPulse
from core.analyzer import PulseAnalyzer

def generate_dashboard(monitor, analyzer):
    pulse = monitor.get_pulse()
    analysis = analyzer.analyze_trend(monitor.history)
    io_proxy = monitor.get_system_bandwidth_proxy()
    
    # RAM Tablosu
    ram_table = Table(title="RAM Yaşamsal Bulgular", expand=True)
    ram_table.add_column("Metrik", style="cyan")
    ram_table.add_column("Değer", style="magenta")
    ram_table.add_row("Toplam", f"{pulse['ram']['total'] / (1024**3):.2f} GB")
    ram_table.add_row("Kullanılabilir", f"{pulse['ram']['available'] / (1024**3):.2f} GB")
    ram_table.add_row("Kullanılan", f"{pulse['ram']['used'] / (1024**3):.2f} GB")
    ram_table.add_row("Kullanım", f"{pulse['ram']['percent']}%")

    # Swap Tablosu
    swap_table = Table(title="Takas Alanı (Swap) Durumu", expand=True)
    swap_table.add_column("Metrik", style="yellow")
    swap_table.add_column("Değer", style="green")
    swap_table.add_row("Toplam", f"{pulse['swap']['total'] / (1024**3):.2f} GB")
    swap_table.add_row("Kullanılan", f"{pulse['swap']['used'] / (1024**3):.2f} GB")
    swap_table.add_row("Kullanım", f"{pulse['swap']['percent']}%")

    # Analiz Paneli
    trend_map = {"RISING": "YÜKSELİYOR", "FALLING": "DÜŞÜYOR", "STABLE": "DURAĞAN", "flat": "DÜZ"}
    trend_tr = trend_map.get(analysis.get('trend'), analysis.get('trend'))
    
    analysis_text = f"Trend: [bold { 'red' if analysis.get('trend') == 'RISING' else 'green' }]{trend_tr}[/]\n"
    analysis_text += f"Eğim: {analysis.get('slope', 'YOK')}\n"
    analysis_text += f"Kayıtlar: {len(monitor.history)}\n\n"
    analysis_text += f"[bold]G/Ç Vekili[/]\n"
    analysis_text += f"Ağ Alınan: {io_proxy['net_bytes_recv'] / (1024**2):.2f} MB\n"
    analysis_text += f"Disk Okuma: {io_proxy['disk_read_bytes'] / (1024**2):.2f} MB"

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )
    layout["header"].update(Panel(Text("THE MEMORY PULSE - DİJİTAL KORTEKS MONİTÖRÜ", justify="center", style="bold white on blue")))
    
    layout["main"].split_row(
        Layout(Panel(ram_table, title="Uçucu Bellek")),
        Layout(Panel(swap_table, title="Disk Belleği")),
        Layout(Panel(analysis_text, title="Korteks Analizi"))
    )
    
    return layout

def main():
    parser = argparse.ArgumentParser(description="The Memory Pulse - Elit İzleme Aracı")
    parser.add_argument("--check", action="store_true", help="Hızlı bir sistem kontrolü yap ve çık")
    args = parser.parse_args()

    monitor = MemoryPulse()
    analyzer = PulseAnalyzer()
    console = Console()

    if args.check:
        pulse = monitor.get_pulse()
        console.print(f"[bold green]Sistem Kontrolü Başarılı[/]")
        console.print(f"RAM: {pulse['ram']['percent']}% | Swap: {pulse['swap']['percent']}%")
        return

    with Live(console=console, refresh_per_second=2) as live:
        try:
            while True:
                live.update(generate_dashboard(monitor, analyzer))
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("[bold red]Monitör Kullanıcı Tarafından Sonlandırıldı.[/]")

if __name__ == "__main__":
    main()
