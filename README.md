### README.md

# Image Captioning and Classification

This repository contains two Python scripts for generating detailed descriptions of images and classifying the factuality and context of these descriptions using OpenAI's GPT models.

## Prerequisites

- Python 3.x
- `requests` library
- `openai` library
- OpenAI API key stored in `_openai_api.key` file

## Files

### 1. image_captioning.py

This script generates detailed descriptions for a set of images.

#### Usage

1. **Image URLs**: Update the `images` dictionary with the URLs of your images.
2. **Run the script**: Execute the script to generate descriptions.
   ```bash
   python image_captioning.py
   ```

#### Description

- **Images**: Dictionary of image filenames and their URLs.
- **Base Prompt**: Template for generating descriptions.
- **Function**: `generate_image_descriptions` sends the images to OpenAI's API and saves the descriptions.

### 2. image_classification.py

This script classifies the generated image descriptions based on their factuality and context.

#### Usage

1. **Generate Descriptions**: Ensure `image_captioning.py` has been run and `outputs/image_descriptions.json` exists.
2. **Run the script**: Execute the script to classify descriptions.
   ```bash
   python image_classification.py
   ```

#### Description

- **Descriptions**: Loaded from `outputs/image_descriptions.json`.
- **Prompt Template**: Detailed instructions and examples for classification.
- **Function**: `classify_descriptions` sends the descriptions to OpenAI's API for classification.

## Output

- **Descriptions**: Saved in `outputs/image_descriptions.json`.
- **Classifications**: Saved in `outputs/classification_results.json`.

## License

This project is licensed under the MIT License.
