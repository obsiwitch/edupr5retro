#!/bin/sh

dnewlines() { cat -s ; }
dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }
dcomments() { sed '/^\s*#/d' ; }
decorate() { cat ; echo ; }

mkdir -p 'out'

out1='out/retro.doc.py'
cat 'src/constants.py' | dnewlines | decorate > "$out1"
for f in 'src/math.py' \
         'src/rect.py' \
         'src/image.py' \
         'src/font.py' \
         'src/window.py' \
         'src/events.py' \
         'src/sprite.py' \
         'src/vector.py'
do cat "$f" | dimports | dnewlines | decorate >> "$out1"; done

out2='out/retro.py'
cat "$out1" | dcomments | dnewlines > "$out2"
