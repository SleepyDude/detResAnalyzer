import re

class DataSearcher:
    """
    Class looking for specific data in text: energy, number of histories and other
    """
    ENERGY_PATTERN = re.compile(r'(?P<energy>\d+\.?\d*?)\s*?(?P<energy_unit>[M|m|k|u]?eV)')
    NHISTS_PATTERN = re.compile(r'(?P<nhists>\d+\.?\d*)\s*(?P<multiplier>kk+)')
    DETNAME_PATTERN = re.compile(r'(?P<hist_type>h1|h2|h3)_(?P<det_name>.+?)\.csv')

    ENERGY_UNITS = ["MeV", "keV", "eV", "meV", "ueV"]
    DET_QUANTITY_TYPES = ["Phi", "Theta", "Spec"]
    DET_CLASSES = ["Diag", "XWall", "YWall", "Vert"] # TODO - for filtering only, user should be able to set it

    def __init__(self):
        pass

    def lookingForEnergyInfo(self, text):
        res = [m.groupdict() for m in self.ENERGY_PATTERN.finditer(text)]
        for item in res:
            item['energy'] = float(item['energy'])
        return res

    def lookingForNhists(self, text):
        histories = None
        m = self.NHISTS_PATTERN.search(text)
        if m:
            histories = int(m.group('nhists')) * 1e3**len(m.group('multiplier'))
        return histories

    def lookingForDetNameInfo(self, filename: str):
        """
            Looking works only for filename because we have a solid rule for csv files naming in geant4
            return detName, histType, detType, detQuantity, detNum
        Example:
            'results-master_h1_DiagDetPV-2-Phi.csv' filename contains:
                hist_type = h1
                det_name = DiagDetPV-2-Phi
                det_quantity = Phi
                det_num = 2
                det_type = DiagDetPV-- (class of detectors without other additional info)
        """
        detName = detQuantity = histType = detNum = detType = None
        # looking for a hist type and the detector name
        m = self.DETNAME_PATTERN.search(filename)
        if m:
            histType = m.group('hist_type')
            detName  = m.group('det_name')
        if not detName: # should handle this case
            return None
        # looking for additional info such as numering and detector type in det name
        for item in self.DET_QUANTITY_TYPES:
            if item in detName:
                detQuantity = item # TODO - should react on the case if there are more than one Quantity found
        m = re.search(r'(\d+)', detName) # TODO - case with more than one numbers in the name
        if m: # if number found in the name then it belongs to detector numeration
            detNum = int(m.group(0))
        for item in self.DET_CLASSES:
            if item in detName:
                detType = item
        return detName, histType, detType, detQuantity, detNum







        m = self.NHISTS_PATTERN.search(text)
        if m:
            histories = int(m.group('nhists')) * 1e3**len(m.group('multiplier'))
        return histories
