from flask import Blueprint, request, jsonify, make_response
from pymongo.collection import ObjectId

from helper.MongoDAO import articleDB

linksBP = Blueprint('links', __name__, url_prefix='/')

@linksBP.route('/get_info', methods=['GET'])
def get_info():
    try:
        GoodPipeline = [
            {"$match": {"Type": 'Bom'}},
            {"$group": {
                "_id": "$Type",
                "count": {"$sum":1}
                }
            }
        ]

        BadPipeline = [
            {"$match": {"Type": 'Ruim'}},
            {"$group": {
                "_id": "$Type",
                "count": {"$sum":1}
                }
            }
        ]

        RestPipeline = [
            {"$match": {"Type": 'Não avaliado'}},
            {"$group": {
                "_id": "$Type",
                "count": {"$sum":1}
                }
            }
        ]

        # AllPipeline = [
        #     {"$match": {}},
        #     {"$group": {
        #         "_id": "Todas",
        #         "count": {"$sum":1}
        #         }
        #     }
        # ]

        with articleDB('News') as adb:
            GN = adb.aggregate(GoodPipeline)
            BN = adb.aggregate(BadPipeline)
            #AN = adb.aggregate(AllPipeline)
            RN = adb.aggregate(RestPipeline)


        for gn in GN:
            for bn in BN: # Esses 3 for são para pegar o a contagem dentro do cursor que o aggregate gera.
                for rn in RN:
                    data ={
                        'Bom': gn['count'],
                        'Ruim': bn['count'],
                        'Rest': rn['count']
                    }
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify('Unexpected error.\n{}'.format(str(e))), 500)

@linksBP.route('/get_links', methods=['GET'])
def get_links():
    try:
        pipeline = [
            {"$match": {"Type": "Não avaliado"}},
            {"$sample": {"size": 1}}
        ]

        with articleDB('News') as adb:
            result = adb.aggregate(pipeline)

        for article in result:

            with articleDB('News') as adb:
                adb.update_one({'_id': ObjectId(article['_id'])}, {
                    "$set": {"Type": "Em avaliação"}})

            data = {
                'id_': str(article['_id']),
                'article': article['Article'],
                'title': article['Title'],
                'subtitle': article['SubTitle'],
                'date': article['Date'],
                'link': article['Link']
            }
            return make_response(jsonify(data), 200)

        return make_response(jsonify(None), 504)
    except Exception as e:
        return make_response(jsonify('Unexpected error.\n{}'.format(str(e))), 500)


@linksBP.route('/avaliate_links', methods=['POST'])
def avaliate_links():
    try:
        _id = request.form['_id']
        status = request.form['status']
        print(75*'#')
        print("- Id: ObjectID('{0}')".format(_id))
        print('- Status', status)
    except KeyError as e:
        return make_response(jsonify('Missing key'), 400)
    except Exception as e:
        return make_response(jsonify('Unexpected error.\n{}'.format(str(e))), 500)

    try:
        if status == '1':
            with articleDB('News') as adb:
                adb.update_one({"_id": ObjectId(_id)}, {
                               "$set": {"Type": "Bom"}})

        elif status == '2':
            with articleDB('News') as adb:
                adb.update_one({"_id": ObjectId(_id)}, {
                               "$set": {"Type": "Ruim"}})

        elif status == '4':
            with articleDB('News') as adb:
                adb.update_one({"_id": ObjectId(_id)}, {
                               "$set": {"Type": "Não avaliado"}})

        elif status == '5':
            with articleDB('News') as adb:
                adb.update_one({"_id": ObjectId(_id)}, {
                               "$set": {"Type": "Não avaliado"}})

        else:
            with articleDB('News') as adb:
                adb.update_one({"_id": ObjectId(_id)}, {
                               "$set": {"Type": "Sem valor"}})

        return make_response(jsonify(None), 204)
    except Exception as e:
        return make_response(jsonify('Unexpected error.\n{}'.format(str(e))), 500)
