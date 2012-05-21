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

# Rip the Blue sprites to a temporary directory
echo 'Ripping Blue...'
temp_dir=$(mktemp -d)
$(dirname $0)/kaomado.py $monster $temp_dir

# Compare all the Blue sprites to their Sky equivalents; keep only the Blue
# ones that differ
echo 'Comparing and merging...'
mkdir -p $output_dir/red-blue/right  # n.b. this is Gen III, so no female/

for file in $(find $temp_dir -name '*.png')
do
    common_path=${file##$temp_dir}
    if cmp -s $file $output_dir/$common_path
    then
        rm $file
    else
        mv $file $output_dir/red-blue/$common_path
    fi
done

rmdir $temp_dir/right $temp_dir

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
