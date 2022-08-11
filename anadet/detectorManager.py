import re

from anadet.dataSearcher import DataSearcher
from anadet.detector import Detector, DetectorProps, SourceProps

class DetectorManager:
    def __init__(self):
        self.detectors = dict()
        self.detCategories = []
        self.dataSearcher = DataSearcher()

    def appendResults(self, filename):
        """
        filename the name of the file with legit .csv results data from Geant4
        """
        # looking for energy info in full filename
        srcProps = None
        energy_list = self.dataSearcher.lookingForEnergyInfo(filename)
        # preority to the last found energy info (closer to the file by the dir tree)
        if energy_list:
            energy = energy_list[-1]['energy']
            energyUnit = energy_list[-1]['energy_unit']
            srcProps = SourceProps(energy, energyUnit)
        else:
            pass # TODO - try to find info in meta file
        if not energy:
            pass # TODO - scenario with unknown source energy

        # looking for num of histories
        nhists = self.dataSearcher.lookingForNhists(filename)
        if not nhists:
            pass # TODO - no nhists in filename, maybe search in meta of doesn't matter
        # looking for det params
        det_name, hist_type, det_type, det_quantity, det_num = self.dataSearcher.lookingForDetNameInfo(filename)
        detProps = DetectorProps(srcProps)
        detProps.setQuantity(det_quantity)
        detProps.setTags(det_type, str(det_num))

        key_name = Detector.createName(detProps)
        if key_name not in self.detectors:
            self.detectors[key_name] = Detector(detProps)
        
        # Now we have detector in the self.detectors list
        self.detectors[key_name].appendResult(filename)


