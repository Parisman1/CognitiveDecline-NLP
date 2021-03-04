from resemblyzer import preprocess_wav, VoiceEncoder
from resemblyzer.hparams import sampling_rate
from pathlib import Path
from demo_utils import interactive_diarization

# DEMO 02: we'll show how this similarity measure can be used to perform speaker diarization
# (telling who is speaking when in a recording).
wav_fpath = Path("audio_data", "1CCC.wav")
wav = preprocess_wav(wav_fpath)

# Cut some segments from single speakers as reference audio
segments = [[0, 8],  [17, 25]]
speaker_names = ["Medical Staff",  "Interviewee"]
speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]

## Compare speaker embeds to the continuous embedding of the interview
encoder = VoiceEncoder("cpu")
print("Running the continuous embedding on cpu, this might take a while...")
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)

# Get the continuous similarity for every speaker. It amounts to a dot product between the
# embedding of the speaker and the continuous embedding of the interview
speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in zip(speaker_names, speaker_embeds)}

## Run the interactive demo
interactive_diarization(similarity_dict, wav, wav_splits)


