import re
import os

def extract_create_table(sql_file, table_name):
    if not os.path.exists(sql_file):
        print(f"❌ File not found: {sql_file}")
        return None

    with open(sql_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Match the CREATE TABLE block
    pattern = re.compile(
        rf'CREATE TABLE\s+`?{table_name}`?\s*\((.*?)\)\s*ENGINE=',
        re.DOTALL | re.IGNORECASE
    )

    match = pattern.search(content)
    if match:
        return match.group(1)
    return None

def extract_column_names(create_block):
    if not create_block:
        return []

    lines = create_block.strip().split('\n')
    columns = []

    for line in lines:
        line = line.strip().rstrip(',')
        # Skip constraints like PRIMARY KEY, UNIQUE, etc.
        if line.upper().startswith(('PRIMARY KEY', 'UNIQUE KEY', 'KEY', 'CONSTRAINT', 'FOREIGN KEY')):
            continue
        col_match = re.match(r'`(\w+)`', line)
        if col_match:
            columns.append(col_match.group(1))
    return columns

def compare_columns(file1, file2, table_name):
    block1 = extract_create_table(file1, table_name)
    block2 = extract_create_table(file2, table_name)

    cols1 = extract_column_names(block1)
    cols2 = extract_column_names(block2)

    set1 = set(cols1)
    set2 = set(cols2)

    print(f"\n=== Column Comparison for Table: `{table_name}` ===")
    print(f"File 1 Columns ({len(cols1)}): {cols1}")
    print(f"File 2 Columns ({len(cols2)}): {cols2}")

    print(f"\n✅ Common Columns ({len(set1 & set2)}): {sorted(set1 & set2)}")
    print(f"➖ Only in File 1 ({len(set1 - set2)}): {sorted(set1 - set2)}")
    print(f"➕ Only in File 2 ({len(set2 - set1)}): {sorted(set2 - set1)}")

# Set file names
file1 = 'unicloud_multiple_version-dump-2025-05-29.sql'
file2 = 'unicloud_ijse_prod_backup_2025-06-11_07-56-00.sql'
table_name = 'academic_misconduct'

# Compare columns
compare_columns(file1, file2, table_name)
