# import re
# from PIL import Image
# import pytesseract

# def extract_ingredients2(image_path):
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
#     # 1. Open image and run Pytesseract OCR
#     img = Image.open(image_path)
#     extracted_text = pytesseract.image_to_string(img, config='--psm 6')

#     # 2. Basic prefix/suffix cleanup
#     if ":" in extracted_text:
#         extracted_text = extracted_text.split(":", 1)[1].strip()
#     else:
#         extracted_text = extracted_text.strip()
        
#     extracted_text = extracted_text.replace("-\n", "")
#     extracted_text = extracted_text.replace("\n", " ")
    
#     extracted_text = re.sub(r'^\s*INGREDIENTS:\s*', '', extracted_text, flags=re.IGNORECASE)
#     extracted_text = re.sub(r'BHT ADDED.*', '', extracted_text, flags=re.IGNORECASE)
#     extracted_text = re.sub(r'CONTAINS:.*', '', extracted_text, flags=re.IGNORECASE)

#     # 3. Normalize periods into commas
#     extracted_text = extracted_text.replace('.', ',')

#     # 4. Parenthesis-aware splitting 
#     items = []
#     current = []
#     depth = 0
    
#     for char in extracted_text:
#         if char == '(':
#             depth += 1
#             current.append(char)
#         elif char == ')':
#             depth = max(0, depth - 1)
#             current.append(char)
#         elif char == ',' and depth == 0:
#             item = "".join(current).strip()
#             if item:
#                 items.append(item)
#             current = []
#         else:
#             current.append(char)
            
#     last_item = "".join(current).strip()
#     if last_item:
#         items.append(last_item)
        
#     # 5. Build clean sub-lists for both coded groups and parenthetical items
#     list_of_lists = []
    
#     for item in items:
#         cleaned_item = item.strip()
#         if not cleaned_item:
#             continue
            
#         codes = re.findall(r'\b\d{3,4}\b', cleaned_item)
        
#         if codes:
#             # CASE 1: Contains numeric codes (e.g., Thickeners, Acidity Regulators)
#             category = cleaned_item.split('(', 1)[0].strip()
#             if category:
#                 list_of_lists.append([category])
#             for code in codes:
#                 combined_name = f"{category} {code}"
#                 list_of_lists.append([combined_name])
#             list_of_lists.append([cleaned_item])
            
#         elif '(' in cleaned_item:
#             # CASE 2: Contains text inside parentheses (e.g., Cream (From Milk), Enzyme (Lactase))
#             base_name = cleaned_item.split('(', 1)[0].strip()
#             if base_name:
#                 list_of_lists.append([base_name])
#             list_of_lists.append([cleaned_item])
            
#         else:
#             # CASE 3: Regular base ingredients with no parentheses (e.g., Sugar, Water)
#             list_of_lists.append([cleaned_item])
            
#     return list_of_lists
#     #return list_of_lists

from query2 import search
import re
from PIL import Image
import pytesseract

def extract_ingredients2(image_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # 1. Open image and run Pytesseract OCR
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img, config='--psm 6')

    # 2. Basic prefix/suffix cleanup
    if ":" in extracted_text:
        extracted_text = extracted_text.split(":", 1)[1].strip()
    else:
        extracted_text = extracted_text.strip()
        
    extracted_text = extracted_text.replace("-\n", "")
    extracted_text = extracted_text.replace("\n", " ")
    
    extracted_text = re.sub(r'^\s*INGREDIENTS:\s*', '', extracted_text, flags=re.IGNORECASE)
    extracted_text = re.sub(r'BHT ADDED.*', '', extracted_text, flags=re.IGNORECASE)
    extracted_text = re.sub(r'CONTAINS:.*', '', extracted_text, flags=re.IGNORECASE)

    # 3. Normalize periods into commas
    extracted_text = extracted_text.replace('.', ',')

    # 4. Parenthesis-aware splitting 
    items = []
    current = []
    depth = 0
    
    for char in extracted_text:
        if char == '(':
            depth += 1
            current.append(char)
        elif char == ')':
            depth = max(0, depth - 1)
            current.append(char)
        elif char == ',' and depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
        else:
            current.append(char)
            
    last_item = "".join(current).strip()
    if last_item:
        items.append(last_item)
        
    # 5. Build nested lists for coded groups and parenthetical items
    list_of_lists = []
    
    for item in items:
        cleaned_item = item.strip()
        if not cleaned_item:
            continue
            
        codes = re.findall(r'\b\d{3,4}\b', cleaned_item)
        
        if codes:
            # CASE 1: Contains numeric codes -> Group category and individual codes
            category = cleaned_item.split('(', 1)[0].strip()
            group = []
            if category:
                group.append([category])
            for code in codes:
                combined_name = f"{category} {code}"
                group.append([combined_name])
            # NOTE: Raw cleaned_item is omitted here as requested
            
            # Append the group as a nested list
            list_of_lists.append(group)
            
        elif '(' in cleaned_item:
            # CASE 2: Contains text inside parentheses (kept as is)
            base_name = cleaned_item.split('(', 1)[0].strip()
            group = []
            if base_name:
                group.append([base_name])
            group.append([cleaned_item])
            
            # Append the group as a nested list
            list_of_lists.append(group)
            
        else:
            # CASE 3: Regular base ingredients with no parentheses
            list_of_lists.append([cleaned_item])
            
    return list_of_lists

text=extract_ingredients2("cropped_img.jpg")
print(text)
print(search (text))