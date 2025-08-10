from utilities import db
from models.post import Post

class PostService():

    @staticmethod
    def new_post(data):
        try:
            post = Post(
                label=data['label'],
                text=data['text'],
                img=data['img'],
                link=data['link'],
                date=data['date'],
                mode=data['mode']
            )

            db.session.add(post)
            db.session.commit()

            return post

        except:
            db.session.rollback()
            raise
        

    @staticmethod
    def update_post_by_id(data, id: int):
        try:
            post = Post.query.get(id)
            
            post.label = data['label']
            post.text = data['text']
            post.img = data['img']
            post.link = data['link']
            post.date = data['date']
            post.mode = data['mode']
            
            db.session.commit()

        except:
            db.session.rollback()
            raise


    @staticmethod
    def get_all_posts():
        try:
            posts = Post.query.all()
            
            if not posts:
                return None
            
            return posts
        
        except:
            raise


    @staticmethod
    def get_post_by_id(id: int):
        try:
            post = Post.query.get(id)
            
            if not post:
                return None
            
            return post

        except:
            raise


    @staticmethod
    def delete_post_by_id(id: int):
        try:
            post = Post.query.get(id)
            if not post:
                return None
            
            temp = post

            db.session.delete(post)
            db.session.commit()

            return temp
            
        except:
            db.session.rollback()
            raise


    # @staticmethod
    # def delete_all_posts():