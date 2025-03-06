## Chatbot Python Script

This Python chatbot script is a simple yet efficient program that can answer user questions. If the chatbot doesn't know the answer to a question, it learns by saving the question and the corresponding answer to a file, enabling it to recall and respond appropriately when asked the same question in the future.

**Key Features:**
**Dynamic Learning:** If the chatbot encounters a question it doesn’t have an answer to, it prompts the user for an answer and stores both the question and the response in a file.

**Persistent Memory:** The chatbot "remembers" previous interactions by storing the questions and answers in a csv file. When the question is asked again, the chatbot retrieves the saved answer, simulating memory and improving over time.

**Simple Interface:** The chatbot communicates with the user via the command line or console, making it easy to interact with.

**Effortless Expansion:** The script is lightweight and can be expanded with more sophisticated features or integrated with external databases for advanced memory management.

**How it Works:**
The chatbot reads for user input and checks if it already has an answer stored.
If a matching answer is found in the memory (file), it responds accordingly.
If no answer is found, the chatbot asks the user for the correct response and saves both the question and the new answer.
The chatbot retrieves saved answers and provides quick responses for future interactions.

**How to Use:**
Clone or download the Python script.
Run the script in your terminal or command line.
Start asking questions. If the answer is unknown, provide the correct response, and it will be remembered.
The next time you ask the same question, the chatbot will recall and provide the stored answer.

**Chatbot needs to learn:**
The chatbot is not given any existing datas. It needs input and learnings from the user. So, when you start, it might not have responses for most of the questions.

This script is perfect for anyone looking for a quick and simple way to create a chatbot that learns and "remembers" user interactions over time, with minimal setup.
