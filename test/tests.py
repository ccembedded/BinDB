import unittest
import sys

sys.path.append('..')

import bins

# Test checkIfBinExists()
class CheckIfBinExists(unittest.TestCase):
    # If a bin does not exist checkIfBinExists() should return False
    def testNotExist(self):
        db = bins.loadDatabase('dbs/emptydb.json')
        for i in range(1, 11):
            exists = bins.checkIfBinExists(db, i)
            self.assertEqual(exists, False, 'FAIL: checkIfBinExists() not exist')

    # If a bin exists checkIfBinExists() should return True
    def testExists(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        for i in range(1, 11):
            exists = bins.checkIfBinExists(db, i)
            if i < 2:
                self.assertEqual(exists, True, 'FAIL: checkIfBinExists() exists')
            else:
                self.assertEqual(exists, False, 'FAIL: checkIfBinExists() exists')


# Test checkIfSpaceExists()
class CheckIfSpaceExists(unittest.TestCase):
    # If a space does not exist checkIfSpaceExists() should return False
    def testNotExist(self):
        db = bins.loadDatabase('dbs/one_bin_no_spaces_db.json')
        for i in range(1, 11):
            exists = bins.checkIfSpaceExists(db, 1, i)
            self.assertEqual(exists, False, 'FAIL: checkIfSpaceExists() not exist')

    # If a space exists checkIfSpaceExists() should return True
    def testExists(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        for i in range(1, 11):
            exists = bins.checkIfSpaceExists(db, 1, i)
            if i < 5:
                self.assertEqual(exists, True, 'FAIL: checkIfSpaceExists() exists')
            else:
                self.assertEqual(exists, False, 'FAIL: checkIfSpaceExists() exists')


# Test checkIfDatasheetExists()
class CheckIfDatasheetExists(unittest.TestCase):
    # Test a space with no datasheet
    def testNoDatasheetExists(self):
        bin = 1
        space = 2
        db = bins.loadDatabase('dbs/one_bin_four_spaces_no_datasheet_2_db.json')
        exists = bins.checkIfDatasheetExists(db, bin, space)
        self.assertEqual(exists, False, 'FAIL: checkIfDatasheetExists() datasheet exists')

    # Test a space wtih a datasheet
    def testDatasheetExists(self):
        bin = 1
        space = 4
        db = bins.loadDatabase('dbs/one_bin_four_spaces_no_datasheet_2_db.json')
        exists = bins.checkIfDatasheetExists(db, bin, space)
        self.assertEqual(exists, True, 'FAIL: checkIfDatasheetExists() datasheet does not exist')


# Test getSpaceNums()
class GetSpaceNums(unittest.TestCase):
    # If there are no spaces in a bin an empty list is returned
    def testNoSpaces(self):
        db = bins.loadDatabase('dbs/one_bin_no_spaces_db.json')
        spaces = bins.getSpaceNums(db, 1)
        self.assertEqual(spaces, list(), 'FAIL: getSpaceNums() no spaces')

    # If there are spaces in a bin a list of spaces is returned
    def testSpaces(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        expected_list = ['1', '2', '3', '4']
        spaces = bins.getSpaceNums(db, 1)
        self.assertEqual(spaces, expected_list, 'FAIL: getSpaceNums() spaces')


# Test getNumSpaces()
class GetNumSpaces(unittest.TestCase):
    # No spaces in a bin
    def testNoSpaces(self):
        db = bins.loadDatabase('dbs/one_bin_no_spaces_db.json')
        num_spaces = bins.getNumSpaces(db, 1)
        self.assertEqual(num_spaces, 0, 'FAIL: getNumSpaces() 0 spaces')

    # There are spaces in the bin
    def testFourSpaces(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        num_spaces = bins.getNumSpaces(db, 1)
        self.assertEqual(num_spaces, 4, 'FAIL: getNumSpaces() 4 spaces')


# Test setNumSpaces()
class SetNumSpaces(unittest.TestCase):
    # Test db has four spaces in a bin
    # Change the number of spaces in the bin and verify that the value has changed
    def testChangeNumSpaces(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        num_spaces = bins.getNumSpaces(db, 1)
        self.assertEqual(num_spaces, 4, 'FAIL: setNumSpaces() pre-test')
        bins.setNumSpaces(db, 1, 8)
        num_spaces = bins.getNumSpaces(db, 1)
        self.assertEqual(num_spaces, 8, 'FAIL: setNumSpaces() 8')


# Test getBinData()
class GetBinData(unittest.TestCase):
    # Get data from a bin and verify it matches expected values
    def testGetBinData(self):
        bin = 1
        space = 2
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        data_dict = bins.getBinData(db, bin)
        self.assertEqual(data_dict[str(space)]['component'], 'Component_1_2', 'FAIL: getBinData() component')
        self.assertEqual(data_dict[str(space)]['component_model'], 'Component_Model_1_2', 'FAIL: getBinData() component model')
        self.assertEqual(data_dict[str(space)]['component_make'], 'Component_Make_1_2', 'FAIL: getBinData() component make')
        self.assertEqual(data_dict[str(space)]['quantity'], 2, 'FAIL: getBinData() quanitity')
        self.assertEqual(data_dict[str(space)]['datasheet'], 'datasheets/1_2', 'FAIL: getBinData() datasheet')


# Test setBinData()
class SetBinData(unittest.TestCase):
    # Get bin data
    # Modify a space
    # Set bin data
    # Get bin data again and verify it changed
    def testSetBinData(self):
        bin = 1
        space = 4
        component = 'Component_1_4_SET'
        model = 'Component_Model_1_4_SET'
        make = 'Component_Make_1_4_SET'
        quantity = 69
        datasheet = 'datasheets/1_4_SET'
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        data_dict = bins.getBinData(db, bin)
        data_dict[str(space)]['component'] = component
        data_dict[str(space)]['component_model'] = model
        data_dict[str(space)]['component_make'] = make
        data_dict[str(space)]['quantity'] = quantity
        data_dict[str(space)]['datasheet'] = datasheet
        bins.setBinData(db, bin, data_dict)
        changed_dict = bins.getBinData(db, bin)
        self.assertEqual(changed_dict[str(space)]['component'], component, 'FAIL: setBinData() component')
        self.assertEqual(changed_dict[str(space)]['component_model'], model, 'FAIL: setBinData() model')
        self.assertEqual(changed_dict[str(space)]['component_make'], make, 'FAIL: setBinData() make')
        self.assertEqual(changed_dict[str(space)]['quantity'], quantity, 'FAIL: setBinData() component')
        self.assertEqual(changed_dict[str(space)]['datasheet'], datasheet, 'FAIL: setBinData() datasheet')


# Test getBinNums()
class GetBinNums(unittest.TestCase):
    # Compare bin numbers to expected
    def testGetBinNums(self):
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        expected_numz = ['1', '2', '3', '4']
        numz = bins.getBinNums(db)
        self.assertListEqual(expected_numz, numz, 'FAIL: getBinNums()')


# Test moveBin()
class MoveBin(unittest.TestCase):
    # Check that bin to move exists
    # Check that bin number moving to does not exist
    # Move bin
    # Check that new bin number exists and old number does not
    def testMoveBin(self):
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        from_bin = 4
        to_bin = 8
        from_exists = bins.checkIfBinExists(db, from_bin)
        to_exists = bins.checkIfBinExists(db, to_bin)
        self.assertEqual(from_exists, True, 'ERROR: moveBin() from bin does not exist')
        self.assertEqual(to_exists, False, 'ERROR: moveBin() to bin exists')
        bins.moveBin(db, from_bin, to_bin)
        from_exists = bins.checkIfBinExists(db, from_bin)
        to_exists = bins.checkIfBinExists(db, to_bin)
        self.assertEqual(from_exists, False, 'ERROR: moveBin() to bin exists after move')
        self.assertEqual(to_exists, True, 'ERROR: moveBin() to bin does not exist after move')


# Test addBin()
class AddBin(unittest.TestCase):
    # Verify bin number does not exist
    # Add a bin and check if it exists
    def testAddBin(self):
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        exists = bins.checkIfBinExists(db, 8)
        self.assertEqual(exists, False, 'FAIL: addBin() bin already exists')
        bins.addBin(db, 8)
        exists = bins.checkIfBinExists(db, 8)
        self.assertEqual(exists, True, 'FAIL: addBin() bin not added')

# Test removeBin()
class RemoveBin(unittest.TestCase):
    # Verify that bin exists
    # Remove bin and check if it exists
    def testRemoveBin(self):
        rm_bin = 3
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, rm_bin)
        self.assertEqual(exists, True, 'FAIL: removeBin() bin does not exist')
        bins.removeBin(db, 3)
        exists = bins.checkIfBinExists(db, rm_bin)
        self.assertEqual(exists, False, 'FAIL: removeBin() bin not removed')


# Test setComponent()
class SetComponent(unittest.TestCase):
    # Set a component name and check that it changed
    def testSetComponent(self):
        bin = 1
        space = 4
        key = 'component'
        component = 'Component_1_4_SET'
        db = bins.loadDatabase('dbs/one_bin_four_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: setComponent() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: setComponent() space does not exist')
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], 'Component_1_4', 'FAIL: setComponent() component does not match')
        bins.setComponent(db, bin, space, component)
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], component, 'FAIL: setComponent() new component does not match')


