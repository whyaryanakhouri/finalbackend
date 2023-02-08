from peewee import *
import datetime

DATABASE='tweepee1.db'

database=SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database=database

class User(BaseModel):
    username= CharField(unique=True,primary_key=True)
    password= CharField()
    email= CharField()
    profilepic=CharField()

class Category(BaseModel):
    name=CharField(unique=True)

class Authentication(BaseModel):
    username= ForeignKeyField(User, to_field="username")
    token= CharField()




class Article(BaseModel):
    content=CharField()
    name=CharField()
    synopsis=CharField()
    thumbnail=CharField()
    author= ForeignKeyField(User, to_field="username")
    category= ForeignKeyField(Category, to_field="id")
    createdat= DateTimeField(default=datetime.datetime.now)
    updatedat= DateTimeField(default=datetime.datetime.now)
    numberoflikes= IntegerField(default=0)
    numberofcomments= IntegerField(default=0)

# class Likes(BaseModel):
#     postid=ForeignKeyField(Article, to_field="id")
#     userid=ForeignKeyField(User,to_field="username")

def create_tables():
    database.connect()
    database.create_tables([User],safe=True)
    database.create_tables([Category],safe=True)
    database.create_tables([Article],safe=True)
    database.create_tables([Authentication],safe=True)
   # database.create_tables([Likes],safe=True)
    database.close()

# create_tables()

# user=User.create(username="Aryan",password="whyaryanakhouri",
# email="aryanakhouri9@gmail.com", profilepic="dummy text")
# User.create(username="Nitish",password="whynitishkumar",
# email="nitishkumar8@gmail.com", profilepic="dummy text")
# User.create(username="Roshan",password="whyroshanoraon",
# email="roshanoraon7@gmail.com", profilepic="dummy text")
# User.create(username="Jatin",password="whyjatinchoubisa",
# email="jatinchoubisa6@gmail.com", profilepic="dummy text")
# user.save()

# category=Category.create(name="Design")
# Category.create(name="Product")
# Category.create(name="Software Development")
# Category.create(name="Customer Success")
# Category.create(name="Leadership")
# Category.create(name="Management")

# article=Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "UX review presentations",synopsis="How do you create compelling presentations that wow your colleagues and impress your managers?",thumbnail="dummyurl", author="Aryan", category="1", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "Migrating to linear 101",synopsis="Linear helps streamline software projects, sprints, tasks, and bug tracking. Here's how to get text",thumbnail="dummyurl", author="Aryan", category="4", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "Building your API Stack",synopsis="The rise of RESTful APIs has been met by a rise in tools for creating, testing and managing them.",thumbnail="dummyurl", author="Nitish", category="3", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "Bill Walsh leadership lessons",synopsis="Like to know the sequence of transforming a 2-14 team into a 3x Super Bowl winning Dynasty?",thumbnail="dummyurl", author="Jatin", category="5", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "PM mental models",synopsis="Mental models are simple expressions of complex processes or relationships",thumbnail="dummyurl", author="Roshan", category="2", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "What is Wireframing?",synopsis="Introduction to Wireframing and its Principles. Learn from the best in the industry",thumbnail="dummyurl", author="Aryan", category="1", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "How collaboration makes us better designers",synopsis="Collaboration can make our teams stronger, and our individual designs better",thumbnail="dummyurl", author="Jatin", category="6", numberoflikes=0, numberofcomments=0)
# Article.create(content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",name= "Our top 10 Javascript frameworks to use",synopsis="JavaScript frameworks make development easy with extensive features and functionalities",thumbnail="dummyurl", author="Nitish", category="3", numberoflikes=0, numberofcomments=0)

# article.save()
from fastapi import FastAPI, Request
from typing import List
import bcrypt,peewee

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi import Form, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


import uuid

app=FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/readarticle/{x}")
def func(x):
    h=Article.select()
    for i in h:
        if i.id==int(x):
            return i.content

# @app.post("/createarticle")
# async def func(request: Request):
#     req= await request.json()
#     content=req.get("content")
#     name=req.get("name")
#     synopsis=req.get("synopsis")
#     thumbnail=req.get("thumbnail")
#     author=req.get("author")
#     category=req.get("category")
#     a=Article.create(content=content,name=name,synopsis=synopsis,thumbnail=thumbnail, author=author, category=category)
#     a.save()
#     return {"article": "added"}

@app.post("/create_article")
async def create_post(request: Request):
    request_data = await request.form()
    token = request.headers.get("Authorizationn")
    name = request_data.get("name")
    content = request_data.get("content")
    category = request_data.get("category")
    synopsis = request_data.get("synopsis")
    thumbnail = request_data.get("thumbnail")
    print(name,content,category,synopsis,thumbnail)
    

    try:
        authentication = Authentication.get(Authentication.token == token)
        user = authentication.username
    except Authentication.DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid Token")

    try:
        new_article = Article.create(
            author = user,
            name=name,
            content=content,
            category=category,
            synopsis = synopsis,
            thumbnail = thumbnail       
        )
        new_article.save()
    except peewee.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error creating post")

    return {"message": "Post created successfully"}

