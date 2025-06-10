import os
import json
import time
from trafilatura import fetch_url, extract
from waybackpy import WaybackMachineCDXServerAPI
from waybackpy.exceptions import NoCDXRecordFound

with open("urls.json", "r") as f:
    websites = json.load(f)

def get_archived_url(url: str) -> str:
    try:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        cdx_api = WaybackMachineCDXServerAPI(url, user_agent)
        
        # Get snapshots and filter for valid ones
        snapshots = list(cdx_api.snapshots())
        if not snapshots:
            print(f"No snapshots found for {url}, using original URL")
            return url
            
        # Get the most recent valid snapshot
        for snapshot in sorted(snapshots, key=lambda x: x.timestamp, reverse=True):
            try:
                return snapshot.archive_url
            except (ValueError, AttributeError):
                continue
                
        return url
    except Exception as e:
        print(f"Error getting archive for {url}: {str(e)}")
        return url

def trafilate(id: int, url: str) -> None:

    base_path = f"output/{id}"
    json_path = f"{base_path}.json"
    text_path = f"{base_path}-text.txt"
    metadata_path = f"{base_path}-metadata.txt"

    # Skip if all output files already exist
    if all(os.path.exists(path) for path in [json_path, text_path, metadata_path]):
        print(f"{id}: files already exist, skipping")
        return

    # Get the archived URL
    archived_url = get_archived_url(url)
    print(f"{id}: Using archived URL: {archived_url}")
    
    downloaded = fetch_url(archived_url)

    if downloaded is None:
        raise Exception(f"Download failed on item {id}: {url}")

    result = extract(downloaded, output_format="json", with_metadata=True)
    if result is None:
        raise Exception(f"Extraction failed on item: {id}")

    json_result = json.loads(result)
    json_result["_id"] = id

    # save all
    with open(json_path, "w") as f:
        json.dump(json_result, f, indent=4)
        print(f"{id}: item saved")

    # save text
    text = "\n\n".join(
        [
            str(json_result.get("title", "Title Not Found")),
            str(json_result.get("excerpt", "Excerpt Not Found")),
            str(json_result.get("text", "Text Not Found")),
        ]
    )

    with open(text_path, "w") as f:
        f.write(text)
        print(f"{id}: text saved")

    # save metadata
    metadata = "\n\n".join(
        [
            f"title: {str(json_result.get('title', ''))}",
            f"excerpt: {str(json_result.get('excerpt', ''))}",
            f"author: {str(json_result.get('author', ''))}",
            f"hostname: {str(json_result.get('hostname', ''))}",
            f"date: {str(json_result.get('date', ''))}",
            f"fingerprint: {str(json_result.get('fingerprint', ''))}",
            f"source: {str(json_result.get('source', ''))}",
            f"source-hostname: {str(json_result.get('source-hostname', ''))}",
            f"categories: {str(json_result.get('categories', ''))}",
            f"tags: {str(json_result.get('tags', ''))}",
        ]
    )

    with open(metadata_path, "w") as f:
        f.write(metadata)
        print(f"{id}: metadata saved")


def main():
    os.makedirs("output", exist_ok=True)

    for website in websites:
        try:
            _id = website.get("id")
            _url = website.get("url")
            trafilate(_id, _url)
        except Exception as e:
            print(f"Error in item {_id}: {e}")

            with open("output/errors.log", "a") as log:
                log.write(f"Item {_id} ({_url}) failed: {e}\n")


def main_unsafe():
    os.makedirs("output", exist_ok=True)

    for website in websites:
        _id = website.get("id")
        _url = website.get("url")
        trafilate(_id, _url)


if __name__ == "__main__":
    main()
