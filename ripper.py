import argparse

from substance3d_ripper import Substance3DRipper


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
        required=True,
        help="ID of the collection to retrieve",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ripper = Substance3DRipper(ims_sid=args.ims_sid)
    session_info = ripper.gen_session()

    print(f"Logged in as: {session_info.displayName} ({session_info.email})")

    result = ripper.get_collection(collection_id=args.collection_id)
    print(f"Collection retrieved: {result.title} (ID: {result.id})")

    download_item = result.assets.items[0]

    for attachment in download_item.attachments:
        if attachment.typename == "DownloadAttachment":
            print(f"Downloading asset: {attachment.label} from {attachment.url}")
            ripper.download_asset(attachment.url)


if __name__ == "__main__":
    main()
