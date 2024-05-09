import pandas as pd

#old df
odf = pd.read_csv("../test_table_files/05-final-results-data.csv")

# Compare by Expected to Actual Texts
#   Complete Text
#   Remaining Text After Test
# Last Column contains Matched Comparison
df = pd.DataFrame()

df['Expected Extracted Text'] = odf['Expected Extracted Text']
df['Actual Extracted Text'] = odf['Actual Extracted Text']
df['Expected Text: Remaining'] = odf['Expected Text: Remaining']
df['Actual Text: Remaining'] = odf['Remaining Text after Test']
df['Matched Text'] = odf['Matched Text Comparison']

df.to_csv("../test_table_files/06-test_results_comparison.csv")