import pandas as pd

# load your data into a dataframe
df = pd.read_csv("lumine_bot.csv")
# print(df)

print("Luminebot: Hello there,I am your lumine bot.Ask me about my collection.")

while True:
    # Get the user input and store into a variable
    user_text = input("\n You:").lower()
    

    # 2. Check if the users want to exit
    if user_text == "quit":
        print("Luminebot:Goodbye! Nice to have been of service to you.Stay Fashionable.")
        break

    # create a variable that will store the details structured in the csv file
    found_answer = False

    # come up with a loop that loops through the entire data frame created before.
    for index,row in df.iterrows():
        # clean up the keywords from the CSV row
        keywords_list = str(row['Keywords']).split(',')

        # Below we check every keyword in that given row(Keywords)

        for word in keywords_list:
            clean_word = word.strip().lower()

            # if the keyword is inside of the user's sentence
            if clean_word in user_text:
                print("Luminebot:", row["Responses"])
                found_answer = True
                break #stop looking at other answers since we already found a match
        if found_answer:
            break #stop looking at other answers since we already found a match
    # 4. If we went through the entire/whole CSV file and never found any match of the keywords,we need to display a message to the user
    if not found_answer:
        print("Luminebot: Sorry,I don't know that one,Try asking for something else.")