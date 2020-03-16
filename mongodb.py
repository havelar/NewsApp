db.createCollection('News', {
    validator: {$jsonSchema: {
        bsonType: 'object',
        required: ['Title', 'SubTitle', 'Date', 'Article', 'Type', 'Link', 'Source'],
        properties: {
            _id: {
                bsonType: 'objectId'
            },
            Title: {
                bsonType: 'string'
            },
            SubTitle: {
                bsonType: 'string'
            },
            Date: {
                bsonType: 'string'
            },
            Article: {
                bsonType: 'string'
            },
            Source: {
                bsonType: 'string'
            },            
            Type: {
                bsonType: 'string',
                enum: ['Bom', 'Ruim', 'Sem valor',
                       'Não avaliado', 'Em avaliação']
            },
            Link: {
                bsonType: 'string'
            }
        },
        additionalProperties: false
    }
    }
})

db.News.createIndex( { "Link": 1 }, { unique: true } )
