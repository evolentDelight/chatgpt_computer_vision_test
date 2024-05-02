import pandas as pd

df = pd.read_csv("../test_table_files/03-chatgpt_text_extraction_results.csv")

for index, row in df.iterrows():
  awardedPoints = 0
  totalPoints = 2

  keywords = row['Expected Output: Classification'].lower().replace(" ", ".").split(".")
  chatgpt_response = row['Actual Output: Classification'].lower()

# Check if the document is recognized as a court record
  if "yes" in chatgpt_response:
    awardedPoints += 1

# Check if it correctly classifies as the 
  classificationPoints = 0
  for keyword in keywords:
    if keyword in chatgpt_response:
      classificationPoints += 1
    if keyword == "crime": #hardcoded due to nested csv... for now...
      if "criminal" in chatgpt_response:
        classificationPoints += 1
  
  if classificationPoints > 0:
    awardedPoints +=1
  
  df.at[index, 'Points Correct: Classification'] = awardedPoints

df.to_csv('../test_table_files/04-chatgpt_classification_results.csv')
