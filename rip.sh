#!/bin/sh
# Run the ripping script
./kaomado.py

# Make duplicates for named default forms
for form in 201-a 386-attack 412-plant 413-plant 421-overcast 422-west \
            423-west 487-altered 492-land
do
    id=$(echo $form | sed 's/-.*//')  # dash has no <<<
    for file in $(find /var/tmp/kaomado -name $form.ppm)
    do
        cp $file $(dirname $file)/$id.ppm
    done
done
