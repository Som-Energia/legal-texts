#!/bin/bash

error() { echo -e '\033[31;1m'"$@"'\033[0m' >&2; }
warn() { echo -e '\033[33;1m'"$@"'\033[0m' >&2; }
step() { echo -e '\033[34;1m'"$@"'\033[0m' >&2; }
die() { error "$@"; exit -1; }

process() {
	lang=$(echo "$1" | sed 's/.*\([A-Z][A-Z]\).*/\1/' | tr '[:upper:]' '[:lower:]')
	[ -z "$lang" ] && die "Uppercase lang code not detected in the input file"
	[ "$lang" = 'ca' ] || 
	[ "$lang" = 'es' ] || 
	[ "$lang" = 'eu' ] || 
	[ "$lang" = 'ga' ] || 
	[ "$lang" = 'gl' ] || die "'$lang' not a supported language"
	# fix lang code for ga -> gl
	[ "$lang" = 'ga' ] && lang='gl'

	step "Processing language $lang"

    pandoc "$1" -o "$lang"_tmp.md --columns 80000 -t gfm-raw_html  
    touch $lang.md
    python toc-generator.py

    rm "$lang"_tmp.md

	# Break paragraphs by phrases
	sed -i 's/\([^0-9]\.\) /\1\n/g' $lang.md
	# Fix subscripts
	sed -i 's/_(\([^)][^)]*\))/~\1~/g' $lang.md
}

for a in "$@"; do
	process "$a"
done


