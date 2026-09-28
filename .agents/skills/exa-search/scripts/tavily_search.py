#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["tavily-python", "python-dotenv"]
# ///
import argparse
import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv

load_dotenv()

try:
    from tavily import TavilyClient
except ImportError:
    print("tavily-python not installed. Run: uv pip install tavily-python", file=sys.stderr)
    sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description="Search the web with Tavily.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=5, help="Number of results")
    parser.add_argument("--depth", choices=["basic", "advanced"], default="advanced", help="Search depth")
    parser.add_argument("--topic", choices=["general", "news"], default="general")
    parser.add_argument("--include-raw-content", action="store_true", help="Include raw page content in results")
    parser.add_argument("--include-answer", action="store_true", help="Include direct answer")
    parser.add_argument("-o", "--output", default=None, help="Write JSON to this file")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("TAVILY_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(2)
        
    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=args.query,
        search_depth=args.depth,
        topic=args.topic,
        max_results=args.max_results,
        include_raw_content=args.include_raw_content,
        include_answer=args.include_answer
    )
    
    text = json.dumps(response, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Wrote {len(response.get('results', []))} results to {args.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
