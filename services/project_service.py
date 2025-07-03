from utilities import db
from models.projects import Project

class ProjectService():
    
    @staticmethod
    def new_project(data):
        try:
            project = Project(
                label=data['label'],
                text=data['text'],
                img=data['img'],
                stack=data['stack'],
                link=data['link']
            )

            db.session.add(project)
            db.session.commit()

            return project

        except:
            db.session.rollback()
            raise
        

    @staticmethod
    def update_project_by_id(data, id: int):
        try:
            project = Project.query.get(id)
            
            project.label = data['label']
            project.text = data['text']
            project.img = data['img']
            project.stack = data['stack']
            project.link = data['link']
            
            db.session.commit()

        except:
            db.session.rollback()
            raise


    @staticmethod
    def get_all_projects():
        try:
            projects = Project.query.all()
            
            if not projects:
                return None
            
            return projects
        
        except:
            raise


    @staticmethod
    def get_project_by_id(id: int):
        try:
            project = Project.query.get(id)
            
            if not project:
                return None
            
            return project

        except:
            raise


    @staticmethod
    def delete_project_by_id(id: int):
        try:
            project = Project.query.get(id)
            if not project:
                return None
            
            temp = project

            db.session.delete(project)
            db.session.commit()

            return temp
            
        except:
            db.session.rollback()
            raise


    # @staticmethod
    # def delete_all_projects():
