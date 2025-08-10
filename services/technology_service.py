from utilities import db
from models.technology import Technology

class TechnologyService():

    @staticmethod
    def new_technology(data):
        try:
            technology = Technology(
                label=data['label'],
                img=data['img'],
                group=data['group'],
                mode=data['mode']
            )

            db.session.add(technology)
            db.session.commit()

            return technology

        except:
            db.session.rollback()
            raise
        

    @staticmethod
    def update_technology_by_id(data, id: int):
        try:
            technology = Technology.query.get(id)
            
            technology.label = data['label']
            technology.img = data['img']
            technology.group = data['group']
            technology.mode = data['mode']
            
            db.session.commit()

        except:
            db.session.rollback()
            raise


    @staticmethod
    def get_all_technologys():
        try:
            technologies = Technology.query.all()
            
            if not technologies:
                return None
            
            return technologies
        
        except:
            raise


    @staticmethod
    def get_technology_by_id(id: int):
        try:
            technology = Technology.query.get(id)
            
            if not technology:
                return None
            
            return technology

        except:
            raise


    @staticmethod
    def get_technologies_by_group(group: str):
        try:
            technologies = Technology.query.filter(Technology.group == group).all()
            
            if not technologies:
                return None
            
            return technologies
        
        except:
            raise


    @staticmethod
    def delete_technology_by_id(id: int):
        try:
            technology = Technology.query.get(id)
            if not technology:
                return None
            
            temp = technology

            db.session.delete(technology)
            db.session.commit()

            return temp
            
        except:
            db.session.rollback()
            raise


    # @staticmethod
    # def delete_all_technologys():