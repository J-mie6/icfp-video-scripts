# Convert a logo (in png format) into one suitable for a titlecard
convert $1 -gravity center -background 'rgba(0,0,0,0)' -extent 1920x1080  logo/icfp-titlecard.png
