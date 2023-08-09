
for seg in shas_output/*.seg
do
    seg2=${seg#shas_output/}
    cat "$seg" | tail -n+3 | head -n-1 | cut -d" " -f3 | sed 's/:$//g' | awk -v seg="${seg2%.seg}" -F"-" '{print seg"_"NR" /project/OML/chuber/2023/data/cs231n_2017-dataset/audio/"seg".wav "$1" "$2}' > "segfiles/${seg2%.seg}.seg.aligned"
done
