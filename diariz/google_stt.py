"""
CSCE 4201 AI project
"""

from google.cloud import speech_v1p1beta1 as speech


def main():
    speech_file = "C:\\AIProjectAudioFiles\\14DCS 3-19-18_Shortened.mp3"
    # upload_blob("AlzheimersAudio",speech_file,"14DCS 3-19-18_Shortened.mp3")
    results = transcribe_gcs('gs://ai-project-audio-files/14DCS 3-19-18_Shortened.mp3')

    with open('output.txt', 'w+') as f:
        if results:
            f.write(results.to_json())


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
    response = operation.result(timeout=100)
    if response:
        print("Success")
    #print(response)

    return response


if __name__ == "__main__":
    main()
