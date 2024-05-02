import pandas as pd

# Purpose of this script:
# Calculate Results
# Output Results
# Clean Up CSV(Delete base64_image column, image_file_type)
# Load test_results files into appropriate columns
#  i.e.: expected_remaining_text, actual_remaining_text, matched_comparison_list

dirty_df = pd.read_csv('../test_table_files/04-chatgpt_classification_results.csv')

#Clean Up Dataframe/CSV
df = dirty_df.drop(columns=['base64_image', 'image_file_type'])

#Calculate Results By Document
# Classification: 100%, 50%, 0%
# Text Extraction: Completely, Partially, None

#Court Record Types
cr_types = df['Court Record Type'].unique()
#Get Lowest and Highest Score with Appropriate Test ID and Description

results = pd.DataFrame({'Court Record Type': cr_types[:]})
results['Average Accuracy: Classification'] = 0.0
results['Average Accuracy: Text Extraction'] = 0.0
results['Best Accuracy: Text Extraction'] = 0.0
results['Worst Accuracy: Text Extraction'] = 0.0
results['Best Accuracy: Text Extraction: Test ID'] = 0
results['Worst Accuracy: Text Extraction: Test ID'] = 0

for cr_type in cr_types:
  df_type = df[df['Court Record Type'] == cr_type]

  #Get Index of Court Record Type Row
  index = results[results["Court Record Type"] == cr_type].index.tolist()[0] # [0] due to it being a list
  
  # Average Accuracy: Classification
  csum = df_type['Points Correct: Classification'].sum()
  cresult = csum/(len(df_type.index) * 2) # Sum / Total Possible Score(amount * 2)

  results.at[index, 'Average Accuracy: Classification'] = cresult

  # Average Accuracy: Text Extraction
  # For reasons of reading capability, the column is in type 'String'. Convert to float
  tesum = df_type['Points Correct: Text Extraction'].sum()
  teresult = tesum/(len(df_type.index))

  results.at[index, 'Average Accuracy: Text Extraction'] = teresult

  # Best Accuracy: Text Extraction
  temax = df_type['Points Correct: Text Extraction'].max()

  results.at[index, 'Best Accuracy: Text Extraction'] = temax

  df_row = df.loc[(df['Court Record Type'] == cr_type) & (df['Points Correct: Text Extraction'] == temax)]
  results.at[index, 'Best Accuracy: Text Extraction: Test ID'] = df_row.at[df_row.index.tolist()[0], 'Test ID']
  # Worst Accuracy: Text Extraction
  temin = df_type['Points Correct: Text Extraction'].min()

  results.at[index, 'Worst Accuracy: Text Extraction'] = temin

  df_row = df.loc[(df['Court Record Type'] == cr_type) & (df['Points Correct: Text Extraction'] == temin)]
  results.at[index, 'Worst Accuracy: Text Extraction: Test ID'] = df_row.at[df_row.index.tolist()[0], 'Test ID']

df['Expected Text: Remaining'] = ""
df['Matched Text Comparison'] = ""

for index, row in df.iterrows():
  with open(f"../test_results/expected_remaining_text/{df.iloc[index]['Test ID']}.txt", "r", encoding="utf-8") as infile:
    data = infile.read()
    df.at[index, 'Expected Text: Remaining'] = data

  with open(f"../test_results/matched_comparison_list/{df.iloc[index]['Test ID']}.txt", "r", encoding="utf-8") as infile:
    data = infile.read()
    df.at[index, 'Matched Text Comparison'] = data

df.to_csv('../test_table_files/05-final-results-data.csv')
results.to_csv('../test_table_files/05-final-results-statistics.csv')