"""
Author: S.T.Sathish (SKYLIB)
Email: skylib.stsathish@gmail.com
Website: https://beacons.ai/skylib
Date Created: 16-December-2024
Description: Python ChatBot Script
This Python chatbot script is a straightforward and efficient program designed to answer user questions. 
If the chatbot encounters a question it cannot answer, it intelligently adapts by saving the question and the corresponding answer to a file. 
This allows the chatbot to learn and respond accurately when the same question is asked in the future, improving its knowledge base over time.

Program Generated with: ChatGPT (OpenAI)

Copyright (c) [2024] S.T.Sathish (SKYLIB)
"""
import csv
import os
from fuzzywuzzy import process  # Install with `pip install fuzzywuzzy`

class SkylibChatbot:
    def __init__(self, knowledge_file="knowledge.csv"):
        self.knowledge_file = knowledge_file
        # Ensure the knowledge file exists
        if not os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Question", "Responses"])  # Initialize with headers

    def learn_response(self, question, response):
        """Add a new question-response pair to the knowledge base."""
        with open(self.knowledge_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([question, response])

    def get_all_questions(self):
        """Retrieve all questions from the knowledge base."""
        with open(self.knowledge_file, mode='r') as file:
            reader = csv.DictReader(file)
            return [row["Question"] for row in reader]

    def search_response(self, user_input):
        """Search for the best match to the user input in the knowledge base."""
        questions = self.get_all_questions()
        if not questions:
            return None, None

        # Find the best match
        best_match, score = process.extractOne(user_input, questions)
        if score >= 70:  # Threshold for satisfactory match
            with open(self.knowledge_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Question"].strip().lower() == best_match.strip().lower():
                        return best_match, row["Responses"].split("||")
        return None, None

    def save_response(self, question, response):
        """Save a learned response to the knowledge base."""
        _, existing_responses = self.search_response(question)
        if existing_responses:
            if response not in existing_responses:
                updated_responses = "||".join(existing_responses + [response])
                self.update_response(question, updated_responses)
        else:
            self.learn_response(question, response)

    def update_response(self, question, responses):
        """Update an existing question's responses."""
        rows = []
        with open(self.knowledge_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Question"].strip().lower() == question.strip().lower():
                    row["Responses"] = responses
                rows.append(row)

        with open(self.knowledge_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Question", "Responses"])
            writer.writeheader()
            writer.writerows(rows)

    def chat(self):
        # Ask for the user's name at the beginning
        user_name = input("SKYLIB: Hello! What's your name? ").strip()
        print(f"SKYLIB: Nice to meet you, {user_name}!")

        print("SKYLIB: I'm SKYLIB. Type 'exit' to end the chat.")
        while True:
            user_input = input(f"{user_name}: ").strip()
            if user_input.lower() == "exit":
                print(f"SKYLIB: Goodbye, {user_name}!")
                break

            # Search for a response in the knowledge base
            question, responses = self.search_response(user_input)
            if responses:
                print(f"SKYLIB: {responses[0]}")  # Default to the first response
                feedback = input("Was this response satisfactory? (yes/no): ").strip().lower()
                if feedback == "no":
                    print("SKYLIB: What should I say instead?")
                    new_response = input("You: ").strip()
                    self.save_response(question, new_response)
                    print("SKYLIB: Learnt.")
            else:
                # Learn a new response
                print("SKYLIB: I don't have a response. I'm learning. What should I answer you?")
                new_response = input("You: ").strip()
                self.save_response(user_input, new_response)
                print("SKYLIB: Learnt.")


# Create and start the chatbot
skylib = SkylibChatbot()
skylib.chat()

