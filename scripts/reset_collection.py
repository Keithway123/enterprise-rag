import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.milvus_client import COLLECTION_NAME,connect_milvus

def main():
    parser = argparse.ArgumentParser(description="Reset the Milvus collection")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm reset. Without this flag, no data will be deleted.",
    )

    args = parser.parse_args()

    if not args.yes:
        print(f"This will delete all records in collection: {COLLECTION_NAME}")
        print("Run again with --yes to confirm.")
        return
    
    client = connect_milvus()

    # drop_collection 是破坏性操作，必须由 --yes 显式确认
    if client.has_collection(COLLECTION_NAME):
        client.drop_collection(COLLECTION_NAME)
        print(f"Dropped collection: {COLLECTION_NAME}")

    # 复用 connect_milvus 的建表逻辑，避免脚本里重复写 schema
    connect_milvus()
    print(f"Recreated collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()