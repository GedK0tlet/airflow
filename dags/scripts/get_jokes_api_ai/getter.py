import requests
import json

def get_jokes_api_ai(api_key: str, examples: [str], theme: str, ti, **kwargs) -> None:

    text_system = "Ты пришел на праздник, тебя попросили рассказать анекдот, который никто не знает. Он может быть на любую тему, любой длинны, к примеру такой "
    for example in examples:
        text_system += example + " или такой "

    prompt = {
        "modelUri": "gpt://b1guuius5lto8g3tmiq7/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.65,
            "maxTokens": "2000"
        },

        "messages" : [
            {
                "role": "system",
                "text": text_system
            },
            {
                "role": "user",
                "text": f"Привет! Расскажи придуманный тобой анекдот про {theme}!"
            },

        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}"
    }

    response = requests.post(url, json=prompt, headers=headers)
    response_dict = json.loads(response.text)
    # print(response_dict)

    try:
        text_msg = response_dict['result']['alternatives'][0]['message']['text']
        # print(text_msg)
        ti.xcom_push(key="text_anekdot", value=text_msg)
    except Exception as e:
        # print(e)
        pass
