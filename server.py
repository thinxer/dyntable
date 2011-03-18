#!/usr/bin/env python2

import web
import pymongo
from pymongo.objectid import ObjectId

import conf
import seg

conn = pymongo.Connection()
db = conn[conf.db_name]
objs = db["objs"]
objs.ensure_index('_tags')

urls = (
        '/', 'index',
        '/manage', 'manage',
        '/export', 'export'
        )
render = web.template.render('templates/')

def get_tags(d):
    s = set()
    for c in conf.columns:
        if d.has_key(c):
            s.update(seg.segment(d[c]))
    return list(s)

class index(object):
    def GET(self):
        i = web.input()
        s = i.get('s', None)
        if s:
            o = list(objs.find({"_tags": {"$all": s.split()}}).limit(100))
        else:
            o = list(objs.find().limit(100))
        return render.index(conf.title, conf.columns, o)

    def POST(self):

        def update(d, i):
            for c in conf.columns:
                # input names are not decoded
                u = c.encode('utf8')
                if i.has_key(u):
                    d[c] = i.get(u)
                d['_tags'] = get_tags(d)

        i = web.input()
        a = i.get('__action', None)
        if a == 'add':
            d = {}
            update(d, i)
            o = objs.save(d)
            o = list(objs.find(d))
            return render.index(conf.title, conf.columns, o, 'add')
        elif a == 'update':
            if i.get('_id', None):
                d = objs.find_one(ObjectId(i['_id']))
                if d:
                    update(d, i)
                    oid = objs.save(d)
                    o = [objs.find_one(oid)]
                    return render.index(conf.title, conf.columns, o, 'update')
        elif a == 'delete':
            if i.get('_id', None):
                objs.remove(ObjectId(i['_id']))
                raise web.SeeOther('/')
        raise web.BadRequest()

class manage(object):
    def GET(self):
        return render.manage(
                "%s %s" % (conf.title, 'management'),
                conf.columns)
    def POST(self):
        import string
        i = web.input()
        if i.has_key('columns'):
            cs = i['columns']
            cs = map(string.strip, cs.split(','))
            conf.save_columns(cs)
        raise web.seeother('/manage')

class export(object):
    def GET(self):
        web.header('Content-Type', 'text/csv')
        web.header('Content-Disposition', 'attachment; filename=export.csv')

        # utf8 BOM, needed for m$ excel
        yield '\xef\xbb\xbf'    

        # csv header
        yield ','.join(conf.columns) + "\n"
        # csv data
        for o in objs.find():
            yield ','.join(map(lambda _:o.get(_, ""), conf.columns)) + "\n"

app = web.application(urls, globals())

if __name__ == "__main__": app.run()
