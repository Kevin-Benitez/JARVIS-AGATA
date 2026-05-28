def system_monitor(parameters=None, player=None, speak=None, **kwargs):
    action = (parameters or {}).get("action", "full")
    try:
        import psutil
        lines = []
        if action in ("cpu", "full"):
            cpu = psutil.cpu_percent(interval=1)
            lines.append(f"CPU: {cpu}%")
        if action in ("ram", "full"):
            ram = psutil.virtual_memory()
            lines.append(f"RAM: {ram.percent}% usado ({ram.used//1024**2}MB / {ram.total//1024**2}MB)")
        if action in ("disk", "full"):
            disk = psutil.disk_usage("/")
            lines.append(f"Disco: {disk.percent}% ({disk.used//1024**3}GB / {disk.total//1024**3}GB)")
        if action in ("battery", "full"):
            bat = psutil.sensors_battery()
            if bat:
                lines.append(f"Batería: {bat.percent:.0f}% {'(cargando)' if bat.power_plugged else ''}")
        if action in ("processes", "full"):
            procs = sorted(psutil.process_iter(["name", "cpu_percent", "memory_percent"]),
                           key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:5]
            for p in procs:
                lines.append(f"  {p.info['name']}: CPU={p.info['cpu_percent']}% MEM={p.info['memory_percent']:.1f}%")
        if action in ("uptime", "full"):
            import time
            boot = psutil.boot_time()
            up   = int(time.time() - boot)
            h, m = divmod(up // 60, 60)
            lines.append(f"Uptime: {h}h {m}m")
        return "\n".join(lines) if lines else "Sin datos."
    except ImportError:
        return "Instalá psutil: pip install psutil"
    except Exception as e:
        return f"Error: {e}"
