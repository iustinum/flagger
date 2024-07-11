import json
import matplotlib.pyplot as plt
import numpy as np
import argparse
from operator import itemgetter

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

def create_histogram(scores, output_file):
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=20, edgecolor='black')
    plt.title('Distribution of Domain Scores')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.axvline(np.mean(scores), color='red', linestyle='dashed', linewidth=1, label=f'Mean ({np.mean(scores):.2f})')
    plt.axvline(np.median(scores), color='green', linestyle='dashed', linewidth=1, label=f'Median ({np.median(scores):.2f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_file)
    print(f"Histogram saved as {output_file}")

def get_top_domains(data, n):
    return sorted(data, key=itemgetter('score'), reverse=True)[:n]

def get_bottom_domains(data, n):
    return sorted(data, key=itemgetter('score'))[:n]

def print_domains(domains, title):
    if not domains:
        return
    print(f"\n{title}:")
    for i, domain in enumerate(domains, 1):
        print(f"{i}. Score: {domain['score']:.2f} - {domain['image_path']}")
        print(f"   Content: {domain['content'][:100]}..." if len(domain['content']) > 100 else f"   Content: {domain['content']}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Generate a histogram of domain scores and optionally list top/bottom domains")
    parser.add_argument("-i", "--input", default="/Users/justin/playground/aroocon/input_domains_processed.json",
                        help="Path to the input JSON file (default: /Users/justin/playground/aroocon/input_domains_processed.json)")
    parser.add_argument("-o", "--output", default="score_distribution.png",
                        help="Path to save the output histogram image (default: score_distribution.png)")
    parser.add_argument("-t", "--top", type=int, metavar='N',
                        help="Number of top domains to display")
    parser.add_argument("-b", "--bottom", type=int, metavar='N',
                        help="Number of bottom domains to display")
    
    args = parser.parse_args()
    
    data = load_data(args.input)
    scores = [item['score'] for item in data]
    
    create_histogram(scores, args.output)
    
    if args.top is not None:
        top_domains = get_top_domains(data, args.top)
        print_domains(top_domains, f"Top {args.top} domains by score")
    
    if args.bottom is not None:
        bottom_domains = get_bottom_domains(data, args.bottom)
        print_domains(bottom_domains, f"Bottom {args.bottom} domains by score")
    
    if args.top is None and args.bottom is None:
        print("\nNo domains listed. Use -t or -b flags to display top or bottom domains.")

if __name__ == "__main__":
    main()