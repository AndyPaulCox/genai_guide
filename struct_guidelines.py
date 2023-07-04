# This code creates two new functions: summarise_text and data_prep.
# The summarise_text function takes a string of text as input, uses the OpenAI
# API to generate a summary of the text using the ChatGPT 3.5 model, and returns the summary.
# The data_prep function cleans and summarises the text chunks in the DataFrame.
# It loops through each row in the DataFrame, cleans the text chunk, and skips the
# iteration if the cleaned text is empty. It then summarises the cleaned text, splits the
# summary into statements, and appends each statement along with the corresponding filename
# and date to the data list. This list is then converted into a pandas DataFrame.
# You might need to adjust the temperature and max_tokens parameters based on your specific needs.
# The temperature parameter controls the randomness of the generated text (higher values make the
# text more random), while the max_tokens parameter controls the maximum length of the generated summary.
# Again, please note that usage of GPT-3 involves cost, and you'll need API credentials from OpenAI
# to access their models. You should also handle exceptions and add error checks as necessary,
import openai
# Function to summarise the text
def summarise_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003.5",  # Use the ChatGPT 3.5
        prompt=text,
        # Higher value (close to 1) means more randomness, lower value (close to 0) means more determinism
        temperature=0.3,
        max_tokens=100  # Maximum length of the generated summary
    )
    return response.choices[0].text.strip()


# Function to prepare the data
def data_prep(df):
    # Initialize an empty list to store the data
    data = []
    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        # Clean the text chunk
        text = clean_text(row['text_chunk'])
        # Skip this iteration if the cleaned text is empty
        if not text:
            continue
        # Summarise the text chunk
        summary = summarise_text(text)
        # Split the summary into statements
        statements = summary.split('. ')
        # Loop through each statement
        for statement in statements:
            # Append a dictionary with the filename, date, and statement to the data list
            data.append({'filename': row['filename'],
                         'date': row['date'],
                         'text_chunk': statement})
    # Convert the data list into a pandas DataFrame and return it
    return pd.DataFrame(data)
