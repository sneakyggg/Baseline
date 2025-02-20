#!/usr/bin/env python3
import os
import sys

def parse_stats_file(filepath):
    """
    Parse the given stats file to extract:
      1) real_map_size (from the line "real_map_size: XYZ")
      2) The covered-blocks value from the last line that starts with '['
    Returns both as strings.
    """
    real_map_size = None
    last_covered_blocks = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Extract real_map_size from a line like "real_map_size: 3038"
            if line.startswith("real_map_size:"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    real_map_size = parts[1].strip()

            # Process lines that start with '[' (data lines)
            elif line.startswith("["):
                fields = [field.strip() for field in line.split(",")]
                if len(fields) >= 3:
                    last_covered_blocks = fields[2]

    return real_map_size, last_covered_blocks


def main(parent_dir):
    """
    Traverse the parent directory, parse the stats file in each sub-directory,
    compute coverage = (covered / map_size), and build a mapping from the sub-directory
    name to (map_size, covered, coverage). Finally, sort the mapping by coverage.
    """
    results = {}

    # Iterate through each entry in the parent directory
    with os.scandir(parent_dir) as entries:
        for entry in entries:
            if entry.is_dir():
                stats_file = os.path.join(entry.path, "perf_periodic.txt")

                if os.path.isfile(stats_file):
                    map_size_str, covered_str = parse_stats_file(stats_file)
                    try:
                        map_size = int(map_size_str)
                        covered = int(covered_str)
                        # Avoid division by zero
                        coverage = covered / map_size if map_size != 0 else 0.0
                    except (ValueError, TypeError):
                        map_size, covered, coverage = 0, 0, 0.0
                else:
                    map_size, covered, coverage = "N/A", "N/A", 0.0

                results[entry.name] = (map_size, covered, coverage)

    # Sort results by coverage value (lowest to highest)
    sorted_results = sorted(results.items(), key=lambda item: item[1][2])

    # Print the sorted results
    for subdir, (size, covered, coverage) in sorted_results:
        print(f"Sub-directory: {subdir} - block-coverage: {coverage:.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} /path/to/parent_directory")
        sys.exit(1)

    parent_directory = sys.argv[1]
    main(parent_directory)
