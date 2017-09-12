 #!/bin/bash

draw_badges() {
    echo "Drawing badges $1 ..."
    python ./pybadges.py -i badges-$1.csv -o badges-$1.pdf -b badges-$1.png
    python ./download-qrcodes.py -i badges-$1.csv -o ./qrcodes
    python ./pybadges_back.py -i badges-$1.csv -o badges-$1-back.pdf -b badges-back.png -q ./qrcodes
    echo
}

draw_badges "staff"
draw_badges "sponsor"
draw_badges "speaker"
draw_badges "public"
