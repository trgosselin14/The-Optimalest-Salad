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
        calc_min = self.minimum_ingredient_weight*10
        to_dist = self.initial_test_distribution[0] - (self.minimum_ingredient_weight*10)
        to_dist_holder = to_dist
        #print(to_dist_holder)
        new_list = self.initial_test_distribution.copy()[1:]
        #print(new_list)
        for i in range(0, len(new_list)):
            index_range = list(range(0, i + 1))
            #print(index_range)
            while to_dist > 0:
                for j in index_range:
                    print(j)
                    new_list[j] += self.minimum_ingredient_weight
                    print(new_list)
                    to_dist -= self.minimum_ingredient_weight
                    if to_dist == 0:
                        break
                    new_list.insert(0, self.initial_test_distribution[0] - to_dist_holder)
            print(new_list)
            non_perm_dists.append(new_list)
            to_dist = to_dist_holder
            new_list = self.initial_test_distribution.copy()[1:]
        unique_sets = list(set(map(tuple, non_perm_dists)))
        all_permutations = []
        for unique in unique_sets:
            perms = set(itertools.permutations(unique))
            for perm in perms:
                all_permutations.append(perm)
        df = pd.DataFrame.from_records(all_permutations, columns=self.foods)
        return df


if __name__ =="__main__":
    x = Combinations()
    y = x.distribute()
    print(set(y['Kale, raw']))