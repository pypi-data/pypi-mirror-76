MMT_CATALOG_ID = 486
MMT_PROGRAM_ID = 977
MMT_JSON_KEYS = ("id", "ra", "objectid", "observationtype", "moon", "seeing", "photometric", "priority", "dec",
                 "ra_decimal", "dec_decimal", "pm_ra", "pm_dec", "magnitude", "exposuretime", "numberexposures",
                 "visits", "onevisitpernight", "filter", "grism", "grating", "centralwavelength", "readtab",
                 "gain", "dithersize", "epoch", "submitted", "modified", "notes", "pa", "maskid", "slitwidth",
                 "slitwidthproperty", "iscomplete", "disabled", "notify", "locked", "findingchartfilename",
                 "instrumentid", "targetofopportunity", "reduced", "exposuretimeremaining", "totallength",
                 "totallengthformatted", "exposuretimeremainingformatted", "exposuretimecompleted",
                 "percentcompleted", "offsetstars", "details", "mask")

MMT_REQUIRED_KEYS = ['ra', 'dec', 'epoch', 'exposuretime', 'observationtype', 'numberexposures', 'observationtype']

def isInt(i):
    try:
        ret = int(i)
        return True
    except:
        return False


def isFloat(i):
    try:
        ret = float(i)
        return True
    except:
        return False
        

from . import mmtapi
