#!/bin/sh

if [ $# -ne 2 ]
then
    echo "Usage: rip.sh /path/to/kaomado.kao output-dir"
    exit 1
fi

# Run the ripping script
$(dirname $0)/kaomado.py $*

# Make duplicates for named default forms
for form in 201-a 386-normal 412-plant 413-plant 421-overcast 422-west \
            423-west 487-altered 492-land
do
    id=${form%%-*}
    for file in $(find $2 -name $form.png)
    do
        cp $file $(dirname $file)/$id.png
    done
done
