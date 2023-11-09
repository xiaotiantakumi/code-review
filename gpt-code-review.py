import requests
import configparser
import inquirer
import glob
import os


def load_api_token():
    """ ./.env/config.txtからChatGPTのAPIトークンを読み込む """
    config = configparser.ConfigParser()
    config.read('./.env/config.txt')
    return config['ChatGPT']['api_token']


def select_file_to_review():
    """ レビューするファイルを選択する """
    txt_files = glob.glob("*.txt")
    questions = [
        inquirer.List('file',
                      message="レビューするファイルを選択してください:",
                      choices=txt_files,
                      ),
    ]
    answers = inquirer.prompt(questions)
    return answers['file']


def call_chatgpt_api(code_to_review, api_token):
    """ ChatGPT APIを呼び出してコードレビューを行う """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {"role": "system", "content": "You are an experienced systems engineer. You are very keen to ensure "
                                          "quality by conducting rigorous code reviews of your colleagues."},
            {"role": "user", "content": f"Please do a rigorous code review:\n\n{code_to_review}\n"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)

    # レスポンスの完全な内容を確認するための出力
    print("Response from API:", response.json())

    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")


def save_review_result(file_name, review_result):
    """ レビュー結果をファイルに保存する """
    output_dir = './output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name_except_ext = os.path.splitext(file_name)[0]
    output_file_path = os.path.join(output_dir, f"{file_name_except_ext}-review.txt")
    with open(output_file_path, 'w') as file:
        file.write(review_result)


def main():
    api_token = load_api_token()
    file_to_review = select_file_to_review()

    with open(file_to_review, 'r') as file:
        code_to_review = file.read()

    review_result = call_chatgpt_api(code_to_review, api_token)
    save_review_result(file_to_review, review_result)
    print(f'レビュー結果が保存されました。')


if __name__ == "__main__":
    main()
