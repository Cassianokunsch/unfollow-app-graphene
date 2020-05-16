from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

import os

app = Flask(__name__)

if os.environ.get('ENV') == "production":
    app.config.from_object('config.config.ProductionConfig')
else:
    app.config.from_object('config.config.DevelopmentConfig')


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=os.environ.get('ENV') == "development"
    )
)

if __name__ == '__main__':
    app.run(host=app.config['HOST'])
