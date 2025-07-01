import json
from collections import defaultdict
from clean_upload import client

def aggregate_field_counts(client, db_name, field_name, output_file="output_counts.json"):
    """
    Aggregate counts of a specified field across all collections in a MongoDB database.
    Counts how many times each value appears, counting duplicates in collections.

    Args:
        client: MongoClient instance.
        db_name (str): Name of the MongoDB database.
        field_name (str): The field name to aggregate counts for.
        output_file (str, optional): JSON file path to save the results. Defaults to "output_counts.json".
    """
    db = client[db_name]
    counts = defaultdict(int)

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        for doc in collection.find({}, {field_name: 1}):
            key = doc.get(field_name)
            if key:
                counts[key] += 1

    counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(counts, f, ensure_ascii=False, indent=2)

    print(f"Saved aggregated counts to {output_file}")

aggregate_field_counts(client, "Latin-Texts", "head_word", output_file="headword_counts.json")
