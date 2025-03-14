# Metadata
__script_name__ = "Chato"
__author__ = "S.T.Sathish (SKYLIB)"
__email__ = "skylib.stsathish@gmail.com"
__website__ = "https://skylib11.wordpress.com"
__repository__ = "https://github.com/skylib11/Chato.git"
__date__ = "14-March-2025"
__copyright__ = "Copyright (c) 2025 S.T.Sathish (SKYLIB)"
__version__ = "2.0.0"

import csv
import os
import logging
import sys

logging.basicConfig(
    filename='Chato.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def show_metadata():
    """Display script metadata."""
    metadata = {
        "Script Name": __script_name__,
        "Author": __author__,
        "Email": __email__,
        "Website": __website__,
        "Repository": __repository__,
        "Date": __date__,
        "Copyright": __copyright__,
        "Version": __version__
    }

    for key, value in metadata.items():
        print(f"{key}: {value}")

class SkylibChatbot:
    def __init__(self, KNOWLEDGE_FILE="Knowledge.csv"):
        self.KNOWLEDGE_FILE = KNOWLEDGE_FILE
        if not os.path.exists(self.KNOWLEDGE_FILE):
            with open(self.KNOWLEDGE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Question", "Responses"])
        self.load_knowledge()

    def load_knowledge(self):
        """Load knowledge base into memory."""
        self.knowledge = []
        try:
            with open(self.KNOWLEDGE_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.knowledge.append((row["Question"], row["Responses"]))
            logging.info("Knowledge base loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading knowledge: {e}")

    def keyword_match(self, user_input):
        """Simple keyword matching algorithm."""
        try:
            for question, responses in self.knowledge:
                words = user_input.split()
                if all(word.lower() in question.lower() for word in words):
                    return question, responses.split("||")
        except Exception as e:
            logging.error(f"Error in keyword_match: {e}")
        return None, None

    def simple_match(self, user_input):
        """Simple exact match check."""
        try:
            for question, responses in self.knowledge:
                if user_input.strip().lower() == question.strip().lower():
                    return question, responses.split("||")
        except Exception as e:
            logging.error(f"Error in simple_match: {e}")
        return None, None

    def search_response(self, user_input):
        """Combine multiple search algorithms."""
        try:
            question, responses = self.keyword_match(user_input)
            if question:
                return question, responses

            question, responses = self.simple_match(user_input)
            if question:
                return question, responses
        except Exception as e:
            logging.error(f"Error in search_response: {e}")
        return None, None

    def save_response(self, question, response):
        """Save a new or updated response to the knowledge base."""
        try:
            existing_question, existing_responses = self.search_response(question)
            if existing_responses:
                if response not in existing_responses:
                    updated_responses = "||".join(existing_responses + [response])
                    self.update_response(question, updated_responses)
            else:
                self.learn_response(question, response)
        except Exception as e:
            logging.error(f"Error in save_response: {e}")

    def learn_response(self, question, response):
        """Add a new question-response pair."""
        try:
            with open(self.KNOWLEDGE_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([question, response])
            self.load_knowledge()
            logging.info(f"Learned new response for question: {question}")
        except Exception as e:
            logging.error(f"Error in learn_response: {e}")

    def update_response(self, question, responses):
        """Update existing question's responses."""
        try:
            rows = []
            for q, r in self.knowledge:
                if q.strip().lower() == question.strip().lower():
                    rows.append((q, responses))
                else:
                    rows.append((q, r))

            with open(self.KNOWLEDGE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Question", "Responses"])
                writer.writerows(rows)
            self.load_knowledge()
            logging.info(f"Updated response for question: {question}")
        except Exception as e:
            logging.error(f"Error in update_response: {e}")

    def chat(self):
        try:
            print(f"Hello! What's your name?")
            user_name = input("You:").strip()
            print(f"SKYLIB: Nice to meet you, {user_name}!")

            print("SKYLIB: I'm SKYLIB. Type 'exit' to end the chat.")
            while True:
                user_input = input(f"{user_name}: ").strip()
                if user_input.lower() == "exit":
                    print(f"SKYLIB: Goodbye, {user_name}!")
                    break

                question, responses = self.search_response(user_input)
                if responses:
                    print(f"SKYLIB: {responses[0]}")
                    feedback = input("Was this response satisfactory?\n(yes/no):")
                    feedback = feedback.strip().lower()
                    if feedback == "no":
                        print("SKYLIB: What should I say instead?")
                        new_response = input().strip()
                        self.save_response(question, new_response)
                        print("SKYLIB: Learnt.")
                else:
                    print(f"SKYLIB: I don't have a response. I'm learning.\n"
                          f"What should I answer?\n{user_name}: ", end="")
                    new_response = input().strip()
                    self.save_response(user_input, new_response)
                    print("SKYLIB: Learnt.")
        except KeyboardInterrupt:
            print("\nSKYLIB: Chat interrupted. Goodbye!")
            logging.info("Chat interrupted by user.")
        except Exception as e:
            logging.error(f"Error in chat loop: {e}")
            
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--about", "-i"]:
        show_metadata()
        sys.exit(0)

skylib = SkylibChatbot()
skylib.chat()
