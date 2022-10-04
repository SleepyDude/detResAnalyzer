from typing import List, Dict, Tuple
from math import isclose as icl

from .detector import Detector

def filterEnergies(detectors : Dict[str, Tuple[set, Detector]], energies : List[Tuple[float, str]]) -> Dict[str, Tuple[set, Detector]]:
    res = dict()
    for _, det_pair in detectors.items():
        blocked_set, value = det_pair
        for energy, energy_unit in energies:
            if icl(value.detProps.src_props.energy, energy, abs_tol=1e-14) and value.detProps.src_props.energy_unit == energy_unit:
                newset = blocked_set.copy()
                if len(energies) == 1:
                    newset.add('energy') # if it's only one energy, so we will not write it near the line
                newkey = value.detProps.getKeyname(newset)
                res[newkey] = (newset, value)
    return res
        
def filterQuantity(detectors : Dict[str, Tuple[set, Detector]], quantity : str) -> Dict[str, Tuple[set, Detector]]:
    res = dict()
    for _, det_pair in detectors.items():
        blocked_set, value = det_pair
        if value.detProps.quantity == quantity:
            newset = blocked_set.copy()
            newset.add('quantity')
            newkey = value.detProps.getKeyname(newset)
            res[newkey] = (newset, value)
    return res

def filterTag(detectors : Dict[str, Tuple[set, Detector]], tag : str) -> Dict[str, Tuple[set, Detector]]:
    res = dict()
    for _, det_pair in detectors.items():
        blocked_set, value = det_pair
        if tag in value.detProps.getTags():
            newset = blocked_set.copy()
            newset.add(tag)
            newkey = value.detProps.getKeyname(newset)
            res[newkey] = (newset, value)
    return res

def filterNums(detectors : Dict[str, Tuple[set, Detector]], nums : List[str]) -> Dict[str, Tuple[set, Detector]]:
    res = dict()
    for key, det_pair in detectors.items():
        blocked_set, value = det_pair
        for num in nums:
            if num == value.detProps.num:
                newset = blocked_set.copy()
                res[key] = (newset, value)
    return res

def prep_dets_for_filtering(detectors : Dict[str, Detector]) -> Dict[str, Tuple[set, Detector]]:
    res = dict()
    for key, value in detectors.items():
        res[key] = (set(), value)
    return res

# ordering detector collection
'''
ORDERING DETECTORS
Among the detectors we should have some priority for sorting
For example, there are many different detectors with different params:
    - Quantity
    - Tags (Detector type: Vert, Diag, XWall, YWall)
    - Energy
    - Number (Kind of tag, but the number)
Sort should be done successively over these params, from the top to bottom
Quantity and tags should be as a base
'''

def order_dets(dets: Dict[str, Tuple[set, Detector]]) -> Dict[str, Tuple[set, Detector]]:
    return dict(sorted(dets.items(), key=lambda dtuple: dtuple[1][1]))
