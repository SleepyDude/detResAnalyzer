import re

from dataSearcher import DataSearcher

class DetectorManager:
    def __init__(self):
        self.detectors = []
        self.detCategories = []
        self.dataSearcher = DataSearcher()

    def appendResults(self, filename):
        """
        filename the name of the file with legit .csv results data from Geant4
        """
        # looking for energy info in full filename
        energy = None
        energy_unit = None
        energy_list = self.dataSearcher.lookingForEnergyInfo(filename)
        # preority to the last found energy info (closer to the file by the dir tree)
        if energy_list:
            energy = energy_list[-1]['energy']
            energy_unit = energy_list[-1]['energy_unit']
        else:
            pass # TODO - try to find info in meta file
        if not energy:
            pass # TODO - scenario with unknown source energy

        # looking for num of histories
        nhists = self.dataSearcher.lookingForNhists(filename)
        if not nhists:
            pass # TODO - no nhists in filename, maybe search in meta of doesn't matter

        # TODO - looking for detector name
        det_name, hist_type, det_type, det_quantity, det_num = self.dataSearcher.lookingForDetNameInfo(filename)

        # TODO - looking for detector quantity type


