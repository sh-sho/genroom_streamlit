import os
import openai
import streamlit as st

# APIキーを環境変数から読み取らせる
OPENAI_API_KEY = st.secrets.Openai_apikey.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
# openai.api_key = os.getenv('OPENAI_API_KEY')

# キャラクターの日本語名と英語名のマッピング
CHARACTER_MAPPING = {
    'ガンダム': "Mobile Suit Gundam",
    'ドラえもん': "Doraemon",
    'セーラームーン': "Sailor Moon",
    'ナルト': "Naruto Shippuden",
    'ワンピース': "ONE PIECE",
    '鬼滅の刃': "Demon Slayer"
}

def chat_gpt_request(prompt):
    """
    GPT-3.5-turboを使って与えられたプロンプトに基づいてテキストを生成します。
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        temperature=0.8,
    )
    message = response.choices[0].message['content'].strip()
    return message

def generate_image(prompt):
    """
    DALL-Eを使って与えられたプロンプトに基づいて画像を生成します。
    """
    response = openai.Image.create(
        prompt=prompt,
        model="image-alpha-001",
        n=1,
        size="256x256",
        response_format="url",
    )
    image_url = response['data'][0]['url']
    return image_url

def display_images(prompt):
    """
    生成された画像を表示します。
    """
    st.header("部屋の内装イメージ 3パターン")
    for _ in range(3):
        st.image(generate_image(prompt), use_column_width=True)

def main():
    st.title('推し活で利用したい休憩・宿泊する理想のお部屋は？')

    selected_oshi_Target = st.sidebar.selectbox("好きなキャラクターを選択してください", list(CHARACTER_MAPPING.keys()))
    
    english_name = CHARACTER_MAPPING.get(selected_oshi_Target, "Mobile Suit Gundam")

    # ChatGPTによる部屋の内装イメージの考案
    prompt = (f"{english_name}のファンが住んでいる、間取り：ワンルームの部屋の内装を考案してください。"
              "その内装イメージが出来上がるようにAIに読み込ませるので、そのイメージを、"
              "単語ベースで、英語で、カンマ区切りで出力してください。")
    roomDesign = chat_gpt_request(prompt)
    prompt = f"Reduce the number of characters in the next sentence to 200 characters.{roomDesign}"
    summary_roomDesign = chat_gpt_request(prompt)
    st.write("考案された部屋の内装デザインのキーワード:", summary_roomDesign)

    # DALL-Eによる画像生成と表示
    prompt = f"Describe an interior design of {english_name} fun.{summary_roomDesign}"
    display_images(prompt)

if __name__ == "__main__":
    main()

"""コード改善ポイント
改善ポイントの説明
環境変数の利用: APIキーはコードに直接書くべきではありません。これはセキュリティリスクとなります。そのため、このコードではos.getenv("OPENAI_API_KEY")を使って、環境変数からAPIキーを取得しています。

キャラクター名の変換の最適化: キャラクター名の変換ロジックを辞書CHARACTER_MAPPINGを使ってシンプルにしました。

画像表示の最適化: 画像の生成と表示のコードを関数display_imagesにまとめ、コードの重複を減らしました。

メインロジックの関数化: コードの主要なロジックをmain()関数にまとめて、コードの構造をクリアにしました。これにより、他のスクリプトやノートブックからこのコードをインポートして利用することも可能になります。

注意: APIキーを環境変数としてセットする方法は、実行環境(OSや使用しているIDEなど)によりますので、適切な方法を選んでください。そして、このコードを実行する前に、環境変数OPENAI_API_KEYに実際のOpenAIのAPIキーをセットしてください。


"""