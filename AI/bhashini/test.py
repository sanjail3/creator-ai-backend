from pipeline import ConfigPipeline,Pipeline
from utils import Operation,Language,pipelineId



if __name__ == "__main__":
    config = ConfigPipeline()
    config.config(operation= Operation.tts,sourceLanguage= Language.english,pipeline_id= pipelineId.MeitY,targetLanguage= Language.hindi)
    pipeline = Pipeline(config)
    path = pipeline.execute(text="women")
    print(path)