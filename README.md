# Substance 3D Ripper

```bash
usage: ripper.py [-h] --ims_sid IMS_SID [--collection_id COLLECTION_ID] [--output_dir OUTPUT_DIR] [--delay-min DELAY_MIN] [--delay-max DELAY_MAX]

Substance 3D Ripper CLI

options:
  -h, --help            show this help message and exit
  --ims_sid IMS_SID     IMS session ID for authentication. 
                        Find it in your browser by entering developer tools. 
                        Navigate to Application > Cookies > https://substance3d.adobe.com/ and copy the value of ims_sid.
  --collection_id COLLECTION_ID
                        ID of the collection to retrieve
  --output_dir OUTPUT_DIR
                        Directory to save downloaded assets (default: 'substance3d_ripper_output')
  --delay-min DELAY_MIN
                        Minimum delay between requests in seconds (default: 1)
  --delay-max DELAY_MAX
                        Maximum delay between requests in seconds (default: 3)
```

Instead of passing --collection_id, you can also update the list inside 'config.py' with multiple collection IDs .

```python
# config.py

collection_ids = [
    "your_collection_id_1",
    "your_collection_id_2",
    "your_collection_id_3",
]
```

If both --collection_id and config.collection_ids are present, the CLI value takes priority.