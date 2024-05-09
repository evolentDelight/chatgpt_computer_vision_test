from openai import OpenAI
import pandas as pd
from dotenv import dotenv_values

def main():
#Get API Key
  config = dotenv_values(".env") #Accessible by {config[`name`]}
  CHATGPT_API_KEY = config['CHATGPT_API_KEY']

  client = OpenAI(
    api_key=CHATGPT_API_KEY,
  )

  df = pd.read_csv('../test_table_files/01-base64_test_table.csv')

  #Convert column data type to string, if not already
  df['Actual Output: Classification'] = df['Actual Output: Classification'].astype(str)
  df['Actual Extracted Text'] = df['Actual Extracted Text'].astype(str)

  for index, row in df.iterrows():
    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content":[
            {"type": "text","text": "Extract all text from this image without any styling or formatting"},
            {"type": "image_url",
              "image_url": {
                "url": f"data:image/{row['image_file_type']}; base64, {row['base64_image']}"
              }
            }
          ]
        }
      ]
    )

    df.at[index, 'Actual Extracted Text'] = response.choices[0].message.content

    with open(f"../chatgpt_responses/text_extraction/{row['Test ID']}.json", "w", encoding="utf-8") as outfile:
      outfile.write(response.choices[0].message.content)

    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {
          "role": "user",
          "content":[
            {"type": "text","text": "Is this a Court Record? If so, what type of Court Record is it?"},
            {"type": "image_url",
              "image_url": {
                "url": f"data:image/{row['image_file_type']}; base64, {row['base64_image']}"
              }
            }
          ]
        }
      ]
    )

    df.at[index, 'Actual Output: Classification'] = response.choices[0].message.content

    with open(f"../chatgpt_responses/classification/{row['Test ID']}.json", "w", encoding="utf-8") as outfile:
      outfile.write(response.choices[0].message.content)

    print(f"Test ID {index+1} Complete")

  #Clean Up Dataframe/CSV
  df = df.drop(columns=['base64_image', 'image_file_type'])

  df.to_csv('../test_table_files/02-chatgpt_test_table.csv')

