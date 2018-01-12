# Convert a logo ($1: in png format) into one suitable for a titlecard
# with resolution $2 (in WWWWxHHHH format)
convert $1 -gravity center -background 'rgba(0,0,0,0)' -extent $2  logo/icfp-titlecard-$2.png
