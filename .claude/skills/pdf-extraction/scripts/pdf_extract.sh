#!/bin/bash
# PDF extraction utilities using poppler's pdftotext
# Usage: ./pdf_extract.sh <command> <file> [args]

COMMAND=$1
FILE=$2

case $COMMAND in
  page)
    # Extract specific page (arg: page number)
    PAGE=$3
    pdftotext -f "$PAGE" -l "$PAGE" -layout "$FILE" -
    ;;
  range)
    # Extract page range (args: start end)
    START=$3
    END=$4
    pdftotext -f "$START" -l "$END" -layout "$FILE" -
    ;;
  first)
    # Extract first N pages (default: 3)
    N=${3:-3}
    pdftotext -f 1 -l "$N" -layout "$FILE" -
    ;;
  all)
    # Extract entire PDF (use sparingly!)
    pdftotext -layout "$FILE" -
    ;;
  search)
    # Search for text, return matching lines with line numbers
    QUERY=$3
    pdftotext "$FILE" - | grep -in "$QUERY"
    ;;
  count)
    # Count occurrences of a query
    QUERY=$3
    pdftotext "$FILE" - | grep -ic "$QUERY"
    ;;
  search-pages)
    # Find which pages contain a query (checks up to 50 pages)
    QUERY=$3
    MAX_PAGES=50
    for ((i=1; i<=MAX_PAGES; i++)); do
      CONTENT=$(pdftotext -f "$i" -l "$i" "$FILE" - 2>/dev/null)
      # Stop if page is empty (past end of document)
      [ -z "$CONTENT" ] && break
      if echo "$CONTENT" | grep -qi "$QUERY"; then
        echo "Page $i"
      fi
    done
    ;;
  *)
    echo "Commands: page, range, first, all, search, count, search-pages"
    exit 1
    ;;
esac
