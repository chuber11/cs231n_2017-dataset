
for file in *.opus
do

if [ -f "${file%.opus}.seg" ]; then
    continue
fi

python audioclient/client.py -i ffmpeg -f "$file" --asr-kv version=offline --asr-kv segmenter=SHAS --ffmpeg-speed -1 --output-file "${file%.mp3}.seg" --no-textsegmenter --asr-kv dummy_asr=True --asr-kv max_segment_length=10

done

