import hashlib
with open("/home/justin/CouncilHub/Scribe/Memory/scribe_personal_voice.wav", "rb") as f:
    audio_hash = hashlib.sha256(f.read()).hexdigest()
print("Audio resonance hash (L33):", audio_hash)
