import re

class DataSearcher:
    """
    Class looking for specific data in text: energy, number of histories and other
    """
    ENERGY_PATTERN = re.compile(r'(?P<energy>\d+\.?\d*?)\s*?(?P<energy_unit>[M|m|k|u]?eV)')
    ENERGY_UNITS = ["MeV", "keV", "eV", "meV", "ueV"]
    NHISTS_PATTERN = re.compile(r'(?P<nhists>\d+\.?\d*)\s*(?P<multiplier>kk+)')

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
