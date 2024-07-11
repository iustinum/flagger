import os
import json
import easyocr
from tqdm import tqdm
import argparse

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Specify the languages you want to support
    results = reader.readtext(image_path)
    if results == []:
        return "--BLANK--"
    tmp = ' '.join(res[1] for res in results)
    return tmp

def process_images(folder_path, output_file):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    results = []
    
    with tqdm(total=len(image_files), desc="Processing Images") as pbar:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            content = extract_text_from_image(image_path)
            results.append({
                "image_path": image_file,
                "content": content
            })
            pbar.update(1)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in results:
            json.dump(item, f)
            f.write('\n')
    
    print(f"Processing complete. Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract text from images in a folder")
    parser.add_argument("-i", "--input", default="/Users/justin/Downloads/screenshots", 
                        help="Path to the folder containing images (default: /Users/justin/Downloads/screenshots)")
    parser.add_argument("-o", "--output", default="input_domains.json", 
                        help="Path to save the output JSON file (default: input_domains.json)")
    
    args = parser.parse_args()
    
    process_images(args.input, args.output)

if __name__ == "__main__":
    main()