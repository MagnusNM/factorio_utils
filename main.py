# Goal:
# Be able to specify desired output (e.g. 60 iron plates/minute) and automatically calculate required inputs
# This will be used to top-down calculate the amount of inputs required to sustain a certain level of output
# Since we always want to expand the factory, aim to build modules with x output that can then be parallelized with known amounts of input

# We need to encode all craftable items with their recipe, crafting speed and output

import pprint
import json

itemlist = ["iron-ore",
            "iron-plate",
            "iron-stick",
            "automation-science-pack",
            "electronic-circuit",
            "advanced-circuit",
            "processing-unit",
            "engine-unit",
            "electric-engine-unit",
            "flying-robot-frame"]

item = itemlist[6]
prod_volume = 1 # what quantity of "item" should be produced per minute?
#item = "water"

vol_dict = {} # Dictionary containing volumes of each item per minute

# Open json file from api and write to jsonObj
f = open("recipe-lister/item.json")
items = json.load(f)
f.close()

# Open json file from api and write to jsonObj
f = open("recipe-lister/recipe.json")
recipes = json.load(f)
f.close()

# Run through all ingredients
# If ingredient is base material, stop
# If ingredient is intermediate product, get ingredients of intermediate and run through all ingredients

print_flag = False
if print_flag == True:
    # All items have these
    print("Item description: ", json.dumps(items[item]["name"], indent=4))
    print("Recipe category: ", json.dumps(recipes[item]["subgroup"]["name"], indent=4))

    # Raw materials don't have these
    print("Recipe ingredients: ", json.dumps(recipes[item]["ingredients"], indent=4))
    print("Recipe products: ", json.dumps(recipes[item]["products"], indent=4))
    print("Crafting time: ", json.dumps(recipes[item]["energy"], indent=4))
    print("Number of items in recipe: ", len(recipes[item]["ingredients"]))

for i in range(len(recipes[item]["ingredients"])):
    sub_item = recipes[item]["ingredients"][i]["name"]
    sub_item_amount = recipes[item]["ingredients"][i]["amount"]
    sub_item_amount_prod = sub_item_amount / recipes[item]["main_product"]["amount"] * prod_volume
    if sub_item not in vol_dict:
        vol_dict[sub_item] = sub_item_amount_prod
    else:
        vol_dict[sub_item] = vol_dict[sub_item] + sub_item_amount_prod
    sub_item_cat = recipes[item]["subgroup"]["name"]

    print("\nLayer 1" , sub_item, sub_item_cat, sub_item_amount_prod)
    if sub_item_cat != "raw-material"  and sub_item in recipes:
        for j in range(len(recipes[sub_item]["ingredients"])):
            sub2_item = recipes[sub_item]["ingredients"][j]["name"]
            sub2_item_amount = recipes[sub_item]["ingredients"][j]["amount"] * sub_item_amount
            sub2_item_amount_prod = sub2_item_amount / recipes[sub_item]["main_product"]["amount"] * prod_volume
            if sub2_item not in vol_dict:
                vol_dict[sub2_item] = sub2_item_amount_prod
            else:
                vol_dict[sub2_item] = vol_dict[sub2_item] + sub2_item_amount_prod
            sub2_item_cat = recipes[sub_item]["subgroup"]["name"]

            print("-Layer 2 ", sub2_item, sub2_item_cat, sub2_item_amount_prod)
            if sub2_item_cat != "raw-material" and sub2_item in recipes:
                for k in range(len(recipes[sub2_item]["ingredients"])):
                    sub3_item = recipes[sub2_item]["ingredients"][k]["name"]
                    sub3_item_amount = recipes[sub2_item]["ingredients"][k]["amount"] * sub2_item_amount
                    sub3_item_amount_prod = sub3_item_amount / recipes[sub2_item]["main_product"]["amount"] * prod_volume
                    if sub3_item not in vol_dict:
                        vol_dict[sub3_item] = sub3_item_amount_prod
                    else:
                        vol_dict[sub3_item] = vol_dict[sub3_item] + sub3_item_amount_prod
                    sub3_item_cat = recipes[sub2_item]["subgroup"]["name"]

                    print("--Layer 3 ", sub3_item, sub3_item_cat, sub3_item_amount_prod)
                    if sub3_item_cat != "raw-material"  and sub3_item in recipes:
                        for l in range(len(recipes[sub3_item]["ingredients"])):
                            sub4_item = recipes[sub3_item]["ingredients"][l]["name"]
                            sub4_item_amount = recipes[sub3_item]["ingredients"][l]["amount"] * sub3_item_amount
                            sub4_item_amount_prod = sub4_item_amount / recipes[sub3_item]["main_product"]["amount"] * prod_volume
                            if sub4_item not in vol_dict:
                                vol_dict[sub4_item] = sub4_item_amount_prod
                            else:
                                vol_dict[sub4_item] = vol_dict[sub4_item] + sub4_item_amount_prod
                            sub4_item_cat = recipes[sub3_item]["subgroup"]["name"]

                            print("---Layer 4 ", sub4_item, sub4_item_cat, sub4_item_amount_prod)
                            if sub4_item_cat != "raw-material" and sub4_item in recipes:
                                for u in range(len(recipes[sub4_item]["ingredients"])):
                                    sub5_item = recipes[sub4_item]["ingredients"][u]["name"]
                                    sub5_item_amount = recipes[sub4_item]["ingredients"][u]["amount"] * sub4_item_amount
                                    sub5_item_amount_prod = sub5_item_amount / recipes[sub4_item]["main_product"]["amount"] * prod_volume
                                    if sub5_item not in vol_dict:
                                        vol_dict[sub5_item] = sub5_item_amount_prod
                                    else:
                                        vol_dict[sub5_item] = vol_dict[sub5_item] + sub5_item_amount_prod
                                    sub5_item_cat = recipes[sub4_item]["subgroup"]["name"]

                                    print("----Layer 5 ", sub5_item, sub5_item_cat, sub5_item_amount_prod)

print(json.dumps(vol_dict, indent=4, sort_keys=True))