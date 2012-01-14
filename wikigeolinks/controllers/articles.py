from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from wikigeolinks.lib.base import BaseController
from wikigeolinks.model.articles import Article
from wikigeolinks.model.meta import Session

from mapfish.protocol import Protocol, create_default_filter
from mapfish.decorators import geojsonify

from geojson import FeatureCollection



class CustomProtocol(Protocol):
    """ Custom protocol to support limits on read requests"""
    def read(self, request, filter=None, id=None, limit=None):
        """ Build a query based on the filter or the idenfier, send the query
        to the database, and return a Feature or a FeatureCollection. """
        ret = None
        if id is not None:
            o = self.Session.query(self.mapped_class).get(id)
            if o is None:
                abort(404)
            ret = self._filter_attrs(o.toFeature(), request)
        else:
            query = self._query(request, filter, execute=False)
            if limit:
                query = query.limit(limit)
            objs = query.all()
            ret = FeatureCollection(
                    [self._filter_attrs(o.toFeature(), request) \
                        for o in objs if o.geometry is not None])
        return ret




class ArticlesController(BaseController):
    readonly =  True # if set to True, only GET is supported

    def __init__(self):
        self.protocol = CustomProtocol(Session, Article, self.readonly)

    @geojsonify
    def index(self, format='json'):
        """GET /: return all features."""
        # If no filter argument is passed to the protocol index method
        # then the default MapFish filter is used.
        #
        # If you need your own filter with application-specific params 
        # taken into acount, create your own filter and pass it to the
        # protocol read method.
        #
        # E.g.
        #
        # from sqlalchemy.sql import and_
        if format != 'json':
            abort(404)
        limit = request.params.get('limit', 500)
        try:
           limit = int(limit)
        except:
           abort(400)
        if limit > 500:
           limit = 500
        return self.protocol.read(request,limit=limit)

    @geojsonify
    def show(self, id, format='json'):
        """GET /id: Show a specific feature."""
        if format != 'json':
            abort(404)
        return self.protocol.read(request, response, id=id)

    @geojsonify
    def create(self):
        """POST /: Create a new feature."""
        return self.protocol.create(request, response)

    @geojsonify
    def update(self, id):
        """PUT /id: Update an existing feature."""
        return self.protocol.update(request, response, id)

    def delete(self, id):
        """DELETE /id: Delete an existing feature."""
        return self.protocol.delete(request, response, id)

    def count(self):
        """GET /count: Count all features."""
        return self.protocol.count(request)
    
    @geojsonify
    def get_linked(self,id):

        article = Session.query(Article).filter(Article.id == id).first()
        linked_articles = article.get_linked_articles(as_features = True)
        return  linked_articles

    def get_links_count(self,id):

        article = Session.query(Article).filter(Article.id == id).first()
        linked_articles = article.get_linked_articles()
        return  str(len(linked_articles))
