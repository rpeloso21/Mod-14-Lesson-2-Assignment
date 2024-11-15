import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import BakeryItem as ItemModel, db
from sqlalchemy.orm import Session

class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel

class Query(graphene.ObjectType):
    items = graphene.List(Item)

    def resolve_items(self, info):
        return db.session.execute(db.select(ItemModel)).scalars()
    
class AddItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)
        category = graphene.String(required=True)


    item = graphene.Field(Item)

    def mutate(self, info, name, price, quantity, category):
        with Session(db.engine) as session:
            with session.begin():
                item = ItemModel(name=name, price=price, quantity=quantity, category=category)
                session.add(item)

            session.refresh(item)
            return AddItem(item=item)

class UpdateItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        quantity = graphene.Int(required=True)
        category = graphene.String(required=True)


    item = graphene.Field(Item)

    def mutate(self, info, id, name, price, quantity, category):
        with Session(db.engine) as session:
            with session.begin():
                item = session.execute(db.select(ItemModel).where(ItemModel.id == id)).scalars().first()
                if item:
                    item.name = name
                    item.price = price
                    item.quantity = quantity
                    item.category = category
                else:
                    return None

            session.refresh(item)
            return UpdateItem(item=item)
        
class DeleteItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    item = graphene.Field(Item)

    def mutate(self, info, id):
        with Session(db.engine) as session:
            with session.begin():
                item = session.execute(db.select(ItemModel).where(ItemModel.id == id)).scalars().first()
                if item:
                    session.delete(item)
                else:
                    return None
            session.refresh(item)
            return DeleteItem(item=item)                

        
class Mutation(graphene.ObjectType):
    create_item = AddItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()
