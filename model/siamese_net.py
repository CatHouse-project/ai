import json
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import numpy as np
from scipy.spatial.distance import cosine

# Load JSON data
data_path = 'data//random_survey_responses.json'
with open(data_path, 'r') as file:
    raw_data = json.load(file)

# Extract responses in a structured format
def preprocess_responses(raw_data):
    # Extract each response and convert answers to tensor format
    return torch.tensor([[entry['responses'][i]['question_answer'] for i in range(30)] for entry in raw_data])

# Convert loaded JSON data to tensor format
data_tensor = preprocess_responses(raw_data)
train_tensor, test_tensor = train_test_split(data_tensor, test_size=0.2, random_state=42)

# Define model parameters
num_questions = 30
embedding_dim = 16
learning_rate = 0.0005
num_epochs = 5


# Define the Siamese Network
class SiameseNetwork(nn.Module):
    def __init__(self, input_size, embedding_dim):
        super(SiameseNetwork, self).__init__()
        self.embedding = nn.Embedding(4, embedding_dim)  # For answers 1, 2, 3
        self.fc1 = nn.Linear(input_size * embedding_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)

    def forward(self, x, weights=None):
        x = self.embedding(x)  # Embed each question response
        if weights is not None:
            x = x * weights.unsqueeze(-1)  # Apply weights to each embedded dimension
        x = x.view(x.size(0), -1)  # Flatten
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)  # Output 32-dimensional vector

# Initialize model and optimizer
model = SiameseNetwork(num_questions, embedding_dim)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


# Dummy training function for Siamese Network
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    embeddings = model(train_tensor)
    loss = criterion(embeddings, embeddings)  # Using self-pair loss for simplicity
    loss.backward()
    optimizer.step()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")


# Function to find similar users
def find_similar_users(user_id, core_questions, core_weight, num_results):
    # Find requested user from raw_data
    requested_user = next((user for user in raw_data if user["user"] == user_id), None)
    if requested_user is None:
        print("User not found.")
        return []

    # Convert requested user's responses to tensor format
    user_tensor = torch.tensor(
        [requested_user['responses'][i]['question_answer'] for i in range(num_questions)]).unsqueeze(0)

    # Create weights tensor with higher weights for core questions
    weights = torch.ones(num_questions)  # Set default weight to 1 for all questions
    for q in core_questions:
        weights[q - 1] = core_weight  # Set higher weight for core questions

    # Get embeddings of requested user and all users in the dataset with weights applied
    user_embedding = model(user_tensor, weights=weights)
    all_embeddings = model(train_tensor, weights=weights)

    # Calculate cosine similarity between requested user and all users in the dataset
    similarities = [1 - cosine(user_embedding.detach().numpy().flatten(), e.detach().numpy().flatten())
                    for e in all_embeddings]

    # Get top N similar users based on similarity scores
    top_indices = np.argsort(similarities)[-num_results:]
    similar_user_ids = [raw_data[i]["user"] for i in top_indices]

    return similar_user_ids

if __name__ == '__main__':
    # Example usage
    user_id = 893539  # Example user_id to search in the JSON data
    core_questions = [1, 5, 10, 22, 30]  # Important question numbers
    core_weight = 10.0  # High weight for core questions
    num_results = 5

    similar_user_ids= find_similar_users(user_id, core_questions, core_weight, num_results)
    print(similar_user_ids)


    # Function to calculate similarity percentages for core and non-core questions
    def calculate_similarity(user_id_A, user_id_B, core_questions):
        # Retrieve responses for both users
        user_A = next((user for user in raw_data if user["user"] == user_id_A), None)
        user_B = next((user for user in raw_data if user["user"] == user_id_B), None)

        if user_A is None or user_B is None:
            print(f"One of the users {user_id_A} or {user_id_B} was not found.")
            return

        # Extract answers for both users
        answers_A = [resp["question_answer"] for resp in user_A["responses"]]
        answers_B = [resp["question_answer"] for resp in user_B["responses"]]

        # Calculate core and non-core question similarities
        core_matches = sum(1 for q in core_questions if answers_A[q - 1] == answers_B[q - 1])
        non_core_matches = sum(
            1 for q in range(1, num_questions + 1) if q not in core_questions and answers_A[q - 1] == answers_B[q - 1])

        # Calculate percentages
        core_percentage = (core_matches / len(core_questions)) * 100
        non_core_percentage = (non_core_matches / (num_questions - len(core_questions))) * 100

        # Print results
        print(f"Similarity between user {user_id_A} and user {user_id_B}:")
        print(f"  Core questions match: {core_percentage:.2f}%")
        print(f"  Non-core questions match: {non_core_percentage:.2f}%\n")


    # Example usage: Run similarity check 5 times
    for i in range(5):
        if i < len(similar_user_ids):
            calculate_similarity(user_id, similar_user_ids[i], core_questions)
