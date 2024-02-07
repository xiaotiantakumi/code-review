import subprocess
import os
import configparser
import inquirer
import glob

def get_config_files(directory):
    """ 指定されたディレクトリ内の設定ファイルの一覧を取得する """
    return glob.glob(f"{directory}/*.txt")

def select_config_file(files):
    """ 設定ファイルを一覧から選択する """
    questions = [
        inquirer.List('config',
                      message="使用する設定ファイルを選択してください:",
                      choices=files,
                     ),
    ]
    answers = inquirer.prompt(questions)
    return answers['config']

def load_config(file_path):
    """ 設定ファイルを読み込む """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['Repository']['url'], config['Repository']['password'], config['Git']['path']


def get_branches(repo_url, password, git_path):
    """ リポジトリのブランチを一覧表示する """
    url_with_credentials = repo_url.replace('https://', f'https://{password}@')
    repo_name = repo_url.split('/')[-1].split('.')[0]
    clone_dir = './tmp_clone'
    os.makedirs(clone_dir, exist_ok=True)
    os.chdir(clone_dir)
    # リポジトリのディレクトリが既に存在するかチェック
    if os.path.isdir(repo_name):
        # リポジトリが存在する場合、ディレクトリに移動して fetch と pull を実行
        os.chdir(repo_name)
        subprocess.run([git_path, 'fetch'], stdout=subprocess.DEVNULL)
        subprocess.run([git_path, 'pull', 'origin', 'main', '--rebase'], stdout=subprocess.DEVNULL)
    else:
        # リポジトリが存在しない場合、clone を実行
        subprocess.run([git_path, 'clone', url_with_credentials], stdout=subprocess.DEVNULL)
        os.chdir(repo_name)

    # ブランチの一覧を取得
    branches = subprocess.check_output(
        [git_path, 'branch', '-r', '--sort=-committerdate'],
        stderr=subprocess.DEVNULL
    ).decode('utf-8')

    os.chdir('../..')  # 元のディレクトリに戻る
    return branches



def select_branch(branches):
    """ ブランチを選択する """
    branches_list = branches.strip().split('\n')
    questions = [
        inquirer.List('branch',
                      message="以下のブランチから選択してください:",
                      choices=branches_list,
                     ),
    ]
    answers = inquirer.prompt(questions)
    return answers['branch']


def get_diff(selected_branch, repo_url, git_path):
    """ 選択したブランチとの差分を取得する """
    os.chdir('./tmp_clone')
    repo_name = repo_url.split('/')[-1].split('.')[0]
    os.chdir(repo_name)
    diff_output = subprocess.check_output([git_path, 'diff', 'origin/main', selected_branch])
    os.chdir('../..')  # 元のディレクトリに戻る
    return diff_output

# 設定ファイルの一覧を取得
config_files = get_config_files('./.env')

# 設定ファイルを選択
selected_config = select_config_file(config_files)

# 設定ファイルからURL、ユーザー名、パスワード、Gitのパスを読み込む
repo_url, password, git_path = load_config(selected_config)

# ブランチの一覧を取得
branches = get_branches(repo_url, password, git_path)

# ブランチを選択
selected_branch = select_branch(branches).strip()

# 差分を取得
diff_output = get_diff(selected_branch, repo_url, git_path)

# 差分をカレントディレクトリのselected_branchよりbranch名を取得してbranch名.txtファイルに出力。
branch_name = selected_branch.split('/')[-1]
with open(f'{branch_name}.txt', 'wb') as f:
    f.write(diff_output)
print('差分を出力しました。')
print(f'ファイルのフルパス: {os.path.abspath(f"{branch_name}.txt")}')
