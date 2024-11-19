from speechmatics.models import ConnectionSettings
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError
import pyttsx3
import os
from dotenv import load_dotenv

load_dotenv()
# Personal news api key
SPEECHMATICS_API_KEY = os.getenv('SPEECHMATICS_API_KEY')

LANGUAGE = "fr"

settings = ConnectionSettings(
    url="https://asr.api.speechmatics.com/v2",
    auth_token=SPEECHMATICS_API_KEY,
)

# Define transcription parameters
conf = {
    "type": "transcription",
    "transcription_config": {
        "language": LANGUAGE
    }
}

# Open the client using a context manager
def transcribe(path_to_file):
    with BatchClient(settings) as client:
        try:
            job_id = client.submit_job(
                audio=path_to_file,
                transcription_config=conf,
            )
            print(f'job {job_id} submitted successfully, waiting for transcript')

            # Note that in production, you should set up notifications instead of polling.
            # Notifications are described here: https://docs.speechmatics.com/features-other/notifications
            transcript = client.wait_for_completion(job_id, transcription_format='txt')
            # To see the full output, try setting transcription_format='json-v2'.
            return transcript
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                print('Invalid API key - Check your API_KEY at the top of the code!')
            elif e.response.status_code == 400:
                print(e.response.json()['detail'])
            else:
                raise e

def speak_text(text):
    engine = pyttsx3.init()
    # engine.setProperty('voice', 'com.apple.voice.compact.fr-FR.Thomas')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 30)
    engine.say(text)
    engine.runAndWait()
