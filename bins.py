import json

NUM_BINS_KEY = "num_bins"
BINS_KEY = "bins"
NUM_SPACES_KEY = "num_spaces"
SPACES_KEY = "spaces"
COMPONENT_KEY = "component"
COMPONENT_MODEL_KEY = "component_model"
COMPONENT_MAKE_KEY = "component_make"
QUANTITY_KEY = "quantity"
DATASHEET_KEY = "datasheet"

## Load database file
#  @param filaname Filename to load database from
#  @return read_db Database data
def loadDatabase(filename):
    read_db = ''
    with open(filename, 'r') as file:
        read_db = json.load(file)

    return read_db


## Save database file
#  @param filename Database filename
#  @param bins_db Database data to save to file
def saveDatabase(filename, bins_db):
    with open(filename, 'w') as file:
        json.dump(bins_db, file)


## Check if bin number exists
#  @param bins_db Database data
#  @param bin_num Check for the existance of this bin number
#  @return True if bin number exists in database
#          False if bin number does not exist in database
def checkIfBinExists(bins_db, bin_num):
    search_dict = bins_db[BINS_KEY]
    match = False
    if str(bin_num) in search_dict:
        match = True

    return match


## Check if space number exists
#  @param bins_db Database data
#  @param bin_num Bin number to check
#  @param space_num Check for the existance of this space number
#  @return True if space number exists in bin
#          False if space number does not exist in bin
def checkIfSpaceExists(bins_db, bin_num, space_num):
    spaces_list = getSpaceNums(bins_db, bin_num)
    match = False
    if str(space_num) in spaces_list:
        match = True

    return match


## Check if datasheet exists
#  @param bins_db Database data
#  @param bin_num Bin number to check
#  @param space_num Check for the existance of this space number
#  @return True if space number exists in bin
#          False if space number does not exist in bin
def checkIfDatasheetExists(bins_db, bin_num, space_num):
    found = False
    space_dict = bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)]
    if DATASHEET_KEY in space_dict:
        found = True

    return found


## Return a list of space numbers in a bin
#  @param bins_db Database data
#  @return List with space numbers
def getSpaceNums(bins_db, bin_num):
    spaces_dict = bins_db[BINS_KEY][str(bin_num)][SPACES_KEY]
    space_list = list()
    for num in spaces_dict:
        space_list.append(num)

    return space_list


## Get the number of spaces within a bin
#  @param bins_db Database data
#  @param bin_num Bin number
#  @return num_spaces Number of spaces in bin
def getNumSpaces(bins_db, bin_num):
    num_spaces = bins_db[BINS_KEY][str(bin_num)][NUM_SPACES_KEY]
    return num_spaces


## Set the number of spaces within a bin
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param num_spaces Number of spaces to set
def setNumSpaces(bins_db, bin_num, num_spaces):
    bins_db[BINS_KEY][str(bin_num)][NUM_SPACES_KEY] = num_spaces


## Get data for a bin
#  @param bins_db Database data
#  @param bin_num Bin number
#  @return Dictionary in format of {'space_num' : {'component' : 'name', 'quantity' : #, 'datasheet' : 'datasheet_link'}}
def getBinData(bins_db, bin_num):
    exists = checkIfBinExists(bins_db, bin_num)
    data_dict = dict()
    if exists == True:
        spaces = bins_db[BINS_KEY][str(bin_num)][SPACES_KEY]
        for space_num, space_dict in spaces.items():
            data_dict[space_num] = space_dict

    return data_dict


## Set data for a bin
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param bin_data Dictionary of bin data
def setBinData(bins_db, bin_num, bin_data):
    exists = checkIfBinExists(bins_db, bin_num)
    if exists == True:
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY] = bin_data


## Return a list of current bin numbers
#  @param bins_db Database data
#  @return List with bin numbers
def getBinNums(bins_db):
    bins = bins_db[BINS_KEY]

    all_bins = list()
    for num in bins:
        all_bins.append(num)

    return all_bins

## Move bin to a new bin number
#  @param bins_db Database data
#  @param bin_num Bin number to move
#  @param new_bin_num Bin number to move to
def moveBin(bins_db, bin_num, new_bin_num):
    bin_dict = bins_db[BINS_KEY][str(bin_num)]
    bins_db[BINS_KEY][str(new_bin_num)] = bin_dict
    removeBin(bins_db, bin_num)

