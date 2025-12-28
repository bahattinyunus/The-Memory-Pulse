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
    
    # RAM Table
    ram_table = Table(title="RAM Vital Signs", expand=True)
    ram_table.add_column("Metric", style="cyan")
    ram_table.add_column("Value", style="magenta")
    ram_table.add_row("Total", f"{pulse['ram']['total'] / (1024**3):.2f} GB")
    ram_table.add_row("Available", f"{pulse['ram']['available'] / (1024**3):.2f} GB")
    ram_table.add_row("Used", f"{pulse['ram']['used'] / (1024**3):.2f} GB")
    ram_table.add_row("Usage", f"{pulse['ram']['percent']}%")

    # Swap Table
    swap_table = Table(title="Swap Status", expand=True)
    swap_table.add_column("Metric", style="yellow")
    swap_table.add_column("Value", style="green")
    swap_table.add_row("Total", f"{pulse['swap']['total'] / (1024**3):.2f} GB")
    swap_table.add_row("Used", f"{pulse['swap']['used'] / (1024**3):.2f} GB")
    swap_table.add_row("Usage", f"{pulse['swap']['percent']}%")

    # Analysis Panel
    analysis_text = f"Trend: [bold { 'red' if analysis.get('trend') == 'RISING' else 'green' }]{analysis.get('trend')}[/]\n"
    analysis_text += f"Slope: {analysis.get('slope', 'N/A')}\n"
    analysis_text += f"Records: {len(monitor.history)}\n\n"
    analysis_text += f"[bold]IO Proxy[/]\n"
    analysis_text += f"Net Recv: {io_proxy['net_bytes_recv'] / (1024**2):.2f} MB\n"
    analysis_text += f"Disk Read: {io_proxy['disk_read_bytes'] / (1024**2):.2f} MB"

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )
    layout["header"].update(Panel(Text("THE MEMORY PULSE - DIGITAL CORTEX MONITOR", justify="center", style="bold white on blue")))
    
    layout["main"].split_row(
        Layout(Panel(ram_table, title="Volatile Memory")),
        Layout(Panel(swap_table, title="Page File")),
        Layout(Panel(analysis_text, title="Cortex Analysis"))
    )
    
    return layout

def main():
    parser = argparse.ArgumentParser(description="The Memory Pulse - Elite Monitoring Tool")
    parser.add_argument("--check", action="store_true", help="Run a quick system check and exit")
    args = parser.parse_args()

    monitor = MemoryPulse()
    analyzer = PulseAnalyzer()
    console = Console()

    if args.check:
        pulse = monitor.get_pulse()
        console.print(f"[bold green]System Check Passed[/]")
        console.print(f"RAM: {pulse['ram']['percent']}% | Swap: {pulse['swap']['percent']}%")
        return

    with Live(console=console, refresh_per_second=2) as live:
        try:
            while True:
                live.update(generate_dashboard(monitor, analyzer))
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("[bold red]Monitor Terminated by User.[/]")

if __name__ == "__main__":
    main()
