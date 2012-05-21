#!/bin/sh

if [ $# -ne 3 ]
then
    echo "Usage: rip.sh /path/to/monster.sbin /path/to/kaomado.kao output-dir"
    exit 1
fi

monster=$1
kaomado=$2
output_dir=$3

# Rip the Sky sprites (there are way more of those)
echo 'Ripping Sky...'
$(dirname $0)/kaomado.py $kaomado $output_dir

# Rip the Blue sprites to a subdirectory
echo 'Ripping Blue...'
$(dirname $0)/kaomado.py $monster $output_dir/red-blue

# Compare all the Blue sprites to their Sky equivalents; keep only the Blue
# ones that differ
echo 'Comparing and pruning...'
for file in $(find $output_dir/red-blue -name '*.png' -printf '%P\n')
do
    if cmp -s $output_dir/$file $output_dir/red-blue/$file
    then
        rm $output_dir/red-blue/$file
    fi
done

# Make duplicates for named default forms
echo 'Copying default forms...'
for form in 201-a 386-normal 412-plant 413-plant 421-overcast 422-west \
            423-west 487-altered 492-land
do
    id=${form%%-*}
    for file in $(find $output_dir -name $form.png)
    do
        cp $file $(dirname $file)/$id.png
    done
done
