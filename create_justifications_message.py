import pandas as pd

df = pd.read_csv('./data/justifications.csv')

questions = df['question'].unique()

message = ""

for question in questions:
    question_df = df[df['question'] == question]
    message += f"Stwierdzenie: \n{question}\n\n"
    message += f"Odpowiedzi:\n\n"
    for _, row in question_df.iterrows():
        message += f"{row['party_name']}: \n{row['comment_text']}\n\n"


with open('./data/justifications_message.txt', 'w') as f:
    f.write(message)