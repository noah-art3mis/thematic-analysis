import os
import json
from trafilatura import fetch_url, extract

with open("urls.json", "r") as f:
    websites = json.load(f)


def trafilate(id: int, url: str) -> None:

    base_path = f"output/{id}"
    json_path = f"{base_path}.json"
    text_path = f"{base_path}-text.txt"
    metadata_path = f"{base_path}-metadata.txt"

    # Skip if all output files already exist
    if all(os.path.exists(path) for path in [json_path, text_path, metadata_path]):
        print(f"{id}: files already exist, skipping")
        return

    downloaded = fetch_url("https://archive.is/" + url)

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
    main_unsafe()
