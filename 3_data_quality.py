import pandas as pd
import json

def load_json_lines(file_path):
  data = []
  with open(file_path, 'r') as f:
    for line in f:
      try:
        json_record = json.loads(line)
        data.append(json_record)
      except json.JSONDecodeError as e:
        print(f'Decoding error: {e} in line: {line.strip()}')

  return pd.DataFrame(data)

def load_users_file():
  user_df = load_json_lines("users.json")
  print(user_df.info())

load_users_file()