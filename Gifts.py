'''
Created on Sep 27, 2014

@author: Sarang Hattikar
'''

import urllib2
import json
import operator
import sys
# # Class gift contains variables to save information obtained  
# # from user and methods to access those varibles and to manipulate them 
class Gift:
# # init method initialize the class variables to there default value
# # user_budget is amount entered by the user which is initialized to 0.0
# # gift_number is number of gifts user wants to purchase
# # gift_category is type of gift user wants to purchase such as boots or 
# # which is initialized to 'boots'    
    def __init__(self):
        self.user_budget = 0.00
        self.gift_number = 0
        self.gift_category = 'boots'
        
    
# # get_user_budget method gets user budget and returns it    
    def get_user_budget(self):
        try:
            self.user_budget = float(input("Enter amount in USD:"))
            return self.user_budget
        except ValueError:
            print("Entered amount is not incorrect")
            print("Please start again")
            sys.exit(0)
            pass
# # get_gift_number method gets total number of gifts user wants to purchase and returns it    
    def get_gift_number(self):
        try:
            self.gift_number = int(input("Enter Number of gifts you want to purchase:"))
            return self.gift_number
        except ValueError:
            print("Entered number is not incorrect")
            print("Please start again")
            sys.exit(0)
            pass

# # get_gift_number method gets total category of gifts purchase and returns it    
    def get_gift_category(self):
        try:
            self.gift_category = str(raw_input("Enter Category of gifts you want to purchase:"))
            return self.gift_category
        except ValueError:
            print("Entered category is not incorrect")
            print("Please start again")
            sys.exit(0)
            pass

# # get_items_from_api method gets item form zappos api based on category entered by the user
# # and also parse the json formatted data into python dictionary format
# # finally selects all possible valid combinations. 
    def get_items_from_api(self):
        access_url = 'http://api.zappos.com/Search?term=' + str(self.gift_category) + '&key=52ddafbe3ee659bad97fcce7c53592916a6bfd73'
        try:
            response = urllib2.urlopen(access_url)
            if response.code == 200:
                data = response.read()
            else:
                print("Sorry for error please try again")
                sys.exit(0)
        except urllib2.URLError as e:
            print("******************" + e.reason)
    
        items = json.loads(data, parse_float='.2f', parse_int=True)
        item_List = items['results']
        current_count = int(items['currentResultCount'])
        if (current_count == 0):
            print("Invalid Search term")
            print("Enter the correct Search term and start again")
            sys.exit(0)
        products = {}
        index = 0
        for each in item_List:
            product_info = []
            product_info.append(str(each['productId']))
            product_info.append(float(str(each['price']).lstrip('$')))
            products[index] = product_info
            index = index + 1
        elements = []
        for i in range(1, current_count):
            elements.append(i)
        Gift.choose(self, elements, products, items)

# #this is a helper function for choose that  
# # arguments elements which is a list of elements to generate combinations.
# # length is total number of items to be taken at a time for generating combinations
# # for current problem length is nothing but total number of items user wants to purchase 
# # and elements is list of total number of elements returned by the api  
    def choose_iter(self, elements, length):
        for i in xrange(len(elements)):
            if length == 1:
                yield (elements[i],)
            else:
                for next in Gift.choose_iter(self, elements[i + 1:len(elements)], length - 1):
                    yield (elements[i],) + next
                                    
# #this is the function where actual logic resides.  
# # arguments 'elements' which is a list of elements to generate combinations.
# # 'products' is dictionary having key as a index and values as a list having 
# # product id and price.
# # for the sake making combinations efficiently each product and its prize 
# # is mapped against a key in dictionary. 
# # 'items' contains data obtained after parsing obtained json object. 
# # This function obtains a possivle combination of products from 'choose_iter'
# # and validate it based on the total prize of the items in that combination.
  
    def choose(self, elements, products, items):
        valid_combinations = {}
        length = self.gift_number
        for x in Gift.choose_iter(self, elements, length):
            total_amt = 0
            for each in x:
                total_amt = total_amt + products[each][1]
            if (total_amt <= self.user_budget):
                valid_combinations[x] = total_amt
        if(bool(valid_combinations) == False):
            print("No combination of items can be purchased within entered amount")
            sys.exit(0)
        sorted_valid_combinations = sorted(valid_combinations.items(), key=operator.itemgetter(1), reverse=True)
        Gift.display_items(self, products, sorted_valid_combinations, items)

# #display_items takes argument as list of valid combinations and there mapping against 
# #key in 'product' dictionary and complete json parsed data 
# #Finally displays product information of each product in valid combination 
# #and total price of combination.
    
    def display_items(self, products, sorted_valid_combinations, items):
        if(bool(sorted_valid_combinations) == False):
            print("No valid products for the entered amount")
            sys.exit(0)
        else:
            for each1 in sorted_valid_combinations:
                comb = []
                comb = each1[0]
                for prod_index in comb:
                    product_id = products[prod_index][0]
                    for each in items['results']:
                        
                        if each['productId'] == str(product_id):
                            
                            print(each['productId'])
                            print(each['price'])
                            print(each['productName'])
                            print(each['brandName'])
                            print(each['styleId'])
                            
                    print("_______________________________________________________")
                    
                print("Total price of the combination:" + str(each1[1]))
                print("***********************************************************************")         
            
            
        
        
        
            
        
    
        
# #Main method contains while(1) loop which 
# #creates an objects of class gift and
# #gives call to different methods in that class        
while(1):    
    g = Gift()
    g.get_user_budget()
    g.get_gift_number()
    g.get_gift_category()
    g.get_items_from_api()
    choice = str(raw_input("Enter Y to Continue else Enter 'N':"))
    if (choice == 'Y'):
        continue
    else:
        print("Thank you for using application")
        sys.exit(0)
   
   
    

    










if __name__ == '__main__':
    pass
