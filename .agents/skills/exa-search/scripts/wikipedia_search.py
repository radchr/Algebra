#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["wikipedia"]
# ///
import argparse
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import wikipedia
except ImportError:
    print("wikipedia not installed. Run: uv pip install wikipedia", file=sys.stderr)
    sys.exit(2)

def main():
    parser = argparse.ArgumentParser(description="Search Wikipedia.")
    parser.add_argument("query", help="Search query or exact page title")
    parser.add_argument("--action", choices=["search", "page", "summary"], default="summary", help="Action to perform")
    parser.add_argument("--lang", default="en", help="Language code (e.g. en, uk)")
    parser.add_argument("-o", "--output", default=None, help="Write output to this file")
    
    args = parser.parse_args()
    wikipedia.set_lang(args.lang)
    
    result = None
    if args.action == "search":
        result = wikipedia.search(args.query)
    elif args.action == "summary":
        try:
            result = wikipedia.summary(args.query)
        except wikipedia.exceptions.DisambiguationError as e:
            result = {"error": "DisambiguationError", "options": e.options}
        except wikipedia.exceptions.PageError:
            result = {"error": "PageError", "message": "Page not found."}
        except Exception as e:
            result = {"error": str(e)}
    elif args.action == "page":
        try:
            page = wikipedia.page(args.query)
            result = {
                "title": page.title,
                "url": page.url,
                "content": page.content
            }
        except wikipedia.exceptions.DisambiguationError as e:
            result = {"error": "DisambiguationError", "options": e.options}
        except wikipedia.exceptions.PageError:
            result = {"error": "PageError", "message": "Page not found."}
        except Exception as e:
            result = {"error": str(e)}
            
    if isinstance(result, str):
        text = result
    else:
        text = json.dumps(result, indent=2, ensure_ascii=False)
        
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Wrote output to {args.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
