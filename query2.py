# # Table_Name = eatsafe_master_database_csv
# ''' desc :-
# (0, 'ingredient', 'TEXT', 0, None, 0)
# (1, 'nova_group', 'INTEGER', 0, None, 0)
# (2, 'additive_risk', 'TEXT', 0, None, 0)
# (3, 'artificial_flag', 'INTEGER', 0, None, 0)
# (4, 'gemini_rating', 'REAL', 0, None, 0)
# (5, 'reason', 'TEXT', 0, None, 0)
# (6, 'processing_penalty', 'REAL', 0, None, 0)
# (7, 'nutrition_impact', 'REAL', 0, None, 0)
# (8, 'whole_food_bonus', 'REAL', 0, None, 0)'''

# def search(ingredient_list):
#     import sqlite3
#     conn = sqlite3.connect("eatsafe_database.db")
#     cursor = conn.cursor()
    
#     try : 
#         #count = 0 
#         for item in ingredient_list:
#             # Using LIKE '%...%' for partial matches, or remove % for exact matches
#             cursor.execute(
#                 """SELECT *FROM eatsafe_master_database_csv WHERE LOWER(ingredient) LIKE LOWER(?);""",
#                 (f"{item.strip()}",)
#             )
            
#             #count += 1
#             tables = cursor.fetchall()
#             for row in tables:  # Fixed: changed 'i' to 'row' to avoid shadowing
#                 return row
                
#         # print(count)
#     except Exception as e:
#         return f"An error occurred during the search: {e}"

#     finally:
#         conn.close()
#         #return tables

# text = ["Live Cultures"]
# print(search(text))


# Table_Name = eatsafe_master_database_csv
''' desc :-
(0, 'ingredient', 'TEXT', 0, None, 0)
(1, 'nova_group', 'INTEGER', 0, None, 0)
(2, 'additive_risk', 'TEXT', 0, None, 0)
(3, 'artificial_flag', 'INTEGER', 0, None, 0)
(4, 'gemini_rating', 'REAL', 0, None, 0)
(5, 'reason', 'TEXT', 0, None, 0)
(6, 'processing_penalty', 'REAL', 0, None, 0)
(7, 'nutrition_impact', 'REAL', 0, None, 0)
(8, 'whole_food_bonus', 'REAL', 0, None, 0)'''

import sqlite3

def search(nested_list):
    conn = sqlite3.connect("eatsafe_database.db")
    cursor = conn.cursor()
    
    all_results = []
    
    try:
        for group in nested_list:
            if isinstance(group, list) and len(group) > 0 and isinstance(group[0], list):
                matched = False
                for sub_item_list in reversed(group[1:]):
                    item_name = sub_item_list[0].strip()
                    cursor.execute(
                        """SELECT * FROM eatsafe_master_database_csv WHERE LOWER(ingredient) LIKE LOWER(?);""",
                        (f"{item_name}",)
                    )
                    rows = cursor.fetchall()
                    if rows:
                        all_results.extend(rows)
                        matched = True
                        break 
                
                if not matched and len(group) > 0:
                    item_name = group[0][0].strip()
                    cursor.execute(
                        """SELECT * FROM eatsafe_master_database_csv WHERE LOWER(ingredient) LIKE LOWER(?);""",
                        (f"{item_name}",)
                    )
                    rows = cursor.fetchall()
                    if rows:
                        all_results.extend(rows)
            else:
                if isinstance(group, list):
                    item_name = group[0].strip()
                else:
                    item_name = str(group).strip()
                    
                cursor.execute(
                    """SELECT * FROM eatsafe_master_database_csv WHERE LOWER(ingredient) LIKE LOWER(?);""",
                    (f"{item_name}",)
                )
                rows = cursor.fetchall()
                if rows:
                    all_results.extend(rows)
                    
        return all_results
        
    except Exception as e:
        return f"An error occurred during the search: {e}"

    finally:
        conn.close()

# Example usage:
# extracted_data = [['sugar'], ['water'], [['Thickeners'], ['Thickeners 1422'], ['Thickeners 1442']]]
# print(search_nested_ingredients(extracted_data))

# text = ["Live Cultures"]
# print(search(text))

