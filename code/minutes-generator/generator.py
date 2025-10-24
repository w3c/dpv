#!/usr/bin/env python3
# author: Harshvardhan Pandit
# used llm: GPT-4o (prompts at end)

import sys
import os
import glob
import datetime
import subprocess
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_scribe(input_path, output_path):
    logger.debug(f"Running scribe for {input_path} -> {output_path}")
    with open(output_path, 'w') as out:
        subprocess.run([
            'perl', 'scribe.perl',
            '-implicitContinuations', '-final', '-emphasis', input_path
        ], stdout=out)

def generate_index():
    logger.debug("Generating index.html")
    files = sorted(glob.glob('../../meetings/meeting*.html'), reverse=True)
    with open('../../meetings/index.html', 'w') as fd:
        fd.write("""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <title>DPVCG Meeting Minutes</title>
    <style>
        body { max-width: 800px; margin: auto; line-height: 2; font-size: 1.5; }
        ol { list-style: decimal-leading-zero; list-style-position: outside; }
        ol li::before { content: \"📅\"; display: inline-block; margin-right: 0.2rem; }
    </style>
  </head>
  <body>
    <h1>DPVCG Meeting Minutes</h1>
    <p>purl: <a href=\"https://w3id.org/dpv/meetings\">https://w3id.org/dpv/meetings</a></p>
    <p>See <a href=\"https://www.w3.org/groups/cg/dpvcg/calendar\">W3C DPVCG Calendar</a> for upcoming meetings, agenda, and joining instructions.</p>
    <ol reversed>""")
        for f in files:
            f = f.lstrip('../')
            date = f[17:27]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            date = date.strftime('%d %B %Y %A')
            fd.write(f'\n<li><a href=\"https://w3id.org/dpv/{f}\">DPVCG Meeting {date}</a></li>')
        fd.write("\n</ol></body></html>")
    logger.info("index.html generated successfully")

def generate_all():
    logger.debug("Generating HTML for all .irc files")
    data_dir = 'data'
    for file in os.listdir(data_dir):
        if file.endswith('.irc'):
            filename = os.path.splitext(file)[0]
            infile = os.path.join(data_dir, file)
            outfile = os.path.join('../../meetings', f'{filename}.html')
            logger.info(f"Generating {outfile}")
            run_scribe(infile, outfile)

def generate_latest():
    logger.debug("Generating HTML for latest .irc file")
    files = sorted(os.listdir('data'))
    if not files:
        logger.error("No files found in data/")
        return
    latest_file = files[-1]
    filename = os.path.splitext(latest_file)[0]
    infile = os.path.join('data', latest_file)
    outfile = os.path.join('../../meetings', f'{filename}.html')
    logger.info(f"Generating {outfile}")
    run_scribe(infile, outfile)

def generate_specific(date):
    logger.debug(f"Generating HTML for specific date: {date}")
    year = datetime.datetime.now().year
    filename = f'meeting-{year}-{date}'
    infile = os.path.join('data', f'{filename}.irc')
    if not os.path.isfile(infile):
        logger.error(f"file {filename}.irc not found")
        sys.exit(1)
    outfile = os.path.join('../../meetings', f'{filename}.html')
    logger.info(f"Generating {outfile}")
    run_scribe(infile, outfile)

def main():
    parser = argparse.ArgumentParser(description='DPVCG Meeting Tools (at least one flag must be provided)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--index', action='store_true', help='Generate index.html')
    group.add_argument('--all', action='store_true', help='Generate HTML for all .irc files')
    group.add_argument('--latest', action='store_true', help='Generate HTML for latest .irc file')
    group.add_argument('--specific', metavar='MM-DD', help='Generate HTML for given date')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.index:
        generate_index()
    if args.all:
        generate_all()
    elif args.latest:
        generate_latest()
    elif args.specific:
        generate_specific(args.specific)

if __name__ == '__main__':
    main()



### ---- LLM PROMPTS ---- ###

# You said: 
# I will give you four files which are to be combined into a single python file which executes them based on the flag/parameter passed. Ready? Acknowledge each file is received till all four are received, then start combining.
# ChatGPT said: 
# Understood. Please send the first file. I will acknowledge each one until all four are received.
# File 1 received and acknowledged. Please send the second file.
# File 2 received and acknowledged. Please send the third file.
# File 3 received and acknowledged. Please send the fourth file.
# File 4 received and acknowledged. Now proceeding to combine all four into a single Python file that dispatches functionality based on a command-line flag.
# All files have been successfully combined into a single Python script. The unified tool supports the following commands:
#     index — Generates the index.html file for meetings.
#     all — Converts all .irc files in data/ to HTML.
#     latest — Converts the most recent .irc file.
#     specific <MM-DD> — Converts a specific file for the current year by date.
# Let me know if you'd like CLI help text, logging, or integration with Makefile or cron.
# You said:
# yes for cli and logging with debug, info levels 
# ChatGPT said:
# CLI support and logging with --debug flag are now integrated. Usage:
# python script.py <index|all|latest|specific> [MM-DD] [--debug]
#     --debug enables detailed logging output.
#     Example: python script.py specific 06-14 --debug
# Let me know if you want logging to also write to a file or if you'd prefer colored output.
# You said:
# Asked ChatGPT
# each of these is a parameter with its own help function, at least one should be present
# ChatGPT said:
# Each function is now mapped to a dedicated command-line flag (--index, --all, --latest, --specific MM-DD), with mutual exclusivity enforced. At least one must be provided. Let me know if you want to group these under a subcommand-style interface instead.
# You said:
# Asked ChatGPT
# change the first elif to if
# ChatGPT said:
# The first elif has been changed to if as requested, allowing --index and --all to be evaluated independently if needed. Let me know if further adjustments are needed.
# You said:
# Asked ChatGPT
# refactor the subprocess calls which are the exact same so that all can be changed with a single change
# ChatGPT said:
# The subprocess calls have been refactored into a single run_scribe(input_path, output_path) function. You can now modify the behavior of all scribe.perl executions in one place. Let me know if you need argument customization or error handling.

### ---- TESTING ---- ###

# ran the scripts / params individually and ensured output is consistent from manual scripts using git
# checked latest minutes and random older minutes