import cmd
import bins
import subprocess

ERR_BIN_POS_INT = 'ERROR: Bin must be a positive integer'
ERR_SPACE_POS_INT = 'ERROR: Space must be a positive integer'
ERR_NUM_SPACE_POS_INT = 'ERROR: Number of spaces must be a positive integer'
ERR_QUANT_POS_INT = 'ERROR: Quanitity must be a positive integer'
ERR_INVALID_ARGS = 'ERROR: Invalid arguments'
ERR_INVALID_CMD = 'ERROR: Invalid command'
ERR_BIN_NOT_EXIST = 'ERROR: Bin does not exist'
ERR_BIN_EXIST = 'ERROR: Bin already exists'
ERR_SPACE_NOT_EXIST = 'ERROR: Space does not exist'
ERR_SPACE_EXIST = 'ERROR: Space already exists'
ERR_DATASHEET_NOT_EXIST = 'ERROR: Datasheet does not exist'

COMPONENT = 0
COMPONENT_MODEL = 1
COMPONENT_MAKE = 2
QUANTITY = 3
DATASHEET = 4
valid_fields = ['component', 'component_model', 'component_make', 'quantity', 'datasheet']

class BinsCmd(cmd.Cmd):
    intro = 'BinsDB'
    prompt = '(bin)'
    file = None

    def help_show(self):
        print('\nShow the contents of a bin\n\n' +
              'Usage:\n'
              'show <bin number>\n\n'
              'To show all bins\n' +
              'show all\n\n' +
              'To show free spaces\n' +
              'show free\n')

    def do_show(self, arg):
        parseShow(arg)

    def help_set(self):
        print('\nSet values for a bin\n\n' +
              'Usage:\n\n' +
              'To set data for a space in a bin:\n' +
              'set <bin number> <space number> <field> <new value>\n\n' +
              'To set the number of spaces in a bin:\n' +
              'set <bin number> spaces <number of spaces in bin>\n')

    def do_set(self, arg):
        parseSet(arg)

    def help_add(self):
        print('\nAdd an empty bin\n\n' +
              'Usage:\n\n' +
              'add bin <bin number>\n\n' +
              'add bin <bin number> <number of spaces>\n\n' +
              'Add a space to a bin\n\n' +
              'add space <bin number> <space number>\n')

    def do_add(self, arg):
        parseAdd(arg)

    def help_remove(self):
        print('\nRemove a bin or a space\n\n'+
              'Usage:\n\n' +
              'remove bin <bin number>\n\n' +
              'remove space <bin number> <space number>\n')

    def do_remove(self, arg):
        parseRemove(arg)

    def help_move(self):
        print('\nMove bin to new bin number.\n\n' +
              'Usage:\n\n' +
              'move <bin number> <new bin number>\n')

    def do_move(self, arg):
        parseMove(arg)

    def help_save(self):
        print('\nSaves the database\n\n' +
              'Usage: \n\n' +
              'save\n')

    def do_save(self, arg):
        bins.saveDatabase('cmd_db_test.json', db)

    def help_search(self):
        print('\nSearches the databse\n\n' +
              'Usage:\n\n' +
              'search <what to search>\n')

    def do_search(self, arg):
        parseSearch(arg)

    def help_datasheet(self):
        print('\nOpen datasheet for a space\n\n'+
              'Usage:\n\n' +
              'datasheet <bin number> <space number>\n')

    def do_datasheet(self, arg):
        parseDatasheet(arg)

    def do_exit(self, arg):
        'Exit'
        return True

## Validates that string is a number and converts to int
#  @param num_str String to validate and convert
def validateNumber(num_str):
    error = False
    num = 0

    if num_str.isdigit() == True:
        num = int(num_str)
        if num < 0:
            error = True
            num = -1
    else:
        error = True

    return error, num

