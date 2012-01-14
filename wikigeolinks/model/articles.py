from sqlalchemy import Column, Integer, String, ForeignKey, Unicode
from sqlalchemy.orm import relationship

from geoalchemy import GeometryColumn, Geometry
from geojson import FeatureCollection

from mapfish.sqlalchemygeom import GeometryTableMixIn
from wikigeolinks.model.meta import Session, Base



class Article(Base, GeometryTableMixIn):
    __tablename__ = "articles"
    exported_keys = ["title","links_count"]

    id = Column(Integer, primary_key=True)
    title = Column(Unicode())
    links_count = Column(Integer)
    the_geom = GeometryColumn(Geometry(srid=4326))

#    @property
#    def links_count(self):
#        return len( Session.query(Link).filter(self.id == Link.id_parent).all() )

    def get_linked_articles(self,as_features=False):
        """Return the articles linked from this article"""
        articles = []
        for link in Session.query(Link) \
                            .join((Article,Article.id == Link.id_parent)) \
                            .filter(Article.id == self.id).all():
            if link.child_article:
                if as_features:
                    articles.append(link.child_article.toFeature())
                else:
                    articles.append(link.child_article)
        if articles and as_features:
            return FeatureCollection(articles)
        else:
            return articles
        

class Link(Base):
    __tablename__ = "links"
    id_parent = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_child = Column(Integer, ForeignKey("articles.id"), primary_key=True)

    parent_article = relationship(Article, primaryjoin=Article.id == id_parent)
    child_article = relationship(Article, primaryjoin=Article.id == id_child)

