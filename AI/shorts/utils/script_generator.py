
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
default_prompt_template = {
        "template": "Write a blog post on {topic}. Include an introduction, main content, and conclusion.",
        "input_variables": ["topic"]
        }
class ScriptGenerator:
    def __init__(
        self,
        api_key,
        model_name="gpt-3.5-turbo",
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.llm = ChatOpenAI(model_name=self.model_name, api_key=self.api_key)

    def generate(self, prompt_template = default_prompt_template, **kwargs):
        prompt = PromptTemplate(
            template=prompt_template["template"],
            input_variables=prompt_template["input_variables"],
        )
        inputs = {variable: kwargs[variable] for variable in prompt_template["input_variables"]}

        print("Generating prediction")
        try:
            chain = prompt|self.llm|StrOutputParser()
            
            response = chain.invoke(inputs)
        
            return response
        except Exception as e:
            print(e)
            raise Exception("Error occurred during prediction: " + str(e))

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    text_creator = ScriptGenerator(api_key=api_key)
    prompt_template = {
        "template": "Write a blog post on {topic}. Include an introduction, main content, and conclusion.",
        "input_variables": ["topic"]
    }
    result = text_creator.generate(prompt_template, topic="The Future of AI")
    print(result)
