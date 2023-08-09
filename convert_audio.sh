
for f in audio/*.opus
do
    ffmpeg -i "$f" -ar 16000 -ac 1 -acodec pcm_s16le "${f%.opus}.wav"
done