## Show command
#  @param arg Command arguments
def parseShow(arg):
    if arg == 'all':
        bins.showAllBins(db)
    elif arg == 'free':
        bin_list = bins.getBinNums(db)
        bin_list.sort(key=int)
        for bin in bin_list:
            free_spaces = list()
            space_list = bins.getSpaceNums(db, bin)
            num_spaces = bins.getNumSpaces(db, bin)
            if len(space_list) < num_spaces:
                for i in range(1, num_spaces+1):
                    if str(i) not in space_list:
                        free_spaces.append(i)
            if len(free_spaces) != 0:
                print(f'Bin: {bin}')
                print(f'Free spaces: ', end='')
                for space in free_spaces:
                    print(f'{space}, ', end='')
                print('\n')
    elif arg.isdigit() == True:
        bin_err, bin = validateNumber(arg)
        if bin_err == False:
            bins.showBinData(db, bin)
        else:
            print(ERR_BIN_POS_INT)
    else:
        print(ERR_INVALID_ARGS)

## Set command
#  @param arg Command arguments
def parseSet(arg):
    parse_args = arg.split(' ')
    num_args = len(parse_args)

    if num_args == 3:
        parseSetSpaces(parse_args)
    elif num_args >= 4:
        parseSetFields(parse_args, num_args)
    else:
        print(ERR_INVALID_ARGS)

## Set spaces command
#  @param parse_args Command arguments
def parseSetSpaces(parse_args):
    spaces = parse_args[1]
    if spaces == 'spaces':
        bin_err, bin = validateNumber(parse_args[0])
        spaces_err, num_spaces = validateNumber(parse_args[2])
        if bin_err == False and spaces_err == False:
            exists = bins.checkIfBinExists(db, bin)
            if exists == True:
                bins.setNumSpaces(db, bin, num_spaces)
            else:
                print(ERR_BIN_NOT_EXIST)
        else:
            print(ERR_BIN_POS_INT)
            print(ERR_NUM_SPACE_POS_INT)
    else:
        print(ERR_INVALID_CMD)

## Set fields command
#  @param parse_args Command arguments
#  @param num_args Number of command arguments
def parseSetFields(parse_args, num_args):
    bin_err, bin = validateNumber(parse_args[0])
    space_err, space = validateNumber(parse_args[1])
    field = parse_args[2]

    if bin_err == True:
        print(ERR_BIN_POS_INT)

    if space_err == True:
        print(ERR_SPACE_POS_INT)

    bin_exists = bins.checkIfBinExists(db, bin)
    space_exists = bins.checkIfSpaceExists(db, bin, space)

    if(bin_exists == False):
        print(ERR_BIN_NOT_EXIST)
        bin_err = True

    if(space_exists == False):
        print(ERR_SPACE_NOT_EXIST)
        space_err = True

    if bin_err == False and space_err == False and field in valid_fields:
        field = parse_args[2]
        value = parse_args[3:]
        value_str = str()
        for v in value:
            value_str += v
            value_str += ' '
        # Remove trailing space
        value_str = value_str[:-1]

        if field == valid_fields[COMPONENT]:
            bins.setComponent(db, bin, space, value_str)
        elif field == valid_fields[COMPONENT_MODEL]:
            bins.setComponentModel(db, bin, space, value_str)
        elif field == valid_fields[COMPONENT_MAKE]:
            bins.setComponentMake(db, bin, space, value_str)
        elif field == valid_fields[QUANTITY]:
            if num_args == 4:
                quantity_err, quantity = validateNumber(value_str)
                if quantity_err == False:
                    bins.setQuantity(db, bin, space, quantity)
                else:
                    print(ERR_QUANT_POS_INT)
            else:
                print(ERR_INVALID_ARGS)
        else:
            bins.setDatasheet(db, bin, space, value_str)

## Add command
#  @param arg Command arguments
def parseAdd(arg):
    parse_args = arg.split(' ')
    num_args = len(parse_args)

    if parse_args[0] == 'bin':
        if num_args == 2:
            addBin(parse_args[1])
        elif num_args == 3:
            addBin(parse_args[1], parse_args[2])
        else:
            print(ERR_INVALID_ARGS)
    elif parse_args[0] == 'space':
        if num_args == 3:
            addSpace(parse_args[1], parse_args[2])
    else:
        print(ERR_INVALID_ARGS)

