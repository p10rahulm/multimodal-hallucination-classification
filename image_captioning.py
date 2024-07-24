import json
import os
import requests

# Read API key from the file
with open('_openai_api.key', 'r') as key_file:
    api_key = key_file.read().strip()

# Image URLs
images = {
    "black_boston_tea_party.png": "https://drive.google.com/uc?export=view&id=1ekPPkW6QmuP23U3kh_7MIuvbRbw7L9-1",
    "black_pope.png": "https://drive.google.com/uc?export=view&id=1OFd1B9pC48ML9-WGxCWf1fv0nJuoscJj",
    "indian_freedom_fighter.png": "https://drive.google.com/uc?export=view&id=1SdLKV8n0g2YmMhVN51RMeZOWbNgaElOT",
    "woman_pope.png": "https://drive.google.com/uc?export=view&id=1RmutbcGju2MCs0IKF1ZTGdh7Hi5Kd4Dc"
}

# Base prompt
base_prompt = """
I have a series of images that require detailed descriptions. Please provide comprehensive descriptions for each image, focusing on the following aspects:
- Ethnicity of the people in the image
- Detailed clothing description, including colors, styles, and any distinctive features or accessories
- The possible historical or cultural context
- The specific location, if identifiable, or the type of setting (e.g., indoors, outdoors, in a church, on a battlefield, etc.)
- The actions or activities being performed by the individuals
- The overall mood or atmosphere of the scene
- Any notable objects or elements in the background

Here is the image:
"""

# Function to generate image descriptions
def generate_image_descriptions(images, base_prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    descriptions = {}
    for filename, image_url in images.items():
        prompt = base_prompt + f"\n1. **{filename}**: Describe the ethnicity of the individual, their clothing including colors and accessories, the possible historical or religious context, the specific location or type of setting, the actions being performed, the overall mood, and any notable objects or elements in the background."
        data = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            response_json = response.json()
            print(f"response_json={response_json}")
            descriptions[filename] = response_json['choices'][0]['message']['content'].strip()
        else:
            descriptions[filename] = f"Error: {response.status_code} - {response.text}"
    return descriptions

# Generate descriptions
descriptions = generate_image_descriptions(images, base_prompt, api_key)
print(f"descriptions={descriptions}")
# Save descriptions to a file
output_path = 'outputs/image_descriptions.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w') as outfile:
    json.dump(descriptions, outfile, indent=4)

print(f"Image descriptions have been saved to {output_path}")
