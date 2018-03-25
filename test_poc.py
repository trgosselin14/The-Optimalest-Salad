import unittest
import poc


class TestPoc(unittest.TestCase):

    def test_generate_init_list(self):
        self.assertEqual(poc.generate_init_list(7, 5), [3, 1, 1, 1, 1, ])

    def test_determine_dist_amt(self):
        self.assertEqual(poc.determine_dist_amt(7, [2, 1, 1, 1, 1]), 1)

    def test_first_index_lists(self):
        self.assertEqual(poc.first_index_lists(), [[1, 1, 1, 1, 1, ],[2,1,1,1,1],[3,1,1,1,1]])

    def test_distribute(self):
        pass
        #self.assetEqual(poc.distribute([[2,1,1,1,1]]), [[2,1,1,1,1],[1,2,1,1,1],[1,1,2,1,1],[1,1,1,2,1],[1,1,1,1,2]])

if __name__ == '__main__':
    unittest.main()
