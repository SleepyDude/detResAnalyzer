import re

from anadet.dataSearcher import DataSearcher
from anadet.detector import Detector, DetectorProps, SourceProps, GeomProps
import yaml
from typing import List, Dict

class DetectorManager:
    def __init__(self):
        self.detectors : Dict[str, Detector] = dict()
        self.state = {}
        self.dataSearcher = DataSearcher()
        self.meta_data = dict()
        self.meta_categories = list()

    def appendResults(self, filename: str):
        if filename.endswith('.csv'):
            self.appendResultsCSV(filename)
        elif filename.endswith('.det.txt'):
            det = Detector()
            det.createFromFile(filename)
            name = det.createName(det.detProps)
            self.detectors[name] = det

    def appendResultsCSV(self, filename):
        """
        filename the name of the file with legit .csv results data from Geant4
        """
        # looking for energy info in full filename
        src_props = None
        energy_list = self.dataSearcher.lookingForEnergyInfo(filename)
        # preority to the last found energy info (closer to the file by the dir tree)
        if energy_list:
            energy = energy_list[-1]['energy']
            energy_unit = energy_list[-1]['energy_unit']
            src_props = SourceProps(energy, energy_unit)
        else:
            pass # TODO - try to find info in meta file
        if not src_props:
            print(f"WARNING: can't find energy for filename {filename}")
            # TODO - scenario with unknown source energy

        # looking for num of histories
        nhists = self.dataSearcher.lookingForNhists(filename)
        if not nhists:
            pass # TODO - no nhists in filename, maybe search in meta of doesn't matter
        # looking for det params
        det_name, hist_type, det_type, det_quantity, det_num = self.dataSearcher.lookingForDetNameInfo(filename)
        det_props = DetectorProps(src_props)
        det_props.quantity = det_quantity
        det_props.num = str(det_num)
        det_props.setTag(det_type) # tags is an array
        
        # TODO change this way to get params for detectors
        gp = None
        if self.meta_data:
            keyword_for_meta = det_type + '-' + str(det_num)
            if keyword_for_meta in self.meta_data:
                gp = GeomProps(**self.meta_data[keyword_for_meta])

        det_props.geom_props = gp

        key_name = Detector.createName(det_props)
        if key_name not in self.detectors:
            self.detectors[key_name] = Detector(det_props)
        
        # Now we have detector in the self.detectors list
        self.detectors[key_name].appendResult(filename)

    def readMeta(self, meta_filename):
        loaded_data = None
        with open(meta_filename, 'r') as stream:
            loaded_data = yaml.safe_load(stream)

        self.meta_categories = loaded_data['__Categories'][:]
        for item_key in loaded_data:
            tags = []
            # let's create a keyword for each tag
            for category in self.meta_categories:
                m = re.search(category, item_key)
                if m:
                    tags.append(m.group(0).strip())
            if tags:
                keyword = '-'.join(tags)
                self.meta_data[keyword] = dict(loaded_data[item_key]) # dict for copy!

    def filterEnergy(self, detectors : Dict[str, Detector], energy : float, energy_unit : str) -> Dict[str, Detector]:
        ...
        