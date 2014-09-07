__author__ = 'flashton'


class PatientRecord:
    def __init__(self):
        self.record_id = int
        self.in_hospital_death = int
        self.saps = int
        self.sofa = int
        self.nimap_array = []
        self.nimap_time = []
        self.nimap_median = float
        self.nimap_stdev = float
        self.nimap_window = []