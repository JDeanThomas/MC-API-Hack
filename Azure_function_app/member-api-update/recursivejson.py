#!/usr/bin/env python3
import sys
import json

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results


if __name__ == '__main__':
    """ 
    Run file as standalone script
    """
    if sys.stdin.isatty():
        filename = sys.argv[-2]
        key = sys.argv[-1]
        extract_values(filename, key)
