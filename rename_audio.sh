
for f in *.opus
do
    f2=`echo $f | sed "s/ /_/g" | sed "s/｜/_/g"`
    mv "$f" "$f2"
done
