import S01_add_base64_encoding
import S02_chatgpt_responses
import S03_test_chatgpt_text_extraction
import S04_test_chatgpt_classification
import time
import datetime

def main():
  print("Automation: Convert Image to Base64 Encoding")
  S01_add_base64_encoding.main()
  print("Automation: Retrieve Text Extraction and Classification from ChatGPT")
  S02_chatgpt_responses.main()
  print("Automation: Test Text Extraction")
  S03_test_chatgpt_text_extraction.main()
  print("Automation: Test Classification")
  S04_test_chatgpt_classification.main()

if __name__ == "__main__":
  start = time.time()
  print("Beginning Automation Demo")
  main()
  end = time.time()
  print(f"Automation Completed in {datetime.timedelta(seconds=end-start)}\n")
  print("To View Results: Find 04-final-results.csv in test_table_files Folder")
