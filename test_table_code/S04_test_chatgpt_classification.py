import pandas as pd

def main():
  df = pd.read_csv("../test_table_files/03-chatgpt_text_extraction_results.csv")

  df['Classification Test Result'] = df['Classification Test Result'].astype(str)

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

    if(awardedPoints == 2):
      df.at[index, 'Classification Test Result'] = "Pass"
    else:
      df.at[index, 'Classification Test Result'] = "Fail"

  df.to_csv('../test_table_files/04-final-results.csv')
