from dotenv import load_dotenv
import os 
from utils import Operation,Language,pipelineId
import requests
from typing import Optional
import tempfile
import base64
load_dotenv()
class ConfigPipeline:
    def __init__(self):
        assert os.getenv("bhashini_api_key") != None , "Bhashini API key not found"
        assert os.getenv("bhashini_userid") != None , "Bhashini User ID not found"

        self.__api_key = os.getenv("bhashini_api_key")
        self.__userid = os.getenv("bhashini_userid")
        self.endpoint = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        self.isConfigured = False
        self.__callbackUrl = None
        self.__authorizationName = None
        self.__authorizationValue = None
        self.__serviceId = None
        self.__operation = None
    def config(self,operation:Operation,sourceLanguage:Language,pipeline_id:pipelineId,targetLanguage:Optional[Language]=None):

        assert operation in Operation, "Invalid operation"
        assert sourceLanguage is None or sourceLanguage  in Language, "Invalid source language"
        assert pipeline_id is None or pipeline_id  in pipelineId, "Invalid pipeline id"
        self.__operation = operation
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage or None
        body = {
            "pipelineTasks":[],
            "pipelineRequestConfig":{
                "pipelineId":pipeline_id.value
            }
        }
        if operation == Operation.translation:
            assert targetLanguage is  None or targetLanguage  in Language, "Target language is required for translation"
            body["pipelineTasks"].append({
                "taskType" : operation.value,
                "config":{
                    "language":
                    {
                    "sourceLanguage":sourceLanguage.value,
                    "targetLanguage":targetLanguage.value
                    }
                }
            })  
        if operation == Operation.asr:
            body["pipelineTasks"].append({
                "taskType" : operation.value,
                "config":{
                    "language":
                    {
                    "sourceLanguage":sourceLanguage.value
                    }
                }
            })
        if operation == Operation.tts:
            body["pipelineTasks"].append({
                "taskType" : operation.value,
                "config":{
                    "language":
                    {
                    "sourceLanguage":sourceLanguage.value
                    }
                }
            })
        headers = {
            "Content-Type":"application/json",
            "userID":self.__userid,
            "ulcaApiKey":self.__api_key,
            "Cache-Control":"no-cache"
        }

        response = requests.post(self.endpoint,json=body,headers=headers)

        if response.status_code == 200:
            formatted_response = response.json()
            # print(formatted_response)
            self.__serviceId = formatted_response["pipelineResponseConfig"][0]["config"][0]["serviceId"]
            self.__modelId = formatted_response["pipelineResponseConfig"][0]["config"][0]["modelId"]
            self.__callbackUrl = formatted_response["pipelineInferenceAPIEndPoint"]["callbackUrl"]
            self.__authorizationName = formatted_response["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]
            self.__authorizationValue = formatted_response["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]
            if operation == Operation.tts:
                self.supportedVoices = formatted_response["pipelineResponseConfig"][0]["config"][0]["supportedVoices"]
            self.isConfigured = True

        else:
            raise Exception("Error in configuring pipeline")
        
    def get_service_id(self):
        return self.__serviceId
    def get_model_id(self):
        return self.__modelId
    def get_callback_url(self):
        return self.__callbackUrl
    def get_authorization(self):
        return {
            self.__authorizationName:self.__authorizationValue
        }
    def get_operation(self):
        return self.__operation
    def get_supported_voices(self):
        if self.get_operation() == Operation.tts:
            return self.supportedVoices
        else:
            return "other operation does not have supported voices"
    def get_all(self):
        return {
            "serviceId":self.__serviceId,
            "modelId":self.__modelId,
            "callbackUrl":self.__callbackUrl,
            "authorization":self.get_authorization()
        }
    
class Pipeline:
    def __init__(self,config:ConfigPipeline):
        assert config.isConfigured == True, "Pipeline not configured"
        self.__config = config
        self.__serviceId = config.get_service_id()
        self.__modelId = config.get_model_id()
        self.__callbackUrl = config.get_callback_url()
        self.__authorization = config.get_authorization()
    def write_temp(self,content):
        folder = tempfile.mkdtemp()
        output_file= f"{folder}/output.wav"
        decode = base64.b64decode(content)
        with open(output_file,"wb") as f:
            f.write(decode)
        return output_file
    def execute(self,text:Optional[str]=None,audioContent:Optional[str]=None):
        body = {
          "pipelineTasks":[]
        }
        auth = tuple(self.__config.get_authorization().items())[0]
        # print(auth)
        headers = {
            "Content-Type":"application/json",
            "Cache-Control":"no-cache",
            auth[0]: auth[1]
        }
        if self.__config.get_operation() == Operation.tts:
            assert text is not None, "Text is required for translation"
            body["pipelineTasks"].append({
                "taskType":self.__config.get_operation().value,
                "config":{
                    "language":{
                        "sourceLanguage":self.__config.sourceLanguage.value,
                    },
                    "serviceId":self.__config.get_service_id(),
                    "gender":"female"
                }
            })
            body["inputData"]={
                "input":[
                    {
                        "source":text
                    }
                ]
            }
            response = requests.post(self.__callbackUrl,json=body,headers=headers)
            formatted_response = response.json()
            # return formatted_response
            saved_path = self.write_temp(formatted_response["pipelineResponse"][0]["audio"][0]["audioContent"])
           
            return saved_path
        else:
            raise NotImplementedError("Only TTS is implemented")
        