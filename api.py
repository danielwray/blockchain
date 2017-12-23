from flask import Flask, request
from flask_restful import Resource, Api
import main
import time

app = Flask(__name__)
api = Api(app)

blockchain = main.BlockChain()
block = main.Block


class BlockChainAPI(Resource):

    def __init__(self):
        self.blockchain = blockchain

    def get(self):
        return {"blockchain_index_count": self.blockchain.get_latest_block().internal_index}


class TransactionAPI(Resource):

    def __init__(self):
        self.blockchain = blockchain

    def get(self):
        pass

    def put(self):
        data = request.form["data"]
        self.blockchain.add_new_block(block(1, time.strftime("%d/%m/%Y"), data))
        return {"block_added": self.blockchain.get_latest_block().hash}


class ViewAPI(Resource):

    def __init__(self):
        self.blockchain = blockchain

    def get(self):
        return {"blockchain": str(self.blockchain.get_all_blocks())}


api.add_resource(BlockChainAPI, '/')
api.add_resource(TransactionAPI, '/transaction')
api.add_resource(ViewAPI, '/view')

if __name__ == "__main__":
    app.run()