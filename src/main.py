import typer
import time
import json
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from core.pulse_monitor import MemoryPulse
from core.analyzer import PulseAnalyzer
from core.omnibus import OmniBus
from core.grid import MemoryGrid

app = typer.Typer(help="The Memory Pulse: Dijital Bilincin Kalp Atışları")
console = Console()

def generate_dashboard(monitor: MemoryPulse, analyzer: PulseAnalyzer, grid: MemoryGrid) -> Layout:
    pulse = monitor.get_pulse()
    analysis = analyzer.analyze_trend(monitor.history)
    top_processes = grid.scan_sector()
    
    # --- RAM Table ---
    ram_table = Table(title="RAM Yaşamsal Bulgular", expand=True, border_style="cyan")
    ram_table.add_column("Metrik", style="cyan")
    ram_table.add_column("Değer", style="bold white")
    ram_table.add_row("Toplam", f"{pulse['ram']['total'] / (1024**3):.2f} GB")
    ram_table.add_row("Kullanılabilir", f"{pulse['ram']['available'] / (1024**3):.2f} GB")
    ram_table.add_row("Kullanılan", f"{pulse['ram']['used'] / (1024**3):.2f} GB")
    ram_table.add_row("Yük", f"{pulse['ram']['percent']}%")

    # --- Grid (Top Processes) Table ---
    grid_table = Table(title="Memory Grid (Hot Zones)", expand=True, border_style="red")
    grid_table.add_column("PID", style="dim")
    grid_table.add_column("Process", style="bold yellow")
    grid_table.add_column("RSS (MB)", justify="right")
    
    for proc in top_processes[:5]:
        grid_table.add_row(
            str(proc['pid']), 
            proc['name'], 
            f"{proc['rss'] / (1024**2):.1f}"
        )

    # --- Analysis Panel ---
    trend_map = {"RISING": "YÜKSELİYOR 🔺", "FALLING": "DÜŞÜYOR 🔻", "STABLE": "DURAĞAN ⚓", "flat": "VERİ BEKLENİYOR"}
    trend_tr = trend_map.get(analysis.get('trend'), analysis.get('trend'))
    
    analysis_content = f"\n[bold underline]Metacognitive Analiz[/]\n\n"
    analysis_content += f"Dinamik Trend: [bold { 'red' if 'RIS' in str(analysis.get('trend')) else 'green' }]{trend_tr}[/]\n"
    analysis_content += f"Eğim (Slope): {analysis.get('slope', '0.00')}\n"
    analysis_content += f"Canlı Örnekler: {len(monitor.history)}\n"
    
    # --- Layout Construction ---
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3)
    )
    
    layout["header"].update(Panel(Text("🧠 THE MEMORY PULSE - OMNI-BUS AKTİF", justify="center", style="bold white on blue")))
    
    layout["body"].split_row(
        Layout(Panel(ram_table, title="Sistem Nabzı")),
        Layout(Panel(grid_table, title="Grid Tarayıcı")),
        Layout(Panel(analysis_content, title="Overseer Raporu"))
    )
    
    layout["footer"].update(Panel(Text("Press Ctrl+C to disconnect from the Cortex.", justify="center", style="dim")))
    
    return layout

@app.command()
def monitor(interval: float = 0.5):
    """
    Canlı İzleme Modu: Sistemi gerçek zamanlı olarak izler.
    """
    monitor_core = MemoryPulse()
    analyzer = PulseAnalyzer()
    bus = OmniBus() # Initialize the bus
    grid = MemoryGrid()
    
    console.print("[bold green]Bağlantı Kuruluyor... The Omni-Bus başlatılıyor...[/]")
    time.sleep(1)
    
    with Live(refresh_per_second=4, screen=True) as live:
        try:
            while True:
                live.update(generate_dashboard(monitor_core, analyzer, grid))
                time.sleep(interval)
        except KeyboardInterrupt:
            console.print("[bold red]Bağlantı kesildi. İyi günler, Mimar.[/]")

@app.command()
def analyze(output: str = "report.json"):
    """
    Derin Analiz Raporu: Anlık durumun fotoğrafını çeker ve kaydeder.
    """
    console.print(f"[yellow]Analiz başlatılıyor... Çıktı hedefi: {output}[/]")
    
    monitor_core = MemoryPulse()
    monitor_core.get_pulse() # Warmup
    time.sleep(0.5)
    pulse = monitor_core.get_pulse()
    
    grid = MemoryGrid()
    sectors = grid.scan_sector()
    
    report = {
        "meta": {
            "timestamp": time.time(),
            "tool": "The Memory Pulse",
            "version": "1.0.0"
        },
        "system_pulse": pulse,
        "memory_grid_snapshot": sectors
    }
    
    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
        
    console.print(f"[bold green]Rapor başarıyla oluşturuldu: {output}[/]")

if __name__ == "__main__":
    app()
