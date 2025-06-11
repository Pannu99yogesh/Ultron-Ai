# ImageGeneration.py

import asyncio
import os
from random import randint
from time import sleep
from PIL import Image
import requests
from dotenv import get_key

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"
}

async def query(payload):
    response = await asyncio.to_thread(
        requests.post, API_URL, headers=headers, json=payload
    )
    return response.content

async def generate_images(prompt: str):
    tasks = []
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality peak, sharpness maximum, Ultra High details, high resolution, seed {randint(0, 1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        filename = f"Data/{prompt.replace(' ', '_').lower()}{i+1}.jpg"
        with open(filename, "wb") as f:
            f.write(image_bytes)

def open_images(prompt: str):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_").lower()
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"🖼 Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"❌ Unable to open {image_path}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)










    


