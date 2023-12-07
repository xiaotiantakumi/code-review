import os
import sys
import fnmatch
import argparse

# 除外するファイルやディレクトリのパターン
EXCLUDE_PATTERNS = {'.*','**/.*','venv', 'node_modules', 'package-lock.json'}

def read_gitignore(gitignore_path, base_path):
    patterns = set()
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    # パターンに基準となるディレクトリのパスを追加
                    full_pattern = os.path.join(base_path, stripped_line)
                    patterns.add(full_pattern)
    except FileNotFoundError:
        print(f"No .gitignore file found at {gitignore_path}")
    return patterns


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
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def summarize_directory_contents(dir_path, include_gitignore, output_file='summary.txt'):
    if include_gitignore:
        gitignore_path = os.path.join(dir_path, '.gitignore')
        EXCLUDE_PATTERNS.update(read_gitignore(gitignore_path, dir_path))
        
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
    parser = argparse.ArgumentParser(description='Summarize the contents of a directory')
    parser.add_argument('--path', required=True, help='Path to the directory to summarize')
    parser.add_argument('--include_ignore', type=bool, default=False, help='Include patterns from .gitignore')
    args = parser.parse_args()

    summarize_directory_contents(args.path, args.include_ignore)
    print(f'Summarized in summary.txt')
