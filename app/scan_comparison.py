from datetime import datetime
from os import listdir
from json import loads

from data_models import ScanComparisonData, ScanData, TimeObject

class ScanComparison:

    most_recent_scan: ScanData
    least_recent_scan: ScanData

    def load_from_files(self):

        folder_path = "results"

        # Filter out files that don't match the expected format
        valid_files = [file_name for file_name in listdir(folder_path) if file_name.startswith("result_")]

        # Sort the files by their datetime value
        sorted_files = sorted(valid_files, key=lambda file_name: datetime.strptime(file_name[7:23], "%Y_%m_%d-%H_%M"), reverse=True)

        # Get the most recent and second most recent files
        most_recent_file = sorted_files[0]
        second_most_recent_file = sorted_files[1]

        # Read the most recent and second most recent files
        with open(f"{folder_path}/{most_recent_file}", "r") as f:
            self.most_recent_scan = ScanData().load_from_dict(loads(f.read()))
        with open(f"{folder_path}/{second_most_recent_file}", "r") as f:
            self.least_recent_scan = ScanData().load_from_dict(loads(f.read()))

    def compare_scans(self):

        # get gained followers
        gained_followers = []
        for fl in self.most_recent_scan.followers:
            if fl.username not in [i.username for i in self.least_recent_scan.followers]:
                gained_followers.append(fl)

        # get lost followers
        lost_followers = []
        for fl in self.least_recent_scan.followers:
            if fl.username not in [i.username for i in self.most_recent_scan.followers]:
                lost_followers.append(fl)

        res = ScanComparisonData()
        res.gained_followers = gained_followers
        res.lost_followers = lost_followers
        res.time_object = TimeObject(current_scan=self.most_recent_scan.date, reference_scan=self.least_recent_scan.date)
        
        res.save_to_file()
        return res