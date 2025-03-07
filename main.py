import os
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

# Step 1: Set up Gemini
GEMINI_API_KEY = "AIzaSyBGZjafGGMHwSB4Gq234s9Jmoc_rxgtv-k"
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=GEMINI_API_KEY)

# Step 2: Define a static PDF summary
pdf_summary = '''
The document discusses the impact of climate change on global agriculture. 
It highlights that rising temperatures and unpredictable weather patterns are causing crop failures, 
reducing yields, and threatening food security. The summary also emphasizes the need for sustainable 
farming practices and the adoption of climate-resilient crops to mitigate these effects.
'''

# Step 3: Generate a two-person conversation using Gemini
def generate_conversation() -> str:
    prompt = f'''
    Create a conversation discussing the following summary:
    {pdf_summary}

    The conversation should be between two individuals, a female (Person A) and a male (Person B). 
    Person A should ask questions, and Person B should provide detailed answers.
    '''

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use "gemini-pro" or "gemini-1.0-pro"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating conversation: {e}")
        return ""

# Step 4: Convert the conversation to audio using ElevenLabs
def text_to_audio(text: str, female_voice: str = "Rachel", male_voice: str = "Domi") -> None:
    try:
        api_key = "sk_94cd146591797de121db944e8cf15b6dbde3dc56ea9135c4"
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable is not set.")

        client = ElevenLabs(api_key=api_key)

        # Split the conversation into lines
        lines = text.split('\n')
        combined_audio = b""

        for line in lines:
            if line.startswith("Person A:"):
                # Generate audio for Person A (female)
                female_text = line.replace("Person A:", "").strip()
                if female_text:
                    female_audio_generator = client.generate(
                        text=female_text,
                        voice=female_voice
                    )
                    for chunk in female_audio_generator:
                        if isinstance(chunk, bytes):
                            combined_audio += chunk
            elif line.startswith("Person B:"):
                # Generate audio for Person B (male)
                male_text = line.replace("Person B:", "").strip()
                if male_text:
                    male_audio_generator = client.generate(
                        text=male_text,
                        voice=male_voice
                    )
                    for chunk in male_audio_generator:
                        if isinstance(chunk, bytes):
                            combined_audio += chunk

        if combined_audio:
            with open("conversation.mp3", "wb") as f:
                f.write(combined_audio)
            print("Audio saved to conversation.mp3")

            play(combined_audio)
        else:
            print("Error: No audio data was generated.")

    except Exception as e:
        print(f"An error occurred: {e}")
# Main function
if __name__ == "__main__":
    conversation = generate_conversation()
    if conversation:
        print("Generated Conversation:")
        print(conversation)

        text_to_audio(conversation)
    else:
        print("Failed to generate conversation.")
