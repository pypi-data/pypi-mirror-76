import elementally as elmy
import unittest
import itertools

pos_array = [1, 2, 3, 4, 5]
pos_array_2 = [5, 4, 3, 2, 1]
neg_array = [-10, -20, -30, -40, -50]
neg_array_2 = [-50, -40, -30, -20, -10]
def odd_generator():
    i=1
    while(True):
        yield i
        i+=2

def complex_generator():
    i=1
    while(True):
        yield i
        i+=2j

class TestBasicArithmetic(unittest.TestCase):
    def test_sum_lists(self):
        """Checks whether two lists sum properly"""
        self.assertListEqual(elmy.sum(pos_array, pos_array_2), [6, 6, 6, 6, 6])
        self.assertListEqual(elmy.sum(pos_array, neg_array), [-9, -18, -27, -36, -45])
    
    def test_sum_list_with_generator(self):
        """Checks whether a list sums with a generator properly, and returns a generator"""
        list_odd_numbers_plus_index = elmy.sum(pos_array, odd_generator())
        self.assertListEqual(list_odd_numbers_plus_index, [2, 5, 8, 11, 14])
    
    def test_sum_generator_with_list(self):
        """Checks whether a generator sums with a list properly, and remains a generator"""
        augend = odd_generator()
        gen_odd_numbers_plus_index = elmy.sum(augend, pos_array)
        self.assertEqual(type(augend), type(gen_odd_numbers_plus_index))
        slice_of_summed_generator = itertools.islice(gen_odd_numbers_plus_index, 8)
        self.assertSequenceEqual(list(slice_of_summed_generator), [2, 5, 8, 11, 14])

    def test_sum_generator_with_generator(self):
        """Checks whether a generator sums with a generator properly, and returns a generator"""
        augend = odd_generator()
        summed = elmy.sum(augend, odd_generator())
        self.assertSequenceEqual([2, 6, 10, 14], list(itertools.islice(summed, 4)))
        self.assertEqual(type(augend), type(summed))


class TestMultistepOps(unittest.TestCase):
    def test_negation_generator(self):
        """Checks whether adding a sequences to its negation yields 0s"""
        operand = odd_generator()
        negated = elmy.negation(odd_generator())
        zeros = elmy.sum(operand, negated)
        for i in itertools.islice(zeros, 1000):
            self.assertEqual(i, 0)
    def test_reciprocal_multiplication(self):
        """Checks whether multiplying a sequence by its reciprocal yields 1s"""
        augend = complex_generator()
        reciprocal = elmy.product(augend, elmy.reciprocal(complex_generator()))
        for i in itertools.islice(reciprocal, 1000):
            self.assertAlmostEqual(i, 1, 14)

if __name__ == '__main__':
    unittest.main()
