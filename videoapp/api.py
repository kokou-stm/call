
from openai import AzureOpenAI

def get_image_dalle(user_prompt,
                               image_dimension="1024x1024",
                               image_quality="hd",
                               model="Dalle3",
                               nb_final_image=1):
   
   open_client = AzureOpenAI(
    api_key="cc5db52f27ee49c489f80a503d7604eb",  
    api_version="2023-12-01-preview",
    azure_endpoint="https://vision-plus-openai.openai.azure.com/"
   )
   response = open_client.images.generate(
     model = model,
     prompt = user_prompt,
     #size = image_dimension,
     #quality = image_quality,
     n=nb_final_image,
   )


   image_url = response.data[0].url
   return image_url
    
from dotenv import load_dotenv
import os

# Charge les variables d'environnement à partir du fichier .env
load_dotenv()

def chat(text):
    open_client = AzureOpenAI(
    api_key='6xv3rz6Asc5Qq86B8vqjhKQzSTUZPmCcSuDm5CLEV5dj9m8gTHlNJQQJ99AKACYeBjFXJ3w3AAABACOGyHXT',
    
    api_version="2023-12-01-preview",
    azure_endpoint="https://chatlearning.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview"
    )
    print(os.getenv("AZURE_OPENAI_KEY"))
    chat_completion = open_client.chat.completions.create(
        model="gpt-35-turbo", # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are my virtual english friend."},
            {"role": "user", "content": f"{text}"},
           
            ]
  
    ) 
    reponse = chat_completion.choices[0].message.content
    return  reponse


def speech_recog(audio_path):
    open_client = AzureOpenAI(
        api_key="0e457189a9644f148f4c4038ddb669af", 
            api_version="2024-02-01",
            azure_endpoint = "https://jacques.openai.azure.com/"
        )
    deployment_id = "whisperlearn" #This will correspond to the custom name you chose for your deployment when you deployed a model."
    



    result = open_client.audio.transcriptions.create(
        file=open(audio_path, "rb"),            
        model=deployment_id
    )

    text =  result.text
    return text

def image_to_text():
    api_base = "https://gpt4learn.openai.azure.com/"
    api_key= "65d90cef613149ef9cc61ea1373bbaec"
    deployment_name = 'gpt_image_meaning'
    api_version = '2023-12-01-preview' # this might change in the future

    client = AzureOpenAI(
        api_key=api_key,  
        api_version=api_version,
        base_url=f"{api_base}/openai/deployments/{deployment_name}"
    )

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            { "role": "system", "content": "You are a helpful assistant." },
            { "role": "user", "content": [  
                { 
                    "type": "text", 
                    "text": "Describe this picture:" 
                },
                { 
                    "type": "image_url",
                    "image_url": {
                        "url": "https://raw.githubusercontent.com/kokou-sekpona/langapp/main/avatar/horses-2904536_640.jpg?token=GHSAT0AAAAAACQLP63LFBXIQZPR2TLJXHX2ZRO5RGA"
                    }
                }
            ] } 
        ],
        max_tokens=2000 
    )

    print(response)


