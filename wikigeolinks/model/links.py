#from sqlalchemy import Column, ForeignKey, Integer
#from sqlalchemy.orm import relationship
#from wikigeolinks.model.meta import Base
##from wikigeolinks.model.articles import Article
#
#class Link(Base):
#    __tablename__ = 'links'
#    id_parent = Column(Integer, ForeignKey("articles.id"), primary_key=True)
#    id_child = Column(Integer, ForeignKey("articles.id"), primary_key=True)
#
#    parent_article = relationship("Article", primaryjoin="Article.id == id_parent")
#    child_article = relationship("Article", primaryjoin="Article.id == id_child")
#
