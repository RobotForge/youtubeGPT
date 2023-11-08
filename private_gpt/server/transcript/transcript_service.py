
import re
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, AnyStr

from injector import inject, singleton


from private_gpt.paths import local_data_path
from youtube_transcript_api.formatters import TextFormatter
from pydantic import BaseModel, Field



logger = logging.getLogger(__name__)





@singleton
class TranscriptService:
    @inject
    def __init__(self, url: str) -> None:
        self.url = url
        

    def extract_id(self) -> str:
        # Regular expression pattern to match YouTube video URLs
        pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+(v=|e/|embed/|watch\?v=|watch\?feature=player_embed&v=|&v=)?([^&=%\?]{11})'

        # Use regex to find the video ID
        match = re.search(pattern, self.url)
        
        if match:
            video_id = match.group(6)
            return video_id
        else:
            return None

    def get_youtube_transcript_to_text(self,youtube_video_id:str):
        try:
            output_file="local_data/"+youtube_video_id+".txt"
            # Get the transcript for the YouTube video
            #transcript = YouTubeTranscriptApi.get_transcript(youtube_video_id)
            transcript_list = YouTubeTranscriptApi.list_transcripts(youtube_video_id)
            transcript = transcript_list.find_manually_created_transcript(['en-US'])
            transcript = transcript.fetch()

            formatter = TextFormatter()
            text_formatted = formatter.format_transcript(transcript)
            print(text_formatted)
           
            # Create and write the transcript to a text file
            with open(output_file, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_formatted )
            
            print(f"Transcript has been successfully extracted and saved as '{output_file}'.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return output_file
    
