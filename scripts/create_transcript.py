
from youtube_transcript_api import YouTubeTranscriptApi



def get_youtube_transcript_to_text(youtube_video_id, output_file="../local_data/transcript.txt"):
    try:
        # Get the transcript for the YouTube video
        transcript = YouTubeTranscriptApi.get_transcript(youtube_video_id)
        
        # Create and write the transcript to a text file
        with open(output_file, 'w', encoding='utf-8') as text_file:
            for entry in transcript:
                text = entry['text']
                print(text)
                text_file.write(text + '\n')
        
        print(f"Transcript has been successfully extracted and saved as '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Example usage
youtube_video_url = "2eWuYf-aZE4"
get_youtube_transcript_to_text(youtube_video_url)