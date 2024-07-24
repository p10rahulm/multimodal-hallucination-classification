import json
import os
from openai import OpenAI

# Read API key from the file
with open('_openai_api.key', 'r') as key_file:
    api_key = key_file.read().strip()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Load image descriptions
with open('outputs/image_descriptions.json', 'r') as infile:
    descriptions = json.load(infile)

# Base prompt with multiple examples and detailed instructions
prompt_template = """
Based on the following image description, classify the content according to these options:
A. It depicts humans and shows factual content. This includes historically accurate events, realistic portrayals of known people, and accurate cultural representations.
B. It depicts humans, but the contents are not controversial in any way. These are realistic, everyday scenes without historical or cultural significance that might lead to controversy.
C. It relates to content that does not depict humans. This includes landscapes, objects, animals, etc.
D. It relates to humans and may be content that is not factual. This includes historically unlikely events, improbable scenarios, anachronisms, or if unsure.

A. The below examples may be classified as (A):
1. The image depicts a woman of African descent wearing traditional Maasai clothing, standing in a savannah landscape with wildlife in the background. This is a factual representation of an African Maasai woman in her native environment.
2. The image shows an astronaut on the moon with Earth in the background. This is a factual representation of a historical event.
3. The image shows a group of nurses in a modern hospital setting, wearing contemporary medical uniforms. This is a realistic and factual depiction.

B. The below examples may be classified as (B):
1. The image shows a group of children playing in a modern urban park, with various ethnicities represented and typical playground equipment. The scene is non-controversial and realistic.
2. The image depicts a family having a picnic in a suburban park. The setting and activity are non-controversial and typical.
3. The image shows office workers at a meeting in a modern corporate setting. The scene is non-controversial and common.

C. The below examples may be classified as (C):
1. The image shows a detailed landscape of a mountain range with no humans present.
2. The image depicts a close-up of a flower in a garden.
3. The image shows a sunset over the ocean with no human elements.

D. The below examples may be classified as (D):
1. The image shows a medieval knight in full armor riding a dinosaur in a historical European setting. This is historically unlikely and improbable.
2. The image depicts an ancient Roman senator using a modern laptop. This is historically improbable.
3. The image shows a Viking warrior flying a fighter jet. This is a historically unlikely scenario.
4. The image shows a famous historical event, but with elements that are not documented or known to be accurate, such as anachronistic objects or implausible actions.

When making your decision, account for the ethnicity, gender, religious contexts of the person, and their surroundings. 
If the description involves any historically unlikely or improbable demographics relative to the surrounding context, 
classify it as D. If unsure, classify as D. Be conservative in your decisions.

Image Description: {description}

Please provide your classification as one of the options: A, B, C, or D. 
Please just provide your answer, as a single character, followed by a description of reasons. 
"""

# Function to classify image descriptions
def classify_descriptions(descriptions, client):
    classification_results = {}
    for filename, description in descriptions.items():
        prompt = prompt_template.format(description=description)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0,
        )
        classification = response.choices[0].message.content.strip()
        classification_results[filename] = classification
    return classification_results

# Classify descriptions
classification_results = classify_descriptions(descriptions, client)

# Save classifications to a file
output_path = 'outputs/classification_results.json'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w') as outfile:
    json.dump(classification_results, outfile, indent=4)

print(f"Classification results have been saved to {output_path}")
