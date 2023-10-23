import os
import openai
import streamlit as st
from PIL import Image

# APIキーを環境変数から読み取らせる
OPENAI_API_KEY = st.secrets.Openai_apikey.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
# openai.api_key = os.getenv('OPENAI_API_KEY')

# キャラクターの日本語名と英語名のマッピング
CHARACTER_MAPPING = {
    'リトルグリーンメン': "Little Green Men"
}

PLACE_MAPPING = {
    '秋葉原': "Akihabara"
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

# def generate_prompt(english_name, spot_name):
#     # キャラクター画像の生成文
#     Design_prompt_jp = (f"{english_name}がいる公園のリアルな風景を{spot_name}をいれて考案してください。"
#               "その風景イメージが出来上がるようにAIに読み込ませるので、そのイメージを、"
#               "単語ベースで、英語で、カンマ区切りで出力してください。")
#     Design_prompt_eng = chat_gpt_request(Design_prompt_jp)
#     summary_prompt = f"Reduce the number of characters in the next sentence to 200 characters.{Design_prompt_eng}"
#     summary_Design = chat_gpt_request(summary_prompt)
#     return summary_Design

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
    st.header("イメージ")
    for _ in range(1):
        gen_image = generate_image(prompt)
        st.image(gen_image, use_column_width=True)
    return gen_image

# 後から画像を付け足し
# def edit_image(gen_image):
#     response = openai.Image.create_edit(
#         image=gen_image,
#         mask=open("/image/little-green-men.png"),
#         size="256x256",
#     )
#     edit_image_url = response['data'][0]['url']
#     return edit_image_url

def generate_story(english_name, spot_name):
    story_prompt = (f"{english_name}が秋葉原に旅行にいった日記を空想のストーリーで日本語で300文字で生成してください。場所は{spot_name}を巡ってください。")
    return story_prompt

def main():
    st.title('推しのキャラクターストーリーを生成します')
    # 場所の選択
    selected_place_Target = st.sidebar.selectbox("好きな場所を選択してください", list(PLACE_MAPPING.keys()))
    place_name = PLACE_MAPPING.get(selected_place_Target, "Akihabara")

    # キャラクターの選択
    selected_oshi_Target = st.sidebar.selectbox("好きなキャラクターを選択してください", list(CHARACTER_MAPPING.keys()))
    english_name = CHARACTER_MAPPING.get(selected_oshi_Target, "Little Green Men")

    # Image create
    st.header("周辺情報")
    # map_image = Image.open("https://github.com/sh-sho/genroom_streamlit/blob/main/image/Akihabara_Station.png")
    map_image = 'https://github.com/sh-sho/genroom_streamlit/blob/main/image/Akihabara_Station.png'
    st.image(map_image, caption='秋葉原駅周辺地図', )

    spot_name_1 = "公園"
    spot_name_2 = "メイドカフェ"
    spot_name_3 = "ゲームセンター"
    # ChatGPTによるイメージの考案
    Design_prompt_jp = (f"{english_name}がいる{spot_name_1}のリアルな風景を考案してください。"
              "その風景イメージが出来上がるようにAIに読み込ませるので、そのイメージを、"
              "単語ベースで、英語で、カンマ区切りで出力してください。")
    Design_prompt_eng = chat_gpt_request(Design_prompt_jp)
    summary_prompt = f"Reduce the number of characters in the next sentence to 200 characters.{Design_prompt_eng}"
    summary_Design = chat_gpt_request(summary_prompt)
    st.write("考案されたデザインのキーワード:", summary_Design)

    # DALL-Eによる画像生成と表示
    prompt = f"Describe an interior design of {english_name} fun.{summary_Design}"
    display_images(prompt)


    st.header("考案されたストーリー")
    # Story生成
    story_prompt_1 = generate_story(english_name, spot_name=spot_name_1)
    st.write(f"ストーリー1「{spot_name_1}」:", chat_gpt_request(story_prompt_1))

    st.divider()

# ChatGPTによるイメージの考案
    Design_prompt_jp = (f"{english_name}がいる{spot_name_2}のリアルな風景を考案してください。"
              "その風景イメージが出来上がるようにAIに読み込ませるので、そのイメージを、"
              "単語ベースで、英語で、カンマ区切りで出力してください。")
    Design_prompt_eng = chat_gpt_request(Design_prompt_jp)
    summary_prompt = f"Reduce the number of characters in the next sentence to 200 characters.{Design_prompt_eng}"
    summary_Design = chat_gpt_request(summary_prompt)
    st.write("考案されたデザインのキーワード:", summary_Design)

    # DALL-Eによる画像生成と表示
    prompt = f"Describe an interior design of {english_name} fun.{summary_Design}"
    display_images(prompt)
    
    story_prompt_2 = generate_story(english_name, spot_name=spot_name_2)
    st.write("考案されたストーリー2「メイドカフェ」:", chat_gpt_request(story_prompt_2))

    st.divider()

# ChatGPTによるイメージの考案
    Design_prompt_jp = (f"{english_name}がいる{spot_name_3}のリアルな風景を考案してください。"
              "その風景イメージが出来上がるようにAIに読み込ませるので、そのイメージを、"
              "単語ベースで、英語で、カンマ区切りで出力してください。")
    Design_prompt_eng = chat_gpt_request(Design_prompt_jp)
    summary_prompt = f"Reduce the number of characters in the next sentence to 200 characters.{Design_prompt_eng}"
    summary_Design = chat_gpt_request(summary_prompt)
    st.write("考案されたデザインのキーワード:", summary_Design)

    # DALL-Eによる画像生成と表示
    prompt = f"Describe an interior design of {english_name} fun.{summary_Design}"
    display_images(prompt)
    
    story_prompt_3 = generate_story(english_name, spot_name=spot_name_3)
    st.write("考案されたストーリー3「ショップ」:", chat_gpt_request(story_prompt_3))

if __name__ == "__main__":
    main()

