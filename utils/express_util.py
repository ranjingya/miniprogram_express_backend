from bson import Regex

from routes import MongoClient, datetime

client = MongoClient("mongodb://root:123456@localhost:27017/")
db_express = client.wx_express
query_history_collection = db_express.wx_query_history


class QueryHistoryUtil:

    # 根据open_id查询查询历史并分页, express_id为None时查询所有
    @staticmethod
    def get_query_history_pagination(open_id, express_id, express_com_type, offset, count):
        query = {'open_id': open_id}
        if express_id is not None and express_id != '' and express_id != 'undefined':
            query['number'] = Regex(express_id)
        if express_com_type is not None and express_com_type != '' and express_com_type != 'undefined':
            query['type'] = express_com_type  # 添加快递公司查询条件
        total = query_history_collection.count_documents(query)
        query_history_list = []
        for query_history in query_history_collection.find(query).skip(offset).limit(count):
            query_history['_id'] = str(query_history['_id'])
            query_history_list.append(query_history)
        print(total, query_history_list)
        return total, query_history_list

    # 获取最大id实现自增
    @staticmethod
    def get_max_id():
        max_id_entry = query_history_collection.find_one(sort=[('id', -1)])
        if max_id_entry is None:
            return 0
        else:
            return max_id_entry['id']

    # 新增查询历史
    @staticmethod
    def add_query_history(open_id, query_result):
        print("add_query_history")
        if query_history_collection.count_documents({'open_id': open_id, 'number': query_result['number']}) < 1:
            query_history = {
                "id": QueryHistoryUtil.get_max_id() + 1,
                "open_id": open_id,
                "query_time": datetime.now().strftime('%Y:%m:%d:%H:%M:%S'),
            }
            query_history.update(query_result)
            query_history_collection.insert_one(query_history)
