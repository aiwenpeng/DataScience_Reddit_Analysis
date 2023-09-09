from pymongo.mongo_client import MongoClient
import configparser
import logging

class mongodb_connection():
    """

    """

    def __init__(self, url, db_name, collection_name) -> None:
        # Create a new client and connect to the server
        client = MongoClient(url)

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            logging.info("error connect to MongoDB")

        # Connect to Reddit_Post database
        db = client[db_name]

        # Connect to Collection
        self.collection = db[collection_name]

    def add_documents(self, documents, add_one=True):
        """
        description: insert documents to a MongoDB collection
        documents: dictionaries  
        add_one: add only one document
        
        """
        try:
            if add_one:
                success = self.collection.insert_one(documents)
                num_inserted = [success.inserted_id]
            else:
                success = self.collection.insert_many(documents)
                num_inserted = success.inserted_ids
            print(f"Inserted {len(num_inserted)} document(s)!")
        except Exception as e:
            print(e)
            logging.info("error add documents")

    def get_documents(self, query):
        """
        description: get documents to from collection
        query: key and value

        """
        documents = self.collection.find(query)
        result = []
        try:
            for doc in documents:
                result.append(doc)
        except Exception as e:
            print(e)
            logging.info("error get documents")
        
        return result
    
    def delete_documents(self, query, delete_one=True):
        """
        description: delete documents from collection
        query:
        delete_one: only delete one document
        """
        try:
            if delete_one:
                deleted_obj = self.collection.delete_one(query)
            else:
                deleted_obj = self.collection.delete_many(query)
            print(deleted_obj.deleted_count, "documents deleted")
        except Exception as e:
            print(e)
            logging.info("error delete documents")
    


if __name__ == "__main__":
   path_to_setting = '/home/awpeng/DataScience_Reddit_Analysis/secrets.ini'
   Configs = configparser.ConfigParser()
   Configs.read(path_to_setting)
   mongo_username = Configs['MongoDB']['user_name']
   mongo_pwd = Configs['MongoDB']['pwd']
   url = f"mongodb+srv://{mongo_username}:{mongo_pwd}@cluster0.pfuwrvp.mongodb.net/?retryWrites=true&w=majority"
   db_name = "Reddit_Post"
   collection_name = "test_collection"
   documents_test = {"name":"AnotherOne", "height":180}
   doc_test2 = [
       {"name":"a", "score": 2},
       {"name":"b", "score": 1}
   ]
   mc = mongodb_connection(url, db_name, collection_name)
   print(mc.get_documents({"name":"eva"}))
#    mc.add_documents(doc_test2, add_one=False)
   mc.delete_documents({"height":180}, delete_one=False)

