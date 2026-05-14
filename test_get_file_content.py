from functions.get_file_content import get_file_content

lorem_result = get_file_content("calculator", "lorem.txt")
print(f'lorem.txt length: {len(lorem_result)}')
print(f'lorem.txt truncated: {'truncated' in lorem_result}')

print(get_file_content("calculator", "main.py"))

print(get_file_content("calculator", "pkg/calculator.py"))

print(get_file_content("calculator", "/bin/cat"))

print(get_file_content("calculator", "pkg/does_not_exist.py"))