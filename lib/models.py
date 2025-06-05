from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        from .models import Freebie
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        from sqlalchemy.orm.session import object_session
        session = object_session(self)
        if session:
            session.add(freebie)
            session.commit()
        return freebie

    @classmethod
    def oldest_company(cls):
        from sqlalchemy.orm.session import object_session
        session = object_session(cls)
        if session:
            return session.query(cls).order_by(cls.founding_year).first()
        return None

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            from sqlalchemy.orm.session import object_session
            session = object_session(self)
            if session:
                session.add(freebie)
                session.commit()
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    dev_id = Column(Integer(), ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)

    dev = relationship('Dev', backref=backref('freebies', cascade='all, delete-orphan'))
    company = relationship('Company', backref=backref('freebies', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Freebie {self.item_name} (${self.value})>'

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."

# Add relationship for Company.devs
Company.devs = relationship(
    'Dev',
    secondary='freebies',
    primaryjoin='Company.id==Freebie.company_id',
    secondaryjoin='Dev.id==Freebie.dev_id',
    backref=backref('companies', lazy='dynamic'),
    viewonly=True,
    lazy='dynamic'
)
