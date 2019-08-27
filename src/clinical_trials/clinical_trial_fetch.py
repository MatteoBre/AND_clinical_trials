from bs4 import BeautifulSoup
from ..clinical_trials.clinical_trial import ClinicalTrial


# This function returns the location of a file, given the clinical trial ID or the file name
def get_file_location(name):
    inner_folder = name[:7] + 'xxxx'   # I get the name of the inner folder (e.g. NTC0000xxxx)
    location = 'src\\AllPublicXML\\' + inner_folder + '\\' + name   # I set the location
    if name[-4:] != '.xml':
        location += '.xml'    # If the input was the ID, we add .xml because the file name is identical to the ID
    return location    # I return the file location


# This function can be used to get the dom and to do multiple things with it
def get_xml_dom(ID):
    location = get_file_location(ID)
    try:
        # return ET.parse(location)
        return BeautifulSoup(open(location, "r", encoding="utf8").read(), "xml")
    except:
        return None


def get_xml_doms(id_list):  # use this for a list of IDs
    doms = [ClinicalTrial(get_xml_dom(element)) for element in id_list]
    return [dom for dom in doms if dom.clinical_trial is not None]
