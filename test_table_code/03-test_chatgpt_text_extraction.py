import pandas as pd

df = pd.read_csv("../test_table_files/02-chatgpt_test_table.csv")

# Total List Count = Total Points possible to be correct on
# Miss = 0 point
# Correct = 1 point


#Due to ChatGPT's responses include special characters to help with readability,
# Complete matches from string to string is an incorrect metric to measure correctness.
# As long as the string exist as a substring in the ChatGPT Response string, they will be awarded points
# except for strings with less than 3 characters

# Test with 1 ROW

for index, row in df.iterrows():

  #Expected Text
  expectedList = df.iloc[index]['Expected Extracted Text'].split()
  #Actual Extracted Text
  actualList = df.iloc[index]['Actual Extracted Text'].split()

  #Total Points Possible are determined by the total items in List in Expected Extracted Text
  totalPoints = len(expectedList) #Here is 254
  awardedPoints = 0

  comparisonList = [] #This is to compare the "matched" strings, manually
  expectedRemainingList = list(expectedList) #Editable Expected Extracted Text List
  fewcList = [] #This list is to store text entry with fewer than <=3 characters

  # Phase 1: Test More than 3-character Strings

  for expectedText in expectedList:
    if(len(expectedText) <= 2):
      fewcList.append(expectedText)
    else:
      for actualText in actualList:
        if expectedText in actualText:
          comparisonList.append(f"{expectedText} || {actualText}")
          expectedRemainingList.remove(expectedText)
          actualList.remove(actualText)
          if( expectedText == actualText):
            awardedPoints += 1
          elif( expectedText != actualText):
            awardedPoints += 0.5
          break

  #Problem faced during the Matching Phase is 1-3 character strings
  # This is due to the logic where the matching is done by finding the existence of an expected character
  # in a substring. It can be anything, for example: 8 can exist in 54853.

  # Phase 2: Matching of 2 character

  for expectedText in expectedRemainingList:
      for actualText in actualList:
        if expectedText in actualText:
          comparisonList.append(f"{expectedText} || {actualText}")
          expectedRemainingList.remove(expectedText)
          actualList.remove(actualText)

          if( expectedText == actualText):
            awardedPoints += 1
          elif( expectedText != actualText):
            awardedPoints += 0.5
          break

  # Phase 3: Complete Matching of 1 Character
  for expectedText in expectedRemainingList:
    for actualText in actualList:
      if(expectedText == actualText):
        awardedPoints += 1
        expectedRemainingList.remove(expectedText)
        actualList.remove(actualText)
        break

  with open(f"../test_results/expected_remaining_text/{df.iloc[index]['Test ID']}.txt", 'w', encoding="utf-8") as outfile:
    for line in expectedRemainingList:
      outfile.write(f"{line}\n")

  with open(f"../test_results/actual_remaining_text/{df.iloc[index]['Test ID']}.txt", 'w', encoding="utf-8") as outfile:
    for line in actualList:
      outfile.write(f"{line}\n")

  with open(f"../test_results/matched_comparison_list/{df.iloc[index]['Test ID']}.txt", 'w', encoding="utf-8") as outfile:
    for line in comparisonList:
      outfile.write(f"{line}\n")

  #Write to dataframe
  df['Remaining Text after Test'] = df['Remaining Text after Test'].astype(str)
  df['Actual Output: Text Extraction'] = df['Actual Output: Text Extraction'].astype(str)

  df.at[index, 'Remaining Text after Test'] = "\n".join(actualList)
  df.at[index, 'Points Correct: Text Extraction'] = awardedPoints/totalPoints

  if(awardedPoints != totalPoints and awardedPoints != 0):
    df.at[index, 'Actual Output: Text Extraction'] = "Extracted Partially"
  elif (awardedPoints == totalPoints):
    df.at[index, 'Actual Output: Text Extraction'] = "Extracted Completely"
  else:
    df.at[index, 'Actual Output: Text Extraction'] = "Extracted None"

df.to_csv('../test_table_files/03-chatgpt_text_extraction_results.csv')