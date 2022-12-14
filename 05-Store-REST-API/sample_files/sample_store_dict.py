# # # WHEN USING A DICTIONARY AS A DB

# @blueprint.route("/store") 
# class StoreList(MethodView):
#     # Retrieve All Store Data
#     @blueprint.response(200, PlainStoreSchema(many=True))  
#     # NB: set many=True to retrieve more than one store data.
#     def get(self):
#         return {"stores": list(stores.values())}

#     # Creating Store Data
#     @blueprint.arguments(PlainStoreSchema)  
#     # NB: when creating, pass the schema in the blueprint.arguments.
#     @blueprint.response(200, PlainStoreSchema)
#     def post(self, store_data):
#         # validate if store already exist        
#         for store in stores.values():
#             if store_data["id"] == store["id"]:
#                 abort(400, message="Store already exist")
        
#         # create unique store id (a string) using uuid
#         store_id = uuid.uuid4().hex  
#         # assign the unique store id to a store data
#         store = {**store_data, "id": store_id}  
#         # NB: ** retrieves all fields data inputted during store creation.
#         # save the store with unique id to stores
#         stores[id] = store 
#         return store, 201


# @blueprint.route("/store/<string:store_id>")
# class Store(MethodView):
#     # Retrieve Store Data by store_id
#     @blueprint.response(200, PlainStoreSchema)
#     def get(self, store_id):
#         try:
#             return stores[store_id]
#         except KeyError:
#             return abort(404, message="Store not found")

#     # Delete Store Data by store_id
#     def delete(self, store_id):
#         try:
#             del stores[store_id]
#             return {"message": "Store deleted successfully"}
#         except KeyError:
#             return abort(404, message="Store not found")

#     # Update Store Data by store_id
#     def put(self, store_id, store_data):
#         try:
#             store = stores[store_id]
#             store |= store_data
#             return store
#         except AttributeError:
#             return abort(404, message="Store not updated")
