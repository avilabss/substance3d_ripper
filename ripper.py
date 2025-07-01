import argparse
import time
import random

from substance3d_ripper import Substance3DRipper
from config import collection_ids

def parse_args():
    parser = argparse.ArgumentParser(description="Substance 3D Ripper CLI")
    parser.add_argument(
        "--ims_sid",
        type=str,
        required=True,
        help="IMS session ID for authentication. Find it in your browser by entering developer tools. Navigate to Application > Cookies > https://substance3d.adobe.com/ and copy the value of ims_sid.",
    )
    parser.add_argument(
        "--collection_id",
        type=str,
        help="ID of the collection to retrieve",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="substance3d_ripper_output",
        help="Directory to save downloaded assets (default: 'substance3d_ripper_output')",
    )
    parser.add_argument(
        "--delay-min",
        type=int,
        default=1,
        help="Minimum delay between requests in seconds (default: 1)",
    )
    parser.add_argument(
        "--delay-max",
        type=int,
        default=3,
        help="Maximum delay between requests in seconds (default: 3)",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    ripper = Substance3DRipper(ims_sid=args.ims_sid, output_dir=args.output_dir)
    session_info = ripper.gen_session()

    print(f"Logged in as: {session_info.displayName} ({session_info.email})")

    limit = 100
    
    if args.collection_id:
        collections_to_download = [args.collection_id]
    elif collection_ids:
        collections_to_download = collection_ids
    else:
        print("No collection ID was provided! update config.py or pass the ID via '--collection_id'.")

    for collection_index, collection_id in enumerate(collections_to_download, start=1):

        page = 0
        collection = ripper.get_collection(collection_id=collection_id, page=page, limit=limit)

        print(f"Retrieved collection {collection_index}/{len(collections_to_download)} | {collection.title} | Total Assets: {collection.assets.total}")

        hasMore = True
        while hasMore is True:

            print(f"\nDownloading assets on page {page} of {(collection.assets.total + limit - 1) // limit}\n")

            for item in collection.assets.items:
                print(f"Asset: {item.title} (ID: {item.id})")
                for attachment in item.attachments:
                    if attachment.typename == "DownloadAttachment":
                        print(f"Downloading asset: {attachment.label} from {attachment.url}")

                        ripper.download_asset(
                            asset_item_id=item.id,
                            asset_url=attachment.url,
                            sub_dir=f"{collection.title}/{item.title}",
                        )

                        delay = random.randint(args.delay_min, args.delay_max)
                        print(f"Waiting for {delay} seconds before next request...")
                        time.sleep(delay)
            
            hasMore = collection.assets.hasMore
            page += 1

            if hasMore:
                collection = ripper.get_collection(collection_id=collection_id, page=page, limit=limit)

        print(f"All assets downloaded successfully for collection: {collection.title} (ID: {collection.id})")


if __name__ == "__main__":
    main()
