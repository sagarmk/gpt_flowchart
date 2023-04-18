import configparser
import os
import openai

class GPT:

    def __init__(self):

        # Get the path of the config file
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        # Configurations
        openai.api_key = self.config.get('gpt', 'openai_key')
        self.model_name = self.config.get('gpt','model_name')
        self.model_list = openai.Model.list().data
        self.models_available = [models.id for models in self.model_list]


    def request_gpt(self, system, query):
        """ query open ai chat completion """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": query},
                {"role":"assistant", "content": "graphviz code:"}
            ],
            temperature=0

        )

        if 'choices' in response:
            return response['choices'][0]['message']
        else:
            return {"content":"", "role":"assistant"}


