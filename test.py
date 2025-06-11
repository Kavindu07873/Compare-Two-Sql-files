import re
import os

def extract_entities(sql_file):
    if not os.path.exists(sql_file):
        print(f"❌ File not found: {sql_file}")
        return {'tables': [], 'views': [], 'procedures': [], 'triggers': []}

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

def compare_tables(tables1, tables2):
    set1 = set(tables1)
    set2 = set(tables2)
    common = sorted(list(set1 & set2))
    only_in_1 = sorted(list(set1 - set2))
    only_in_2 = sorted(list(set2 - set1))

    print(f"\n=== Table Comparison ===")
    print(f"Total tables in File 1: {len(tables1)}")
    print(f"Total tables in File 2: {len(tables2)}")
    print(f"Common tables ({len(common)}): {common if common else 'None'}")
    print(f"\n=================================")
    print(f"Only in File 1 ({len(only_in_1)}): {only_in_1 if only_in_1 else 'None'}")
    print(f"\n=================================")
    print(f"Only in File 2 ({len(only_in_2)}): {only_in_2 if only_in_2 else 'None'}")

# Update paths if needed
file1 = 'unicloud_multiple_version-dump-2025-05-29.sql'
file2 = 'unicloud_ijse_prod_backup_2025-06-11_07-56-00.sql'

entities1 = extract_entities(file1)
entities2 = extract_entities(file2)


print("_____________________________________________")


print_entities("File 1", entities1)

print("_____________________________________________")

print_entities("File 2", entities2)


# Compare tables
compare_tables(entities1['tables'], entities2['tables'])
