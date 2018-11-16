from sqlalchemy import Column

from unbabel.db import db


class Translation(db.Model):
    id = Column(db.Integer, primary_key=True)
    uid = Column(db.String)
