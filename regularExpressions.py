import re

# List of SQL injection patterns
sql_injection_patterns = [
    r"union\s+select",  # UNION SELECT
    r"or\s+1=1",        # OR 1=1
    r"order\s+by",      # ORDER BY
    r"--",              # SQL comment
    r"drop\s+table",    # DROP TABLE
    r"insert\s+into",   # INSERT INTO
    r"select\s+\*",     # SELECT *
    r"\'\s+or",         # ' OR
    r"\bwhere\b.*\b(or|and)\b.*="   # WHERE statement
    r"\bupdate\b.*\bset\b.*(\bwhere\b.*(like|or|and|=))"  # UPDATE statement
    r";.*\b(drop|select|insert|delete|update)\b"  # Multiline statement
    r"\blike\b.*['\"].*['\"]"  # Catches any LIKE keyword in input
]

# Function to detect SQL injection
def is_sql_injection(input_string):
    for pattern in sql_injection_patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return True
    return False
