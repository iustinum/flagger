import argparse
import datasets
from scoring import calculate_score, get_interest_flag

def process_domains(input_file, output_file, interesting_keywords, uninteresting_keywords):
    def add_flag_and_score(domain_data):
        score = calculate_score(domain_data['content'], interesting_keywords, uninteresting_keywords)
        domain_data['score'] = score
        domain_data['interest_flag'] = get_interest_flag(score)
        return domain_data

    domain_dataset = datasets.load_dataset('json', data_files=input_file, split="train")
    processed_dataset = domain_dataset.map(add_flag_and_score)
    processed_dataset.to_json(output_file)
    print(f"Processing complete. Output saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON file, add interest flags and scores based on keywords.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to save the output JSON file")
    parser.add_argument("interesting_keywords", help="Path to the file containing interesting keywords")
    parser.add_argument("uninteresting_keywords", help="Path to the file containing uninteresting keywords")
    
    args = parser.parse_args()

    process_domains(args.input_file, args.output_file, args.interesting_keywords, args.uninteresting_keywords)