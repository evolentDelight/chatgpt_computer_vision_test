import pandas as pd

def main():
  df = pd.read_csv("../test_table_files/02-chatgpt_test_table.csv")

  #Due to ChatGPT's responses include special characters to help with readability,
  # Complete matches from string to string is an incorrect metric to measure correctness.
  # As long as the string exist as a substring in the ChatGPT Response string, they will be awarded points
  # except for strings with less than 3 characters

  testResult = [] #append String Category : Pass/Fail : score / total_score
  failedTest = []

  df['Test Result By Category'] = df['Test Result By Category'].astype(str)
  df['Failed Test By Category'] = df['Failed Test By Category'].astype(str)

  for index, row in df.iterrows():
    testResult = []
    failedTest = []

    categoryToTest = df.iloc[index]['Category To Test'].split("\n")
    categoryContentList = df.iloc[index]['Text By Category'].split("\n")

    actualList = df.iloc[index]['Actual Extracted Text'].split()

    score = 0
    totalScore = 0

    for idx, category in enumerate(categoryToTest):
      categoryList = categoryContentList[idx].split(" ")
      remainingList = list(categoryList)
      comparisonList = []

      score = 0
      totalScore = len(categoryList)

      for expectedText in categoryList:
        for actualText in actualList:
          if(expectedText == actualText):
            comparisonList.append(f"{expectedText} || {actualText}")
            remainingList.remove(expectedText)
            score += 1
            break

      with open(f"../test_results/matched_comparison_list/{df.iloc[index]['Test ID']}[{category}].txt", 'w', encoding="utf-8") as outfile:
        for line in comparisonList:
          outfile.write(f"{line}\n")

      if(score == totalScore):
        testResult.append(f"[{category} : Pass : {score}/{totalScore}]")
      else:
        testResult.append(f"[{category} : Fail : {score}/{totalScore}]")
        failedTestContent = " || ".join(remainingList)
        failedTest.append(f"[{category} : {failedTestContent}]")
    
    df.at[index, 'Test Result By Category'] = "\n".join(testResult)
    df.at[index, 'Failed Test By Category'] = "\n".join(failedTest)

  df.to_csv('../test_table_files/03-chatgpt_text_extraction_results.csv')