# Test setComponentModel()
class SetComponentModel(unittest.TestCase):
    # Set a component model and check that it changed
    def testSetComponentModel(self):
        bin = 3
        space = 7
        key = 'component_model'
        model = 'Component_Model_3_7_SET'
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: setComponentModel() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: setComponentModel() space does not exist')
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], 'Component_Model_3_7', 'FAIL: setComponentModel() model does not match')
        bins.setComponentModel(db, bin, space, model)
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], model, 'FAIL: setComponentModel() new model does not match')


# Test setComponentMake()
class SetComponentMake(unittest.TestCase):
    # Set a component make and check that it changed
    def testSetComponentMake(self):
        bin = 4
        space = 1
        key = 'component_make'
        make = 'Component_Make_4_1_SET'
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: setComponentMake() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: setComponentMake() space does not exist')
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], 'Component_Make_4_1', 'FAIL: setComponentMake() model does not match')
        bins.setComponentMake(db, bin, space, make)
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], make, 'FAIL: setComponentMake() new model does not match')


# Test setQuantity()
class SetQuantity(unittest.TestCase):
    # Set a component quantity and check that it changed
    def testSetQuantity(self):
        bin = 1
        space = 4
        key = 'quantity'
        quantity = 69
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: setQuantity() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: setQuantity() space does not exist')
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], 4, 'FAIL: setQuantity() model does not match')
        bins.setQuantity(db, bin, space, quantity)
        bin_dict = bins.getBinData(db, bin)
        self.assertEqual(bin_dict[str(space)][key], quantity, 'FAIL: setQuantity() new model does not match')