## Add bin command
#  @param arg Command arguments
def addBin(bin_str, num_spaces_str=None):
    bin_err, bin = validateNumber(bin_str)
    if bin_err == False:
        exists = bins.checkIfBinExists(db, bin)
        if exists == False:
            if num_spaces_str == None:
                bins.addBin(db, bin)
                bins.setNumSpaces(db, bin, 0)
            else:
                num_spaces_err, num_spaces = validateNumber(num_spaces_str)
                if num_spaces_err == False:
                    bins.addBin(db, bin)
                    bins.setNumSpaces(db, bin, num_spaces)
                else:
                    print(ERR_SPACE_POS_INT)
        else:
            print(ERR_BIN_EXIST)
    else:
        print(ERR_BIN_POS_INT)

## Add space command
#  @param arg Command arguments
def addSpace(bin_str, space_str):
    bin_err, bin = validateNumber(bin_str)
    if bin_err == False:
        exists = bins.checkIfBinExists(db, bin)
        if exists == True:
            space_err, space = validateNumber(space_str)
            if space_err == False:
                space_exists = bins.checkIfSpaceExists(db, bin, space)
                if space_exists == False:
                    bins.addSpace(db, bin, space)
                else:
                    print(ERR_SPACE_EXIST)
            else:
                print(ERR_SPACE_POS_INT)
        else:
            print(ERR_BIN_NOT_EXIST)
    else:
        print(ERR_BIN_POS_INT)

## Remove command
#  @param arg Command arguments
def parseRemove(arg):
    parse_args = arg.split(' ')
    num_args = len(parse_args)

    if parse_args[0] == 'bin' and num_args == 2:
        bin_err, bin = validateNumber(parse_args[1])
        if bin_err == False:
            bins.removeBin(db, bin)
        else:
            print(ERR_BIN_POS_INT)
    elif parse_args[0] == 'space' and num_args == 3:
        bin_err, bin = validateNumber(parse_args[1])
        space_err, space = validateNumber(parse_args[2])
        if bin_err == False and space_err == False:
            bins.removeSpace(db, bin, space)
        else:
            print(ERR_BIN_POS_INT)
            print(ERR_SPACE_POS_INT)
    else:
        print(ERR_INVALID_ARGS)

## Move command
#  @param arg Command arguments
def parseMove(arg):
    parse_args = arg.split(' ')
    num_args = len(parse_args)

    bin_err, bin = validateNumber(parse_args[0])
    new_bin_err, new_bin = validateNumber(parse_args[1])

    if num_args == 2:
        if bin_err == False and new_bin_err == False:
            bin_exists = bins.checkIfBinExists(db, bin)
            new_bin_exists = bins.checkIfBinExists(db, new_bin)
            if bin_exists == True and new_bin_exists == False:
                bins.moveBin(db, bin, new_bin)
            else:
                print(ERR_BIN_NOT_EXIST)
        else:
            print(ERR_INVALID_ARGS)
    else:
        print(ERR_INVALID_ARGS)

## Search command
#  @param arg Command arguments
def parseSearch(arg):
    bins.searchData(db, arg)

## Open datasheet
def parseDatasheet(arg):
    parse_args = arg.split(' ')
    num_args = len(parse_args)

    bin_err, bin = validateNumber(parse_args[0])
    space_err, space = validateNumber(parse_args[1])

    if num_args == 2:
        if bin_err == False and space_err == False:
            bin_exists = bins.checkIfBinExists(db, bin)
            if bin_exists == True:
                space_exists = bins.checkIfSpaceExists(db, bin, space)
                if space_exists == True:
                    datasheet_exists = bins.checkIfDatasheetExists(db, bin, space)
                    if datasheet_exists == True:
                        datasheet = bins.getDatasheet(db, bin, space)
                        subprocess.run(["open", datasheet])
                    else:
                        print(ERR_DATASHEET_NOT_EXIST)
                else:
                    print(ERR_SPACE_NOT_EXIST)
            else:
                print(ERR_BIN_NOT_EXIST)
        else:
            print(ERR_INVALID_ARGS)
    else:
        print(ERR_INVALID_ARGS)



db = bins.loadDatabase('db.json')

BinsCmd().cmdloop()