@app.get("/writearticle")
async def func():
    content = """
<body>
<form action="/createarticle" enctype="multipart/form-data" method="post">
Enter Content:
<input name="content" type="text"><br>
Enter Name:
<input name="name" type="text"><br>
Enter Synopsis:
<input name="synopsis" type="text"><br>
Enter Thumbnail:
<input name="thumbnail" type="text"><br>
Enter Author:
<input name="author" type="text"><br>
Enter Category_id:
<input name="category" type="number"><br>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.delete("/deletearticle/{x}")
async def funct(x): 
    try:
        article=Article.get(Article.id==x)
        query = Article.delete().where(Article.id ==int(x))
        query.execute()
        return {"post": "deleted"}
    except Article.DoesNotExist:
        return {"message": "post does not exist"}



@app.get("/editarticle")
async def func():
    content = """
<body>
<form action="/articles" enctype="multipart/form-data" method="put">
Enter Article ID:
<input name="article_id" type="number"><br>
Enter Title:
<input name="title" type="text"><br>
Enter Content:
<input name="text" type="text"><br>
Enter Category ID:
<input name="category_name" type="number"><br>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.put("/articles/{article_id}")
async def update_article(request:Request, article_id:int):
    req= await request.json()
    k=Article.select()
    for i in k:
        if(i.id==article_id):
            title=req.get("name")
            text=req.get("content")
            category_name=req.get("category_id")
            i.name=title
            i.content=text
            i.category_id=category_name
            i.updatedat= datetime.datetime.now()
            i.save()
            return {"article": "updated"}
    return {"article": "not found"}
    
    


@app.get("/displaynames/{x}")
async def func(x):
    a=[]
    k=Article.select()
    for i in k:
        if i.category_id==int(x):
            a.append(i.name)
    return a

@app.get("/allarticles")
def get_articles():
    articles = Article.select()
    a=[]
    for article in articles:
        a.append({"id":article.__data__['id'],"content":article.__data__['content'],"name": article.__data__['name'] ,"synopsis": article.__data__['synopsis'],"thumbnail":article.__data__['thumbnail'],"author_id": article.__data__['author'] ,"category_id": article.__data__['category'],"createdat": article.__data__['createdat'] ,"updatedat": article.__data__['updatedat'],"numberoflikes": article.__data__['numberoflikes'] ,"numberofcomments": article.__data__['numberofcomments']})
    return a


#edit profile

@app.put("/editprofile/{username}")
async def func(request:Request,username: str):
    try:
        req= await request.json()
        profile=User.get(User.username==username)
        profile.username= req.get("username")
        profile.email= req.get("email")
        profile.profilepic= req.get("profilepic")
        profile.save()
        return {"Message": "profile updated"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="Profile not found")

#login signup
@app.post("/login")
async def login(request : Request):
    request_data = await request.json()
    username = request_data.get("username")
    password = request_data.get("password")

    try:
        user = User.get(User.username == username)

        bytes = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        
        hash = bcrypt.hashpw(bytes, salt)

        if User.password == hash:
            token = str(uuid.uuid4())
            try:
                a=Authentication.get(Authentication.username==username)
                a.token = token
                a.save()
                return{"message": "Login successful", "token": token}
            except Authentication.DoesNotExist:
                Authentication.create(username=user, token=token)
                return {"message": "Login successful", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="Username not found")

@app.post("/sign-up")
async def register(request : Request):
    request_data = await request.json()
    username = request_data.get("username")
    password = request_data.get("password")
    email = request_data.get("email")
    pp = request_data.get("profilepic")
    bytes = password.encode('utf-8')
        
    salt = bcrypt.gensalt()
    
    hash = bcrypt.hashpw(bytes, salt)

    try:
        new_user = User.create(username = username, email = email, password = hash,profilepic = pp)
        new_user.save()
    except peewee.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    token = str(uuid.uuid4())
    a=Authentication.create(username=new_user, token=token)
    a.save()
    return {"message": "User registered", "token": token}


#search article
@app.get("/searcharticle/{x}")
async def func(x : str):
    a=[]
    k=Article.select().where(Article.name.startswith(x))
    for i in k:
        a.append(i.name)
    return a

#category filter
@app.get("/categoryfilter/{x}")
async def func(x: int):
    k=Article.select().where(Article.category==x)
    a=[]
    for i in k:  
        a.append(i.name)
    return a

#author filter
@app.get("/authorfilter/{x}")
async def func(x: str):
    k=Article.select().where(Article.author==x)
    a=[]
    for i in k:  
        a.append(i._data_['name'])
    return a
#like dislike
@app.put("/increaselikes/{x}")
async def func(x: int):
    k=Article.select()
    for i in k:
        if i.id==x:
            i.numberoflikes = i.numberoflikes + 1
            i.save()
            return {"post": "was liked"}

@app.put("/decreaselikes/{x}")
async def func(x: int):
    k=Article.select()
    for i in k:
        if i.id==x:
            i.numberoflikes = i.numberoflikes - 1
            i.save()
            return {"post": "was unliked"}

#most liked
@app.get("/mostliked")
async def func():
    k=Article.select()
    s=k[0].numberoflikes
    l=0
    for i in k:
        if i.numberoflikes>s:
            s=i.numberoflikes
            l=i.id
    return l