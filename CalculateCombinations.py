import os
import pandas as pd
import itertools
import numpy as np


class Combinations:

    def __init__(self,desired_weight = 5):
        self.fooddb = pd.read_csv(os.path.dirname(__file__) + "/Data/fooddb.csv")
        self.foods = list(self.fooddb["Name"])
        self.nutrients = list(self.fooddb.columns)[1:]
        self.weight = desired_weight
        self.number_of_ingredients = len(self.foods)
        self.minimum_ingredient_weight = 0.1
        self.maximum_ingredient_weight = self.weight -(self.number_of_ingredients-1)*self.minimum_ingredient_weight
        self.initial_test_distribution = [self.minimum_ingredient_weight for i in self.foods]
        self.initial_test_distribution[0] = self.maximum_ingredient_weight

    def distribute(self):
        non_perm_dists = []
        to_dist = self.initial_test_distribution[0] - self.minimum_ingredient_weight
        to_dist_holder = to_dist
        #print(to_dist_holder)
        new_list = self.initial_test_distribution.copy()[1:]
        #print(new_list)
        for i in range(0, len(new_list)):
            index_range = list(range(0, i + 1))
            #print(index_range) #1 then 1 and 2 then 1 and 2 and 3 ...
            while to_dist > 0:
                for j in index_range:

                    new_list[j] += self.minimum_ingredient_weight

                    to_dist -= self.minimum_ingredient_weight
                    if to_dist == 0:
                        break
                    #print(new_list)
                    print_values = []
                    for f in new_list:
                        string_truncated = format(f,'.1f')
                        float_value = float(string_truncated)
                        print_values.append(float_value)
                    non_perm_dists.append(print_values)
            to_dist = to_dist_holder
            new_list = self.initial_test_distribution.copy()[1:]
        clean_list = []
        for sub_list in non_perm_dists:
            sub_list_sum = sum(sub_list)
            diff = self.weight - sub_list_sum
            string_truncated = format(diff, '.1f')
            float_value = float(string_truncated)
            sub_list.insert(0,float_value)
            if float_value > 0:
                clean_list.append(sub_list)
        clean_list.append(self.initial_test_distribution)
        #unique_sets = list(set(map(tuple, clean_list)))
        #print(unique_sets)
        all_permutations = []
        for unique in clean_list:
            perms = set(itertools.permutations(unique))
            for perm in perms:
                all_permutations.append(perm)
        unique_sets = list(set(map(tuple, all_permutations)))
        df = pd.DataFrame.from_records(unique_sets, columns=self.foods)
        return df


if __name__ =="__main__":
    x = Combinations()
    y = x.distribute()
    print(x.foods)