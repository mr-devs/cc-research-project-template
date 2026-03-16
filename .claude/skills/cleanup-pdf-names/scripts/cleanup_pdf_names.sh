#!/bin/bash
#
# cleanup_pdf_names.sh - Clean up PDF filenames for consistency
#
# Transformations:
#   - Spaces → underscores (_)
#   - Em dashes (—) and en dashes (–) → regular hyphens (-)
#   - Smart quotes (' ' " ") → regular quotes (' ")
#   - Common accented characters → ASCII equivalents
#
# Usage: ./cleanup_pdf_names.sh <directory>
#

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    echo "  Recursively cleans up PDF filenames in the specified directory"
    exit 1
fi

TARGET_DIR="$1"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist"
    exit 1
fi

# Counter for renamed files
renamed_count=0
skipped_count=0

# Find all PDF files recursively
while IFS= read -r -d '' filepath; do
    dir=$(dirname "$filepath")
    filename=$(basename "$filepath")

    # Apply transformations to filename
    new_filename="$filename"

    # Replace spaces with underscores
    new_filename="${new_filename// /_}"

    # Replace em dash (—) with hyphen
    new_filename=$(echo "$new_filename" | sed 's/—/-/g')

    # Replace en dash (–) with hyphen
    new_filename=$(echo "$new_filename" | sed 's/–/-/g')

    # Replace smart single quotes with regular single quote
    new_filename=$(echo "$new_filename" | sed "s/'/'/g; s/'/'/g")

    # Replace smart double quotes with regular double quote
    new_filename=$(echo "$new_filename" | sed 's/"/"/g; s/"/"/g')

    # Replace common accented characters with ASCII equivalents
    new_filename=$(echo "$new_filename" | sed '
        s/á/a/g; s/à/a/g; s/â/a/g; s/ä/a/g; s/ã/a/g; s/å/a/g
        s/Á/A/g; s/À/A/g; s/Â/A/g; s/Ä/A/g; s/Ã/A/g; s/Å/A/g
        s/é/e/g; s/è/e/g; s/ê/e/g; s/ë/e/g
        s/É/E/g; s/È/E/g; s/Ê/E/g; s/Ë/E/g
        s/í/i/g; s/ì/i/g; s/î/i/g; s/ï/i/g
        s/Í/I/g; s/Ì/I/g; s/Î/I/g; s/Ï/I/g
        s/ó/o/g; s/ò/o/g; s/ô/o/g; s/ö/o/g; s/õ/o/g; s/ø/o/g
        s/Ó/O/g; s/Ò/O/g; s/Ô/O/g; s/Ö/O/g; s/Õ/O/g; s/Ø/O/g
        s/ú/u/g; s/ù/u/g; s/û/u/g; s/ü/u/g
        s/Ú/U/g; s/Ù/U/g; s/Û/U/g; s/Ü/U/g
        s/ñ/n/g; s/Ñ/N/g
        s/ç/c/g; s/Ç/C/g
        s/ß/ss/g
    ')

    # Check if filename changed
    if [ "$filename" != "$new_filename" ]; then
        old_path="$filepath"
        new_path="$dir/$new_filename"

        # Check if target already exists
        if [ -e "$new_path" ]; then
            echo "SKIP: '$old_path' -> target already exists: '$new_path'"
            ((skipped_count++))
        else
            mv "$old_path" "$new_path"
            echo "RENAMED: '$filename' -> '$new_filename'"
            ((renamed_count++))
        fi
    fi
done < <(find "$TARGET_DIR" -type f -name "*.pdf" -print0)

echo ""
echo "Summary:"
echo "  Renamed: $renamed_count files"
echo "  Skipped: $skipped_count files"
