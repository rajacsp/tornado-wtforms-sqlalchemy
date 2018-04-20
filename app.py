import tornado
import tornado.ioloop
import tornado.web
from sqlalchemy import create_engine
from tornado.gen import coroutine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from wtforms_tornado import Form
import wtforms


Base = declarative_base()
engine = create_engine('postgresql://localhost/test')
Base.metadata.create_all(engine)


class PostModel(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    title = Column(String(30))
    description = Column(String(30))

    def __init__(self, name, title, description):
        self.name = name
        self.title = title
        self.description = description

    def __str__(self, name, title, description):
        self.name = name
        self.title = title
        self.description = description

    def __repr__(self, name):
        return "<Projects('%s')>" % (self.name)


class PostForm(Form):
    name = wtforms.StringField(
        'name', validators=[wtforms.validators.DataRequired()])
    title = wtforms.StringField(
        'title', validators=[wtforms.validators.DataRequired()])
    description = wtforms.StringField('description', validators=[
                                      wtforms.validators.DataRequired()])


class AddPost(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        form = PostForm()
        self.render('templates/projectform.html', form=form)

    def post(self):
        form = PostForm(self.request.arguments)
        if form.validate():
            name = self.request.arguments['name']
            title = self.request.arguments['title']
            description = self.request.arguments['description']
            project = PostModel(str(name[0].decode("utf-8")), str(
                title[0].decode("utf-8")), str(description[0].decode("utf-8")))
            print(type(name[0]))
            Session = sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            session.add(project)
            session.commit()
            self.write("Form Succesfully Submited")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/addpost", AddPost),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
