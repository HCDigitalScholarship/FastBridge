import os, sys
# https://www.geeksforgeeks.org/python-import-from-parent-directory/
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

import random
import json
from pathlib import Path
import json
from language_texts import greek_titles, latin_titles

section_map_file = Path(parent) / "sections.json"
if section_map_file.exists():
    with section_map_file.open() as f:
        section_maps = json.load(f)
    latin_section_map = section_maps.get("Latin", {})
    greek_section_map = section_maps.get("Greek", {})
else:
    print("section.json file not found. using empty section map with start and end as defaults.")
    latin_section_map = {}
    greek_section_map = {}

# Reverse the value map to get readable names for test generation
greek_readable_titles = {v.split("_")[0]: k for k, v in greek_titles.items()}
latin_readable_titles = {v.split("_")[0]: k for k, v in latin_titles.items()}

if not latin_section_map:
    latin_section_map = {title: {"start": "start", "end": "end"} for title in latin_readable_titles.keys()}

greek_section_map = {title: {"start": "start", "end": "end"} for title in greek_readable_titles.keys()}


def get_start_end(text_name, language):
    section_map = latin_section_map if language == 'Latin' else greek_section_map
    sections = section_map.get(text_name, {})
    numbered_sections = [s for s in sections if s not in ("start", "end")]
    
    if not numbered_sections:
        return "start", "end"
    numbered_sections = sorted(numbered_sections, key=lambda x: int(x) if x.isdigit() else float('inf'))
    start_idx = random.randint(0, len(numbered_sections) - 2)
    end_idx = random.randint(start_idx + 1, len(numbered_sections) - 1)
    return numbered_sections[start_idx], numbered_sections[end_idx]


# Generate tests for /oracle/ and /select/
def generate_tests(concat_val=20):
    tests = []
    select_tests, oracle_tests = [], []

    for language in ['Latin', 'Greek']:
        section_map = latin_section_map if language == 'Latin' else greek_section_map
        titles = latin_readable_titles if language == 'Latin' else greek_readable_titles
        other_texts = list(titles.values())
        for internal_name, text_name in titles.items():
            readable_name = internal_name.split('_')[0]
            start, end = get_start_end(readable_name, language)

            # Oracle Route
            section_size = random.randint(3, 9)
            oracle_url = f"/oracle/{language}/result/{text_name}/{start}/{end}/1/{section_size}/{random.choice(other_texts)}/start-end"
            oracle_tests.append(f"def test_oracle_{text_name.replace('-', '_')}():\n    response = client.get(\"{oracle_url}\")\n    assert response.status_code == 200")

            # Select Route 1 - long form
            select_url1 = f"/select/{language}/result/{text_name}/{start}-{end}/include/{random.choice(other_texts)}/start-end/non_running/"
            select_tests.append(f"def test_select_full_{text_name.replace('-', '_')}():\n    response = client.get(\"{select_url1}\")\n    assert response.status_code == 200")

            # Select Route 2 - short form
            select_url2 = f"/select/{language}/result/{text_name}/{start}-{end}/non_running/"
            select_tests.append(f"def test_select_simple_{text_name.replace('-', '_')}():\n    response = client.get(\"{select_url2}\")\n    assert response.status_code == 200")

        # Generate tests for concatenated texts
        for _ in range(concat_val):
                concat_texts = random.sample(other_texts, k=2)
                original_titles = latin_titles if language == 'Latin' else greek_titles
                t1, t2 = concat_texts
                s1, e1 = get_start_end(original_titles[t1].split('_')[0], language)
                s2, e2 = get_start_end(original_titles[t2].split('_')[0], language)
                
                concat_text = f"{t1}+{t2}"
                concat_starts = f"{s1}+{s2}"
                concat_ends = f"{e1}+{e2}"

                # Select (concatenated)
                concat_url = f"/select/{language}/result/{concat_text}/{concat_starts}-{concat_ends}/non_running/"
                select_tests.append(f"def test_select_concat_{concat_text.replace('-', '_').replace('+', '_')}():\n    response = client.get(\"{concat_url}\")\n    assert response.status_code == 200")

                select_url1 = f"/select/{language}/result/{concat_text}/{concat_starts}-{concat_ends}/include/{random.choice(other_texts)}/start-end/non_running/"
                select_tests.append(f"def test_select_full_concat_{concat_text.replace('-', '_').replace('+', '_')}():\n    response = client.get(\"{select_url1}\")\n    assert response.status_code == 200")

                # Oracle (Concatenated)
                section_size_1 = random.randint(3, 9)
                section_size_2 = random.randint(3, 9)
                oracle_units = "1+1"
                oracle_sizes = f"{section_size_1}+{section_size_2}"
                oracle_url_concat = f"/oracle/{language}/result/{concat_text}/{concat_starts}/{concat_ends}/{oracle_units}/{oracle_sizes}/{random.choice(other_texts)}/start-end"
                oracle_tests.append(
                    f"def test_oracle_concat_{concat_text.replace('-', '_').replace('+', '_')}():\n    response = client.get(\"{oracle_url_concat}\")\n    assert response.status_code == 200"
                )

    return list(set(oracle_tests)), list(set(select_tests))

base_test_imports = '''\
"""Auto-generated test file with absolute imports"""
import os, sys
from fastapi.testclient import TestClient

# Add project root to sys.path in order to import main
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from main import app

client = TestClient(app)
'''

def write_test_file(path: str, test_functions: list[str]):
    full_content = base_test_imports + "\n\n" + "\n\n".join(test_functions)
    Path(path).write_text(full_content)

# Write each test file
oracle_tests_functions, select_tests_functions = generate_tests(concat_val=20)
write_test_file("tests/test_oracle.py", oracle_tests_functions)
write_test_file("tests/test_select.py", select_tests_functions)

