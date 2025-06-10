import os 
import json
from trafilatura import fetch_url, extract

with open('urls.txt', 'r') as f:
    URLS = [url.strip() for url in f.readlines()]

def trafilate(url, counter):
    downloaded = fetch_url(url)
    if downloaded is None:
        print(f"Download failed on item: {url}")
        raise Exception(f"Download failed on item: {counter}")
    
    result = extract(downloaded, output_format='json', with_metadata=True)
    if result is None:
        raise Exception(f"Extraction failed on item: {counter}")
    
    json_result = json.loads(result)
    
    json_result['_id'] = counter
    
    # save all
    with open(f'output/{counter}.json', 'w') as f:
        json.dump(json_result, f, indent=4)
        print(f'{counter}: item saved')

        
    # save text
    text = '\n\n'.join([
        str(json_result.get('title', 'Title Not Found')),
        str(json_result.get('excerpt', 'Excerpt Not Found')),
        str(json_result.get('text', 'Text Not Found'))
    ])
    
    with open(f'output/{counter}-text.txt', 'w') as f:
        f.write(text)
        print(f'{counter}: text saved')
        
        
    # save metadata
    metadata = "\n\n".join([
        f"title: {str(json_result.get('title', ''))}",
        f"excerpt: {str(json_result.get('excerpt', ''))}",
        f"author: {str(json_result.get('author', ''))}",
        f"hostname: {str(json_result.get('hostname', ''))}",
        f"date: {str(json_result.get('date', ''))}",
        f"fingerprint: {str(json_result.get('fingerprint', ''))}",
        f"source: {str(json_result.get('source', ''))}",
        f"source-hostname: {str(json_result.get('source-hostname', ''))}",
        f"categories: {str(json_result.get('categories', ''))}",
        f"tags: {str(json_result.get('tags', ''))}"
    ])

    with open(f'output/{counter}-metadata.txt', 'w') as f:
        f.write(metadata)
        print(f'{counter}: metadata saved')
        

def main():
    os.makedirs('output', exist_ok=True)
    
    for counter, url in enumerate(URLS, 1):
        try:
            trafilate(url, counter)
        except Exception as e:
            print(f'Error in item {counter}: {e}')
            
            with open('output/errors.log', 'a') as log:
                log.write(f"Item {counter} ({url}) failed: {e}\n")
            
if __name__ == "__main__":
    main()