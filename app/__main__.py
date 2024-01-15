from my_stacklogging import new_logger
from scan_engine import scan
from scan_comparison import ScanComparison

from dotenv import load_dotenv
from os import environ as env
load_dotenv(".env")

from traceback import format_exc

if __name__ == "__main__":
    log = new_logger()
    try:
        service_path = env.get("SERVICE_PATH", None)
        headless = env.get("HEADLESS", "True") == "True"
        username = env.get("USERNAME", None)

        scan_data = scan(username,service_path, log, headless=headless)
        scan_data.save_to_file()
        log.info("Finished Scan")

        engine = ScanComparison()
        engine.load_from_files()
        scan_comparison_data = engine.compare_scans()
        scan_comparison_data.save_to_file()
        log.info("Finished Comparison", extra=scan_comparison_data.results)

    except Exception as ex:
        log.error(f"{ex.__class__.__name__}: {ex}")
        print(format_exc())
