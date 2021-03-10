"""
CSCE 4201 AI project
"""

import os
import json
from google.cloud import speech_v1p1beta1 as speech


def main():
    credentials_path = "AlzheimersNLP-1c5bb4f4fb21.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    #uris = ['gs://ai-project-audio-files/14DCS 3-19-18_Shortened.mp3']
    uris = get_uris()
    for filename, uri in uris:
        print(f"working on {uri}")
        results = transcribe_gcs(uri)
        with open('output/' + filename + '.json', 'w+') as f:
            if results:
                try:
                    error = False
                    audio_breakdown = parse_response(results)
                    if audio_breakdown:
                        breakdown_json = json.dumps(audio_breakdown, indent=4, sort_keys=True, default=str)
                        #breakdown_json = json.dumps(audio_breakdown)
                    else:
                        error = True
                        print(f"Error: Empty breakdown for {uri}")
                    if breakdown_json:
                        written = f.write(breakdown_json)
                    else:
                        error = True
                        print(f"Error: No json found for {uri}")
                    if error:
                        print("Writing raw response")
                        written = f.write(results)
                    print(f"{written} for {uri}")
                except Exception as e:
                    print(f"ERROR: {uri}")
                    print(e)
            else:
                print(f"Error: No results for {uri}")


def get_uris():
    done = os.listdir('output')
    for filename in os.listdir("C:\AIProjectAudioFiles"):
        if filename+'.json' not in done:
            yield filename, "gs://ai-project-audio-files/" + filename


def parse_response(response):
    result = []
    try:
        words = response.results[-1].alternatives[0].words
        for word in words:
            result.append({
                "start_time": word.start_time,
                "end_time": word.end_time,
                "word": word.word,
                "speaker_tag": word.speaker_tag
            })
    except Exception as e:
        print(e)
        print(result)
        raise e
    return result


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code="en-US",
        # enable_word_time_offsets=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)
    if response:
        print("Success")
    #print(response)

    return response


if __name__ == "__main__":
    main()
