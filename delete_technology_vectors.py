from vector_store_free import PineconeVectorStoreFree
import logging
import traceback
import sys

# Add error handling and verbose output

def delete_documents_by_source(source_name: str):
    vector_store = PineconeVectorStoreFree()
    try:
        all_docs = vector_store.find_by_source(source_name, top_k=200)
        print(f"Found {len(all_docs)} documents with source '{source_name}' in Pinecone.")
        deleted = 0
        for doc in all_docs:
            print(f"Full doc structure: {doc}")  # Debug: print the whole doc
            try:
                print(f"Deleting vector ID: {doc['id']} (title: {doc.get('title','')})")
                success = vector_store.delete_document(doc['id'])
                if success:
                    deleted += 1
                else:
                    print(f"Failed to delete vector ID: {doc['id']}")
            except Exception as e:
                print(f"Error deleting vector ID {doc.get('id')}: {e}")
                traceback.print_exc()
        print(f"Deleted {deleted} documents with source '{source_name}' from Pinecone.")
    except Exception as e:
        print(f"Error during search or deletion: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_name = sys.argv[1]
    else:
        source_name = "technology.pdf"
    delete_documents_by_source(source_name)
