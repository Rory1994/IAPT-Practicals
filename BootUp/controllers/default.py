# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def login():

    form = FORM(LEGEND('Login'), INPUT(_type='text', _name='username', _class = 'input-block-level', _placeholder='username', requires=IS_NOT_EMPTY()),
                 INPUT(_type='password',_name='password', _class = 'input-block-level', _placeholder='password', requires=IS_NOT_EMPTY()), INPUT(_type='submit', _class='btn btn-primary', _value='Login'),
                 A('Register',_href="{{=URL('default','register')}}", _role='button', _class='btn btn-info'))
    if form.process(onvalidation=login_validation).accepted:
        response.flash = 'form accepted'
        user = auth.login_bare(request.vars.username, request.vars.password)
        if(user is False):
            response.flash = DIV("Invalid Username/Password Combination", _class='alert alert-error')
        else:
            redirect(URL('index'))

    return dict(form=form)

def login_validation(form):
    if form.vars.username =="cat":
        form.errors.username= "Hello Cat"
    if form.vars.password == None:
        form.errors.password = "Password can not be empty"

def register():

    return dict()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
