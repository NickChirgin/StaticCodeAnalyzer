code = 'S001'
message = 'Too long'
with open(input(), 'r') as f:
    for i, value in enumerate(f.readlines()):
        if len(value) >= 79:
            print(f"Line {i+1}: {code} {message}")