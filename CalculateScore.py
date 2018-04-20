import os
import pandas as pd
import itertools
import numpy as np
from CalculateCombinations import Combinations

class CalculateScore:

    def __init__(self, list_of_ingredients):
        self.ingredient_list = list_of_ingredients
        self.fooddb = pd.read_csv(os.path.dirname(__file__) + "/Data/fooddb.csv")
        self.nutrients = list(self.fooddb.columns)[1:]
        self.poss_dist_obj = Combinations()
        self.poss_dist = self.poss_dist_obj.distribute()


    def calculate_nutritional_dot_product(self):
        possible_distribution_matrix = self.poss_dist.values
        inv_sd_of_dists = [((len(self.ingredient_list)*2/self.poss_dist_obj.weight)-np.std(poss)) for poss in possible_distribution_matrix]
        nutrient_matrix = self.fooddb.iloc[:,1:].values
        dot_product = np.dot(possible_distribution_matrix,nutrient_matrix)
        #self.nut_score = (('Carbohydrates', 1), ('Cholesterol', -0.3), ('Fat', -65), ('Sodium', -2.4), ('Fiber', 1))
        scoring_list = [1/i for i in [1, -0.3, -65, -2.4, 1,]]

        self.dist_nutrients = pd.DataFrame(dot_product, columns=self.nutrients)
        self.dist_nutrients['Score'] = self.dist_nutrients.dot(scoring_list)
        self.dist_nutrients['Score'] = self.dist_nutrients['Score'] * inv_sd_of_dists
        self.dist_nutrients.sort_values('Score', ascending=False, inplace=True)
        best_distributions = list(self.dist_nutrients[self.dist_nutrients['Score'] == max(self.dist_nutrients['Score'])].index)
        #print(self.dist_nutrients)
        print(self.poss_dist.iloc[best_distributions,:])


# https://www.ncbi.nlm.nih.gov/books/NBK56068/
if __name__ == "__main__":
    x = CalculateScore(['Kale, raw',
                        'Onions, raw',
                        'Carrots, raw',
                        'Cheese, cheddar, nonfat or fat free',
                        'Olives, pickled, canned or bottled, green'])
    x.calculate_nutritional_dot_product()
    #print(x.dist_nutrients)