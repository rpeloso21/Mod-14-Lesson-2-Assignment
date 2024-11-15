from flask import Flask
from flask_graphql import  GraphQLView
import graphene
from schema import Query, Mutation
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tsrost007!@localhost/movie_db'
db.init_app(app)

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)