import platform
import psutil
import shutil
import subprocess
import time

from print_functions.print_message import print_message

def print_system_info_in_terminal() -> None:
    """
    Print the system information in the terminal.

    This function prints the system information in the terminal using the following information:
    - Operating System
    - OS Version
    - Machine
    - Processor
    - CPU count (logical and physical)
    - Total memory
    - Available memory
    - Disk usage
    - System uptime

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    def get_processor_name():
        """
        Get the processor name.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The processor name.
        
        Raises
        ------
        subprocess.CalledProcessError
            If the subprocess call fails.
        """
        try:
            result = subprocess.run(["lscpu"], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if "Model name" in line:
                    return line.split(":")[1].strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return platform.processor()

    terminal_width = shutil.get_terminal_size().columns
    separator = "=" * terminal_width

    print_message(separator, None)
    print_message("System Information".center(terminal_width), None)
    print_message(f"Operating System: {platform.system()} {platform.release()}", 'info')
    print_message(f"OS Version: {platform.version()}", 'info')
    print_message(f"Machine: {platform.machine()}", 'info')
    print_message(f"Processor: {get_processor_name()}", 'info')
    print_message(f"CPU count: {psutil.cpu_count(logical=True)} (logical), {psutil.cpu_count(logical=False)} (physical)", 'info')
    print_message(f"Total memory: {psutil.virtual_memory().total / (1024 * 1024):.2f} MB", 'info')
    print_message(f"Available memory: {psutil.virtual_memory().available / (1024 * 1024):.2f} MB", 'info')
    print_message(f"Disk usage: {psutil.disk_usage('/').percent}%", 'info')
    # Calculate and print system uptime in days, hours, and seconds
    current_time = time.time()
    boot_time = psutil.boot_time()
    uptime_seconds = current_time - boot_time

    uptime_days = int(uptime_seconds // (24 * 3600))
    uptime_hours = int((uptime_seconds % (24 * 3600)) // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    uptime_remaining_seconds = int(uptime_seconds % 60)
    print_message(f"System Uptime: {uptime_days} days, {uptime_hours} hours, {uptime_minutes} minutes, {uptime_remaining_seconds} seconds", 'info')
    print_message(separator, None)