## Add an empty bin
#  Need to check that bin does not exist already with checkIfBinExists()
#  @param bins_db Database data
#  @param bin_num Bin number to add
def addBin(bins_db, bin_num):
    bin_str = str(bin_num)
    bins_db[BINS_KEY][bin_str] = dict()
    bins_db[BINS_KEY][bin_str][NUM_SPACES_KEY] = 0
    bins_db[BINS_KEY][bin_str][SPACES_KEY] = dict()
    bins_db[NUM_BINS_KEY] += 1


## Remove a bin
#  Need to check that bin exists with checkIfBinExists()
#  @param bins_db Database data
#  @param bin_num Bin number to remove
def removeBin(bins_db, bin_num):
    write_dict = dict()
    bin_str = str(bin_num)
    for bnum, bdict in bins_db[BINS_KEY].items():
        if bin_str != bnum:
            write_dict[bnum] = bdict

    bins_db[BINS_KEY] = write_dict


## Show info for all spaces in a bin
#  @param bins_db Database data
#  @param bin_num Bin number
def showBinData(bins_db, bin_num):
    SHOW_ORDER = [COMPONENT_KEY, COMPONENT_MODEL_KEY, COMPONENT_MAKE_KEY, QUANTITY_KEY, DATASHEET_KEY]
    data_dict = getBinData(bins_db, bin_num)
    num_spaces = getNumSpaces(bins_db, bin_num)
    print(f'Bin: {bin_num}  Spaces: {num_spaces}')
    print('----------------------------------------------')
    for space_num, space_dict in data_dict.items():
        print(f'Space: {space_num}')
        for key in SHOW_ORDER:
            if key in space_dict:
                print(f'{key}: {space_dict[key]}')
        print('')


## Show info for all bins
#  @param bins_db Database data
def showAllBins(bins_db):
    bin_nums = getBinNums(bins_db)
    bin_nums.sort(key=int)

    for bin in bin_nums:
        showBinData(bins_db, bin)

## Set the component for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
#  @param component Component
def setComponent(bins_db, bin_num, space_num, component):
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][COMPONENT_KEY] = component


## Set the component model for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
#  @param model Component model
def setComponentModel(bins_db, bin_num, space_num, model):
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][COMPONENT_MODEL_KEY] = model


## Set the component make for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
#  @param make Component make
def setComponentMake(bins_db, bin_num, space_num, make):
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][COMPONENT_MAKE_KEY] = make


## Set the component quantity for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
#  @param quantity Component quantity
def setQuantity(bins_db, bin_num, space_num, quantity):
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][QUANTITY_KEY] = quantity


## Get the component datasheet for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
def getDatasheet(bins_db, bin_num, space_num):
        return bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][DATASHEET_KEY]

## Set the component datasheet for a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
#  @param datasheet Component datasheet
def setDatasheet(bins_db, bin_num, space_num, datasheet):
        bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)][DATASHEET_KEY] = datasheet


## Adds a space within a bin
#  Must check for bin existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
def addSpace(bins_db, bin_num, space_num):
    bins_db[BINS_KEY][str(bin_num)][SPACES_KEY][str(space_num)] = dict()


## Removes a space within a bin
#  Must check for bin and space existing before calling
#  @param bins_db Database data
#  @param bin_num Bin number
#  @param space_num Space number
def removeSpace(bins_db, bin_num, space_num):
    bin_dict = getBinData(bins_db, bin_num)
    write_dict = dict()
    space_num_str = str(space_num)
    for snum, sdict in bin_dict.items():
        if space_num_str != snum:
            write_dict[snum] = sdict

    setBinData(bins_db, bin_num, write_dict)

## Search all bins for search word
#  @param bins_db Database data
#  @param search Search words
def searchData(bins_db, search):
    bin_list = getBinNums(bins_db)
    bin_list.sort(key=int)
    for bin in bin_list:
        bin_dict = getBinData(bins_db, bin)
        for snum, sdict in bin_dict.items():
            for key, value in sdict.items():
                if type(value) != int and search.lower() in value.lower():
                    print(f'Bin: {bin}  Space: {snum}')
                    print(f'{key}: {value}\n')
