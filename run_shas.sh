
filetype=opus

for file in *.$filetype
do

if [ -f "shas_output/${file%.$filetype}.seg" ]; then
    continue
fi

python audioclient/client.py -i ffmpeg -f "$file" --asr-kv version=offline --asr-kv segmenter=SHAS --ffmpeg-speed -1 --output-file "shas_output/${file%.$filetype}.seg" --no-textsegmenter --asr-kv dummy_asr=True --asr-kv max_segment_length=10 --no-logging

done

