
for seg in *.seg
do
    cat "$seg" | tail -n+3 | head -n-1 | cut -d" " -f3 | sed 's/:$//g' | awk -v seg="${seg%.seg}" -F"-" '{print seg"_"NR" "seg".opus "$1" "$2}' > "segfiles/${seg%.seg}.seg.aligned"
done