# Test getDatasheet()
class GetDatasheet(unittest.TestCase):
    # Get a datasheet from a space and check that it matches expected value
    def testGetDatasheet(self):
        bin = 3
        space = 5
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: getDatasheet() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: getDatasheet() space does not exist')
        datasheet = bins.getDatasheet(db, bin, space)
        self.assertEqual(datasheet, 'datasheets/3_5', 'FAIL: getDatasheet() datasheet does not match')


# Test setDatasheet()
class SetDatasheet(unittest.TestCase):
    # Set a datasheet and check that it matches
    def testSetDatasheet(self):
        bin = 3
        space = 5
        datasheet = 'datasheets/3_5_SET'
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: setQuantity() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: setQuantity() space does not exist')
        bins.setDatasheet(db, bin, space, datasheet)
        read_val = bins.getDatasheet(db, bin, space)
        self.assertEqual(read_val, datasheet, 'FAIL: setDatasheet() new value not set')


# Test addSpace()
class AddSpace(unittest.TestCase):
    # Add a space in a bin
    # Verify it was added
    def testAddSpace(self):
        bin = 4
        space = 2
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: addSpace() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, False, 'FAIL: addSpace() space already exists')
        bins.addSpace(db, bin, space)
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: addSpace() space does not exist')


# Test removeSpace()
class RemoveSpace(unittest.TestCase):
    # Remove a space in a bin
    # Verify it has been removed
    def testRemoveSpace(self):
        bin = 3
        space = 4
        db = bins.loadDatabase('dbs/four_bins_4_2_8_1_spaces_db.json')
        exists = bins.checkIfBinExists(db, bin)
        self.assertEqual(exists, True, 'FAIL: removeSpace() bin does not exist')
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, True, 'FAIL: removeSpace() space does not exist')
        bins.removeSpace(db, bin, space)
        space_exists = bins.checkIfSpaceExists(db, bin, space)
        self.assertEqual(space_exists, False, 'FAIL: removeSpace() space still exists')


if __name__ == '__main__':
    unittest.main()