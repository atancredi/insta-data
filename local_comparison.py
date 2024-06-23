from app.scan_comparison import ScanComparison

engine = ScanComparison()
engine.load_from_files()
scan_comparison_data = engine.compare_scans()
scan_comparison_data.save_to_file()
print("Finished Comparison")
print(scan_comparison_data.results)
