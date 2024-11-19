from openai import OpenAI
from record_audio import record_audio, today
from speech_to_text import transcribe, speak_text
import os
import string
from dotenv import load_dotenv

load_dotenv()
# Personal news api key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key = OPENAI_API_KEY,
)

# Function to save the transcript
def save_transcript(transcript, message_count):
    directory = f"./user_inputs/{today}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    transcript_path = f"{directory}/user_transcript_{message_count}.txt"
    
    with open(transcript_path, "w") as file:
        file.write(transcript)
    
    print(f"Transcript saved at {transcript_path}")


def clean_transcript(transcript):
    """Strip text and move to lower case"""
    return transcript.strip().lower().translate(str.maketrans('', '', string.punctuation))


def generate_response(conversation):
    # Generate a response from Pierre using GPT-4
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=conversation
    )
    return completion.choices[0].message.content


# Recursive conversation function
def chat_with_pierre(conversation, mode = 'text', message_count=1):

    # Get user input
    if mode == 'text':
        user_input = input("You: ")

        # Append the user's input to conversation
        conversation.append({"role": "user", "content": user_input})

        # If user types 'exit', end the conversation
        if user_input.lower() == "exit":
            print("Pierre: Au revoir ! Passe une bonne journée !")
            return

    elif mode == 'audio':

        file_path = f"user_audio_{message_count}"
        audio_file_path = record_audio(file_path)

        print(audio_file_path)
        transcript = transcribe(audio_file_path)

        save_transcript(transcript, message_count)

        cleaned_transcript = clean_transcript(transcript)

        if cleaned_transcript in ['exit', 'stop', 'sortir', 'adiós']:
            print("Pierre: Au revoir ! Passe une bonne journée !")
            return

        # Append the user's input to the conversation
        conversation.append({"role": "user", "content": transcript})

    response = generate_response(conversation=conversation)

    if mode == "text":
        print("Pierre: " + response)

    elif mode == "audio":
        print("Pierre: " + response)
        speak_text(response)

    # Append Pierre's response to the conversation history
    conversation.append({"role": "assistant", "content": response})

    # Recursive call to continue conversation
    chat_with_pierre(conversation, mode, message_count=message_count+1)


# Start the recursive conversation loop
def main():
    print("Bienvenue! Would you like to talk to Pierre using text or audio?")
    mode_choice = input("Type 'text' for text-based conversation or 'audio' for audio-based conversation: ").strip().lower()

    if mode_choice not in ["text", "audio"]:
        print("Please choose either 'text' or 'audio'.")
        return
    
    # Initial system message
    system_message = {
        "role": "system", 
        "content": "You are a friendly French-speaking assistant named Pierre. Answer user inputs in French and engage in casual and/or helpful conversation."
    }
    conversation = [system_message]

    # Start the conversation loop with the chosen mode
    chat_with_pierre(conversation, mode=mode_choice)

if __name__ == "__main__":
    main()
