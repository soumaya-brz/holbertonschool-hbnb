class SQLAlchemyRepository:
    def __init__(self, model_cls, session):
        self.model_cls = model_cls
        self.session = session

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return obj

    def get(self, obj_id):
        return self.session.get(self.model_cls, obj_id)

    def get_all(self):
        return self.session.query(self.model_cls).all()

    def get_by_attribute(self, attr_name, value):
        return self.session.query(self.model_cls).filter(getattr(self.model_cls, attr_name) == value).first()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        self.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True