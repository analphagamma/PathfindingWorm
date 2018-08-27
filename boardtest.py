import unittest
import pathfinder as pf

class BoardTest(unittest.TestCase):

    test_obj = pf.Board(10,10)
    # Fail cases
    def test_query_validation_nottuple(self):
        self.assertEqual(self.test_obj.query_cell([0,0]), None)        
                
    def test_query_validation_notint(self):
        self.assertEqual(self.test_obj.query_cell(('0', '1')), None)
        
    def test_query_validation_outofrange(self):
        self.assertEqual(self.test_obj.query_cell((10, 0)), None)

    # Pass cases
    def test_query_origin(self):
        self.assertEqual(self.test_obj.query_cell((0, 0)), [(0, 1), (1, 0)])

    def test_query_zeroonx(self):
        self.assertEqual(self.test_obj.query_cell((0, 5)), [(0, 4), (0, 6), (1, 5)])

    def test_query_zeroony(self):
        self.assertEqual(self.test_obj.query_cell((5, 0)), [(4, 0), (5, 1), (6, 0)])

    def test_query_maxonx(self):
        self.assertEqual(self.test_obj.query_cell((9, 5)), [(8, 5), (9, 4), (9, 6)])

    def test_query_maxony(self):
        self.assertEqual(self.test_obj.query_cell((5, 9)), [(4, 9), (5, 8), (6, 9)])

    def test_query_topcorner(self):
        self.assertEqual(self.test_obj.query_cell((9, 9)), [(8, 9), (9, 8)])

    def test_query_general(self):
        self.assertEqual(self.test_obj.query_cell((5, 5)), [(4, 5), (5, 4), (5, 6), (6, 5)])

    
if __name__ == '__main__':
    unittest.main()
