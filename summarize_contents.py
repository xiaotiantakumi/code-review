import os
import sys

# 除外するファイルやディレクトリのパターン
EXCLUDE_PATTERNS = {'.gitignore', '.venv', 'venv', '.git', '.vscode', 'node_modules', 'package-lock.json'}

def is_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            for chunk in file:
                if b'\0' in chunk:
                    return True
        return False
    except Exception as e:
        print(f"Error checking if file is binary: {e}")
        return True

def should_exclude(file_path):
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_path:
            return True
    return False

def summarize_directory_contents(dir_path, output_file='summary.txt'):
    with open(output_file, 'w', encoding='utf-8') as summary_file:
        for root, dirs, files in os.walk(dir_path):
            # ディレクトリの除外
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            for file in files:
                file_path = os.path.join(root, file)
                if not is_binary(file_path) and not should_exclude(file_path):
                    summary_file.write(f'{file_path}\n```\n')
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            summary_file.write(content)
                    except UnicodeDecodeError:
                        summary_file.write('Error: Could not decode file\n')
                    summary_file.write('\n```\n\n')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python summarize_contents.py [directory_path]")
    else:
        dir_path = sys.argv[1]
        summarize_directory_contents(dir_path)
        print(f'summarized in summary.txt')
