import json


class Conversation:
    def __init__(self, data):
        self.messages = self.get_messages(data)

    def get_messages(self, data):
        messages = []
        # Check if 'mapping' is present and is a dictionary
        mapping = data.get("mapping", {})
        if isinstance(mapping, dict):
            for key in mapping:
                message_dict = mapping[key].get("message", {})
                if not message_dict:
                    continue
                content = message_dict.get("content", {})
                if isinstance(content, dict):
                    parts = content.get("parts", [])
                    if parts and isinstance(parts, list):
                        if parts[0] and isinstance(parts[0], str):
                            messages.append(parts[0])  # Safely add the message part
                        elif parts[0] and isinstance(parts[0], dict):
                            messages.append(parts[0].get("text", ""))
        return messages


class History:
    def __init__(self, filename):
        self.conversations = self.load_data(filename)

    def load_data(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return [Conversation(conversation) for conversation in data]
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except json.JSONDecodeError:
            print("Failed to decode JSON. Please check the file content.")
            return []

    def search(self, keyword):
        results = []
        for conversation in self.conversations:
            for message in conversation.messages:
                if keyword.lower() in message.lower():
                    results.append(message)
        return results


# Usage
file = "/path/to/conversations.json"
hist = History(file)
search = "genetic algorithm"
results = hist.search(search)
with open(f"{search}.md", "w") as file:
    for result in results:
        file.write(f"- {result}\n")
