import os
import json
from PIL import Image
import streamlit as st
from streamlit_cropper import st_cropper
from query2 import search
from search2 import extract_ingredients2

# 1. Page Configuration
st.set_page_config(
    page_title="Eatsafe - Smart Ingredient Scanner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for a cleaner look
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.title("🥗 Eatsafe: Smart Ingredient & Allergen Scanner")
st.markdown(
    "Scan or upload product ingredient labels to instantly check for safety,"
    " allergens, and health insights."
)
st.divider()

# Sidebar configuration for input options
st.sidebar.header("⚙️ Settings")
input_method = st.sidebar.radio(
    "Choose input method:", ("Camera 📸", "Upload Image 📁")
)

# Main 2-Column Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
  st.subheader("📸 Step 1: Capture or Upload Label")

  image = None
  if "Camera" in input_method:
    picture = st.camera_input("Take a clear photo of the ingredients list")
    if picture is not None:
      image = Image.open(picture)
  else:
    uploaded_file = st.file_uploader(
        "Upload a label image", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
      image = Image.open(uploaded_file)

  if image is not None:
    st.markdown("### ✂️ Crop Ingredient Area")
    st.write("Drag and resize the box to focus strictly on the ingredients:")

    # Interactive cropping component
    cropped_img = st_cropper(
        image, realtime_update=True, box_color="#00FF00", aspect_ratio=None
    )

    st.markdown("### 👁️ Cropped Preview")
    st.image(cropped_img, use_container_width=True)
    cropped_img.save("cropped_img.jpg")

with col2:
  st.subheader("🔍 Step 2: Analysis & Health Insights")

  if os.path.exists("cropped_img.jpg"):
    # Action button to trigger processing
    if st.button("🚀 Analyze Ingredients", type="primary"):
      with st.spinner("Extracting text from image..."):
        try:
          text = extract_ingredients2("cropped_img.jpg")
        except Exception as e:
          st.error(f"Error during extraction: {e}")
          text = []

      if text:
        with st.container(border=True):
          st.markdown("#### 📝 Detected Ingredients Structure")
          # Single-line compact JSON representation
          formatted_text_structure = json.dumps(text)
          st.code(formatted_text_structure, language="json")

        st.markdown("#### 🛡️ Ingredient Safety Breakdown")
        with st.spinner("Querying health database..."):
          for group in text:
            # Determine display name for the expander title
            if isinstance(group, list) and len(group) > 0 and isinstance(group[0], list):
              display_name = group[0][0]
            elif isinstance(group, list):
              display_name = group[0]
            else:
              display_name = str(group)

            with st.expander(f"Analysis for: **{display_name}**", expanded=False):
              try:
                result = search([group])
                if result:
                  formatted_result = json.dumps(result, indent=4)
                  st.code(formatted_result, language="json")
                else:
                  st.info("No matching records found in the database.")
              except Exception as e:
                st.error(f"Could not retrieve info: {e}")
  else:
    st.info(
        "👈 Please take or upload a photo of the ingredient label on the left"
        " to begin the analysis."
    )

# Cleanup temporary file when appropriate
if not os.path.exists("cropped_img.jpg"):
  try:
    os.remove("cropped_img.jpg")
  except:
    pass


      # import os
# from PIL import Image
# import streamlit as st
# from streamlit_cropper import st_cropper
# #from image_scan import extract_ingredients
# #from query_try import search
# from query2 import search
# from search2 import extract_ingredients2
# #from search_try import extract_ingredients2

# # 1. Page Configuration
# st.set_page_config(
#     page_title="Eatsafe - Smart Ingredient Scanner",
#     page_icon="🥗",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # Custom CSS styling for a cleaner look
# st.markdown(
#     """
#     <style>
#     .main {
#         background-color: #f8f9fa;
#     }
#     .stButton>button {
#         width: 100%;
#         border-radius: 8px;
#         font-weight: bold;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # App Header
# st.title("🥗 Eatsafe: Smart Ingredient & Allergen Scanner")
# st.markdown(
#     "Scan or upload product ingredient labels to instantly check for safety,"
#     " allergens, and health insights."
# )
# st.divider()

# # Sidebar configuration for input options
# st.sidebar.header("⚙️ Settings")
# input_method = st.sidebar.radio(
#     "Choose input method:", ("Camera 📸", "Upload Image 📁")
# )

# # Main 2-Column Layout
# col1, col2 = st.columns([1, 1], gap="large")

# with col1:
#   st.subheader("📸 Step 1: Capture or Upload Label")

#   image = None
#   if "Camera" in input_method:
#     picture = st.camera_input("Take a clear photo of the ingredients list")
#     if picture is not None:
#       image = Image.open(picture)
#   else:
#     uploaded_file = st.file_uploader(
#         "Upload a label image", type=["jpg", "jpeg", "png"]
#     )
#     if uploaded_file is not None:
#       image = Image.open(uploaded_file)

#   if image is not None:
#     st.markdown("### ✂️ Crop Ingredient Area")
#     st.write("Drag and resize the box to focus strictly on the ingredients:")

#     # Interactive cropping component
#     cropped_img = st_cropper(
#         image, realtime_update=True, box_color="#00FF00", aspect_ratio=None
#     )

#     st.markdown("### 👁️ Cropped Preview")
#     st.image(cropped_img, use_container_width=True)
#     cropped_img.save("cropped_img.jpg")

# with col2:
#   st.subheader("🔍 Step 2: Analysis & Health Insights")

#   if os.path.exists("cropped_img.jpg"):
#     # Action button to trigger processing
#     if st.button("🚀 Analyze Ingredients", type="primary"):
#       with st.spinner("Extracting text from image..."):
#         try:
#           text = extract_ingredients2("cropped_img.jpg")
#         except Exception as e:
#           st.error(f"Error during extraction: {e}")
#           text = []

#       if text:
#         with st.container(border=True):
#           st.markdown("#### 📝 Detected Ingredients")
#           st.write(text)

#         st.markdown("#### 🛡️ Ingredient Safety Breakdown")
#         with st.spinner("Querying health database..."):
#           for i in text:
#             # Use expanders for clean, organized layout per ingredient
#             with st.expander(f"Analysis for: **{i}**", expanded=False):
#               try:
#                 result = search(i)
#                 st.write(result)

#               except Exception as e:
#                 st.error(f"Could not retrieve info for {i}: {e}")
#   else:
#     st.info(
#         "👈 Please take or upload a photo of the ingredient label on the left"
#         " to begin the analysis."
#     )

# # Cleanup temporary file when appropriate
# if not os.path.exists("cropped_img.jpg") and os.path.exists("cropped_img.jpg"):
#   try:
#     os.remove("cropped_img.jpg")
#   except:
#     pass

