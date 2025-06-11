import re

def extract_entities(sql_file):
    with open(sql_file, 'r', encoding='utf-8') as file:
        content = file.read()

    tables = re.findall(r'CREATE TABLE\s+`?(\w+)`?', content, re.IGNORECASE)
    views = re.findall(r'CREATE VIEW\s+`?(\w+)`?', content, re.IGNORECASE)
    procedures = re.findall(r'CREATE PROCEDURE\s+`?(\w+)`?', content, re.IGNORECASE)
    triggers = re.findall(r'CREATE TRIGGER\s+`?(\w+)`?', content, re.IGNORECASE)

    return {
        'tables': tables,
        'views': views,
        'procedures': procedures,
        'triggers': triggers
    }

def print_entities(label, entities):
    print(f"\n=== Entities in {label} ===")
    for key, val in entities.items():
        print(f"{key.capitalize()} ({len(val)}): {val if val else 'None'}")

# Replace with full file paths if necessary
file1 = 'unicloud_multiple_version-dump-2025-05-29.sql'
file2 = 'unicloud_ijse_prod_backup_2025-06-11_07-56-00.sql'

entities1 = extract_entities(file1)
entities2 = extract_entities(file2)

print_entities("File 1", entities1)
print_entities("File 2", entities2)
