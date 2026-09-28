#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["ddgs"]
# ///
import argparse
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    from ddgs import DDGS
except ImportError as e:
    print(f"ImportError: {e}", file=sys.stderr)
    print("ddgs not installed or failed to import. Run: uv pip install ddgs", file=sys.stderr)
    sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description="Search the web with DuckDuckGo (Free, no API key).")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10, help="Number of results")
    parser.add_argument("-o", "--output", default=None, help="Write JSON to this file")
    
    args = parser.parse_args()
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(args.query, max_results=args.max_results))
            
        response = {
            "query": args.query,
            "num_results": len(results),
            "results": results
        }
        
        text = json.dumps(response, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(f"Wrote {len(results)} results to {args.output}")
        else:
            print(text)
    except Exception as e:
        print(f"Error during DuckDuckGo search: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
