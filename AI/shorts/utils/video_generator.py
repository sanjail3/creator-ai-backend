import json
from ..prompts.video_generator_prompt import VIDEO_PROMPT
from video_syntax import SHORT_VIDEO_WITH_IMAGES
from script_generator import ScriptGenerator
from audio_generator import AudioGenerator
from image_generator import ImageGenerator
from ..editor.editor import VideoEditor
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


load_dotenv()


class VideoGenerator:
    def __init__(
        self,
        prompt=VIDEO_PROMPT,
        syntax=SHORT_VIDEO_WITH_IMAGES,
    ):

        self.prompt = prompt
        self.syntax = syntax
        self.languages = ["en", "hi"]

    def get_languages(self):

        return self.languages


    def get_font_list(self):

        video_converter = VideoEditor()
        return video_converter.get_font_list()

    def generate_script(
        self,
        topic,
        duration="30s",
        tone="casual",
        language="en",
        instructions="",
        num_of_images=5,
    ):

        try:
            api_key = os.getenv("OPENAI_API_KEY")
            text_creator = ScriptGenerator(api_key=api_key)

            print("Generating script...")
            generated_script = text_creator.generate(
                self.prompt,
                topic=topic,
                duration=duration,
                tone=tone,
                language=language,
                instructions=instructions,
                num_of_images=num_of_images,
                syntax=self.syntax,
            )
            print(generated_script)

            try:
                generated_script = generated_script.replace("```json", "")
                generated_script = generated_script.replace("```", "")
            except Exception as e:
                raise Exception(
                    "Error occurred while removing json code block: " + str(e)
                )

            generated_script = json.loads(generated_script)
            video_title = generated_script["video_title"]
            video_description = generated_script["video_description"]
            video_script_json = json.dumps(generated_script["scripts"])
            script_parts = []
            image_prompts = []

            for key, script in generated_script["scripts"].items():
                script_parts.append(script["text"])
                image_prompts.append(script["image"])

            video_script = {
                "video_title": video_title,
                "video_description": video_description,
                "video_script": video_script_json,
                "script_parts": script_parts,
                "image_prompts": image_prompts,
            }
            print(video_script)

            return video_script



        except Exception as e:
            print(e)
            return None

    def generate_audio(
        self,
        script_parts=[],
        output_file="audio.wav",

    ):

        audio_ai = AudioGenerator()
        script = ". ".join(script_parts)
        asyncio.run(audio_ai.generate(prompt=script,
                                      output_file=output_file))

        print(script)

    def generate_images(self, image_prompts=[], image_path="images"):

        try:
            image_ai = ImageGenerator(api_key=api_key)
            image_paths = []
            for i, prompt in enumerate(image_prompts):
                path = os.path.join(image_path, f"{i}.png")
                path = os.path.abspath(path)
                try:
                    image_ai.generate(
                        prompt=prompt,
                        output_file=path,
                    )
                    image_paths.append(path)
                except Exception as e:
                    print(f"Error generating image: {e}")
                    continue
            return image_paths
        except Exception as e:
            print(e)
            return None

    def generate_subtiles(self, audio_path, word_timestamps=True):

        audio_ai = AudioGenerator()
        subs = audio_ai.get_transcription(audio_path, word_timestamps)
        print(subs)
        return subs

    def generate_video(
        self,
        video_dir,
        audio_path,
        output_file="video.mp4",

        subtitle_options={
            "font_color": "yellow",
            "font_size": 60,
            "font": "liberation-sans",
        },
    ):

        try:
            video_editor = VideoEditor()

            # subtitles = self.generate_subtiles(audio_path)
            subtitles = None
            video_path = video_editor.create_video(
                video_dir,subtitle_options=subtitle_options
            )

            return video_path
        except Exception as e:
            print(e)
            return None
