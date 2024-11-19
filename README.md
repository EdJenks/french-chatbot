# french-chatbot

A project that utilises the OpenAI GPT-4 model API and Speechmatics speech to text transcription API to create conversations in French.

Users will need to obtain an API key for both of the above APIs from the respective websites.

[Speechmatics' research](https://www.speechmatics.com/company/articles-and-news/our-new-unified-speech-translation-api) into dialectic and multilingual transcription has proved to produce some of the most accurate models/tools on the market on orders of magnitude less data, and was therefore chosen for this task.

OpenAI at the time of development produce the most realistic conversational AIs that exist, hence was chosen for the chatbot's responses.

## Talking with Pierre

A non-exhaustive but essenital list of libraries and the versions used is included in the requirements.txt file. The user should install these in the projects virtual environment, and then can run the app simply by calling pierre.py and interacting with the chatbot using the terminal. The code has been commented where possible to give developers an idea of how the app works, and allow for individual customisation where desired.

## Further improvements

Further iterations of this project include fine tuning existing models on labeled data of [CEFR score](https://tracktest.eu/english-levels-cefr/#:~:text=How%20many%20language%20levels%20are,%2DC2%20(Proficient%20User).) examples, and estimating the user's french level using this based on their responses.
