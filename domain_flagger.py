import os
import argparse
import datasets
from scoring import calculate_score, get_interest_flag

def process_domain(domain_data, interesting_keywords_path, uninteresting_keywords_path):
    domain_score = calculate_score(domain_data['content'], interesting_keywords_path, uninteresting_keywords_path)
    domain_data['score'] = domain_score
    domain_data['interest_flag'] = get_interest_flag(domain_score)
    return domain_data

def main(input_json_path, interesting_keywords_path, uninteresting_keywords_path, output_json_path):
    domain_dataset = datasets.load_dataset('json', data_files=input_json_path, split="train")

    processed_dataset = domain_dataset.map(lambda domain: process_domain(domain, interesting_keywords_path, uninteresting_keywords_path))

    processed_dataset.to_json(output_json_path)

    print(f"Processing complete. Output saved to {output_json_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process domains, add interest flags and scores based on keywords.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file")
    parser.add_argument("-o", "--output", help="Path to save the output JSON file (default: processed_domains.json)")
    parser.add_argument("--interesting", default="interesting_keywords.txt", 
                        help="Path to the file containing interesting keywords (default: interesting_keywords.txt)")
    parser.add_argument("--uninteresting", default="uninteresting_keywords.txt", 
                        help="Path to the file containing uninteresting keywords (default: uninteresting_keywords.txt)")
    
    args = parser.parse_args()

    # Set default output filename if not provided
    if not args.output:
        input_name = os.path.splitext(os.path.basename(args.input))[0]
        args.output = f"{input_name}_processed.json"

    main(args.input, args.interesting, args.uninteresting, args.output)