import pandas as pd
import os
from fuzzywuzzy import fuzz

def searchdb():
    fooddb = pd.read_csv(os.path.dirname(__file__) + "/Data/fooddb.csv")
    entered_term = input('Enter a search term to select an item. When you are finished enter "Done": ')
    if (entered_term == 'Done')|(entered_term == 'done'):
        print('done')
    else:
        fooddb['Match Score'] = [fuzz.ratio(entered_term,i) for i in fooddb['Name']]
        sorted_fooddb = fooddb.copy()
        sorted_fooddb.sort_values(by=['Match Score'], ascending=False, inplace=True)
        sorted_fooddb.reset_index(inplace=True)
        print(sorted_fooddb['Name'].head())
        selection = input("Select the food item by typing the index number (enter 'X' to quit): ")
        if (selection == 'X') | (selection == 'x'):
            print('done')
        else:
            selection = int(selection)
            return sorted_fooddb.iloc[selection,:]

"""
class UI(object):




"""
if __name__ == "__main__":
   x = searchdb()
   print(x)