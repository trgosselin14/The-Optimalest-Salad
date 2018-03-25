import pandas as pd
import random
import itertools
import copy

# Nutritional Facts Data mg per g of items


def nut_val():
    val = random.randrange(1, 10, 1)
    return val


foods = ['Kale', 'Olives', 'Carrots', 'Cheese', 'Onions', ]
labels = ['Name', 'Fat', 'Carbs', 'Protein', 'Fiber', 'Iron', ]

table = [[i, [nut_val() for j in foods]] for i in labels]

table[0][1] = foods

nutr_vals = pd.DataFrame.from_items(table)


"""
class Food:

    def __init__(self, name):
        self.name = name
        self.Fat
        -
        -
        -
"""

# Possible Weight Compositions
# Give weight in lbs iterate over all possible .1 lbs

given_weight = 4 # Min = number of ingredients * .1
num_ingredients = 5
# Therefore the minimum wieght of an ingredient is 0.1 (set value) and the max would be
# given wieght - (number of ingredeitns - 1)*0.1
# the sum of the ingredient must equal the given weight
#
min = 0.1
max = given_weight - (num_ingredients-1)*min

init_dist = [max, min, min, min]

test = [7, 1, 1, 1, 1]


def iterate_seq(init_list, set_min):
    altered_list = init_list
    list_sum = sum(init_list)
    list_len = len(init_list)
    while altered_list[0] > set_min:
        print(altered_list)
        to_distribute = list_sum - altered_list[0] - sum(altered_list[1:list_len])
        print(to_distribute)
        if to_distribute > 0:
            perm_gen = itertools.permutations(range(1, to_distribute+2), list_len - 1)
            poss_perms = [j for j in perm_gen]
            #print(poss_perms)
        altered_list[0] = altered_list[0] - set_min

def iterate_seq2(init_list, set_min):
    altered_list = init_list
    list_sum = sum(init_list)
    list_len = len(init_list)
    non_permuted_lists = []
    while init_list[0] >= set_min:
        to_distribute = list_sum - init_list[0] - sum(init_list[1:list_len])
        # for i in range(1, list_len):
        #     add_to = 1
        #     if to_distribute > 0:
        #         altered_list[add_to] += 1
        #         if add_to >= i:
        #             add_to = 1
        #         else:
        #             add_to += 1
        #     to_distribute = to_distribute - 1
        print(altered_list)
        non_permuted_lists.append(altered_list)
        altered_list[0] = altered_list[0] - set_min
    print(non_permuted_lists)


def generate_init_list(given_weight = 7, number_of_ingredients= 5):
    min = 1
    max = given_weight - (number_of_ingredients- 1) * min
    init_list = [min]*number_of_ingredients
    init_list[0] = max
    return init_list


def determine_dist_amt(init_list_sum, init_list):
    init_list_sum = init_list_sum
    max = init_list[0]
    sum_remaining = sum(init_list[1:])
    dist = init_list_sum - max - sum_remaining
    return dist


def first_index_lists():
    init_list = generate_init_list()
    index_lists = []
    max = init_list[0]
    for i in range(1,max+1):
        new_max = i
        init_list[0] = new_max
        index_lists.append(init_list.copy())
    return index_lists

def distribute(index_lists):
    for list_ in index_lists:
        non_perm_dists = []
        to_dist = list_[0] - 1
        to_dist_holder = to_dist
        new_list = list_.copy()[1:]
        for i in range(0,len(new_list)):
            index_range = list(range(0, i+1))
            while to_dist > 0:
                for j in index_range:
                    new_list[j] +=1
                    to_dist -= 1
                    if to_dist == 0:
                        break
            new_list.insert(0,list_[0] - to_dist_holder)
            non_perm_dists.append(new_list)
            to_dist = to_dist_holder
            new_list = list_.copy()[1:]
        print(set(map(tuple, non_perm_dists)))

"""def distribute(index_lists):
    for list_ in index_lists:
        #to_dist = determine_dist_amt(init_sum ,list_)
        to_dist = list_[0] - 1
        #print(to_dist)
        to_dist_holder = to_dist
        new_list = list_.copy()[1:]
        for i in range(0,len(new_list)):
            index_range = list(range(0, i+1))
            print(index_range)
            for j in index_range:
                while to_dist !=0:
                    new_list[j] +=1
                    print(new_list)
                    to_dist -= 1
                to_dist = to_dist_holder
            new_list = list_.copy()[1:]
"""




distribute([[4,1,1,1,1]])












































