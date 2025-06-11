from typing import Dict, List, Any, Optional, Union
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from src.config import CONFIG

class CollectionManager:
    """Interface for managing MongoDB collections (tables)"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create_collection(self, collection_name: str, options: Dict = None) -> bool:
        """
        Create a new collection with optional configuration
        Args:
            collection_name: Name of the collection
            options: Additional collection options (e.g., capped, size, etc.)
        """
        try:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name, **(options or {}))
                return True
            return False
        except Exception as e:
            raise Exception(f"Failed to create collection: {str(e)}")

    def delete_collection(self, collection_name: str) -> bool:
        """Delete a collection"""
        try:
            if collection_name in self.db.list_collection_names():
                self.db.drop_collection(collection_name)
                return True
            return False
        except Exception as e:
            raise Exception(f"Failed to delete collection: {str(e)}")

    def list_collections(self) -> List[str]:
        """List all collections in the database"""
        return self.db.list_collection_names()

class CollectionOperator:
    """Interface for performing CRUD operations on a specific collection"""
    
    def __init__(self, collection: Collection):
        self.collection = collection

    def insert(self, data: Union[Dict, List[Dict]], many: bool = False) -> Union[str, List[str]]:
        """
        Insert one or multiple documents
        Args:
            data: Document or list of documents to insert
            many: If True, insert multiple documents
        Returns:
            Inserted document ID(s)
        """
        try:
            if many:
                result = self.collection.insert_many(data)
                return result.inserted_ids
            else:
                result = self.collection.insert_one(data)
                return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Insert operation failed: {str(e)}")

    def find(self, 
            query: Dict = None, 
            projection: Dict = None,
            sort: List[tuple] = None,
            skip: int = 0,
            limit: int = 0) -> List[Dict]:
        """
        Find documents matching the query
        Args:
            query: Query filter
            projection: Fields to include/exclude
            sort: List of (field, direction) pairs for sorting
            skip: Number of documents to skip
            limit: Maximum number of documents to return
        """
        try:
            cursor = self.collection.find(
                filter=query or {}, 
                projection=projection
            )
            if sort:
                cursor = cursor.sort(sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            raise Exception(f"Find operation failed: {str(e)}")

    def update(self,
             query: Dict,
             update_data: Dict,
             many: bool = False,
             upsert: bool = False) -> int:
        """
        Update documents matching the query
        Args:
            query: Query to match documents
            update_data: Data to update
            many: If True, update multiple documents
            upsert: If True, insert document if none matches query
        Returns:
            Number of documents modified
        """
        try:
            if many:
                result = self.collection.update_many(
                    query, update_data, upsert=upsert
                )
            else:
                result = self.collection.update_one(
                    query, update_data, upsert=upsert
                )
            return result.modified_count
        except Exception as e:
            raise Exception(f"Update operation failed: {str(e)}")

    def delete(self, query: Dict, many: bool = False) -> int:
        """
        Delete documents matching the query
        Args:
            query: Query to match documents
            many: If True, delete multiple documents
        Returns:
            Number of documents deleted
        """
        try:
            if many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            raise Exception(f"Delete operation failed: {str(e)}")

class MongoDBInterface:
    """Main interface for MongoDB operations"""
    
    def __init__(self, host: str = "localhost", port: int = 27017, db_name: str = "mydb"):
        host = CONFIG.get("mongodb.host", env_var="MONGODB_HOST")
        port = int(CONFIG.get("mongodb.port", env_var="MONGODB_PORT"))
        db_name = CONFIG.get("mongodb.db_name", env_var="MONGODB_DB_NAME")
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection_manager = CollectionManager(self.db)
    
    def get_collection_manager(self) -> CollectionManager:
        """Get the collection manager interface"""
        return self.collection_manager
    
    def get_collection_operator(self, collection_name: str) -> CollectionOperator:
        """Get operator interface for a specific collection"""
        return CollectionOperator(self.db[collection_name])