import pandas as pd
from image_encoder_base64 import encode_image

def main():
  #Populate test table DATAFRAME with image base64

  df = pd.read_csv('../test_table_files/00-initial_test_table.csv')

  #Convert base64_image data type to string, if not already
  df['base64_image'] = df['base64_image'].astype(str)

  for index, row in df.iterrows():
    image_path = f"../images/{row['Test ID']}.{row['image_file_type']}"
    base64_image = encode_image(image_path)

    df.at[index, 'base64_image'] = base64_image

  df.to_csv('../test_table_files/01-base64_test_table.csv')
