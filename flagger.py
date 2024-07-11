#!/usr/bin/env python3
import click
import os
from image_text_extractor import process_images
from domain_processor import process_domains
from score_visualizer import visualize_scores

@click.group()
def cli():
    """Flagger: A tool for processing and analyzing domain images."""
    pass

@cli.command()
@click.option('-i', '--input', 'input_folder', required=True, type=click.Path(exists=True), help='Path to the folder containing images')
@click.option('-o', '--output', 'output_file', default='input_domains.json', help='Path to save the output JSON file')
def extract(input_folder, output_file):
    """Extract text from images in a folder."""
    process_images(input_folder, output_file)

@cli.command()
@click.option('-i', '--input', 'input_file', required=True, type=click.Path(exists=True), help='Path to the input JSON file')
@click.option('-o', '--output', 'output_file', default='input_domains_processed.json', help='Path to save the output JSON file')
@click.option('--interesting', 'interesting_keywords', default='interesting_keywords.txt', help='Path to the file containing interesting keywords')
@click.option('--uninteresting', 'uninteresting_keywords', default='uninteresting_keywords.txt', help='Path to the file containing uninteresting keywords')
def flag(input_file, output_file, interesting_keywords, uninteresting_keywords):
    """Process domains and add interest flags based on keywords."""
    process_domains(input_file, output_file, interesting_keywords, uninteresting_keywords)

@cli.command()
@click.option('-i', '--input', 'input_file', required=True, type=click.Path(exists=True), help='Path to the input JSON file')
@click.option('-o', '--output', 'output_file', default='score_distribution.png', help='Path to save the output histogram image')
@click.option('-t', '--top', 'top_n', type=int, help='Number of top domains to display')
@click.option('-b', '--bottom', 'bottom_n', type=int, help='Number of bottom domains to display')
def visualize(input_file, output_file, top_n, bottom_n):
    """Generate a histogram of domain scores and optionally list top/bottom domains."""
    visualize_scores(input_file, output_file, top_n, bottom_n)

if __name__ == '__main__':
    cli()