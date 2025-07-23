import json
import sys
from json2xml import json_to_xml

# Usage: python debug_json2xml.py <combinations.jsonl> <tester.xml> <output.xml> [entry_index]
# entry_index: which line to use from combinations.jsonl (default: 0)

if len(sys.argv) < 4:
    print("Usage: python debug_json2xml.py <combinations.jsonl> <tester.xml> <output.xml> [entry_index]")
    sys.exit(1)

jsonl_path = sys.argv[1]
tester_xml = sys.argv[2]
output_xml = sys.argv[3]
entry_index = int(sys.argv[4]) if len(sys.argv) > 4 else 0

with open(jsonl_path) as f:
    lines = f.readlines()
    if entry_index >= len(lines):
        print(f"Entry index {entry_index} out of range. File has {len(lines)} lines.")
        sys.exit(1)
    params = json.loads(lines[entry_index])

print(f"Using entry {entry_index} from {jsonl_path}:")
print(json.dumps(params, indent=2))

print(f"Calling json_to_xml with {tester_xml} -> {output_xml}")
json_to_xml(params, tester_xml, output_xml)
print("Done.")
