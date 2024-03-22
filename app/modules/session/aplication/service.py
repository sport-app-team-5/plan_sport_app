from typing import List
from sqlalchemy.orm import Session
from app.modules.session.aplication.schemas import RegisterSportsSessionResponseModel, StartSportsSessionRequestModel, StartSportsSessionResponseModel, StopSportsSessionResponseModel
from app.modules.session.aplication.schemas.session_schema import RegisterSportsSessionModel, StopSportsSessionRequestModel
from app.modules.session.domain.repository import RegisterSessionRepository, StartSessionRepository, StopSessionRepository
from app.modules.session.infrastructure.factories import RepositoryFactory
from app.seedwork.aplicacion.services import Service
import uuid
import boto3
from config import settings 

class SessionService(Service):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    def start(self, model: StartSportsSessionRequestModel, db: Session) -> StartSportsSessionResponseModel:
        repository = self.repository_factory.create_object(StartSessionRepository)
        model.id = str(uuid.uuid4())
        return repository.create(model, db)
    
    def send_to_pub_sub(self, message: StopSportsSessionRequestModel, topic: str):
        try:
            sns_client = boto3.client('sns', region_name='us-east-1', 
                           aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            mensaje_json = message.model_dump_json()
            sns_client.publish(TopicArn=topic, Message=mensaje_json)
        
        except Exception as e:
            return f'Error: {str(e)}'
        finally:
            sns_client.close()
            sns_client = None

    def stop(self,model: StopSportsSessionRequestModel, db: Session) ->StopSportsSessionResponseModel:
        repository = self.repository_factory.create_object(StopSessionRepository)
        #self.send_to_pub_sub(model,settings.TOPIC_ARN) #TODO fix integration with lambda, the name of the table session change by monitoring
        return repository.update(model.id,model,db)

    def register(self,model: RegisterSportsSessionModel, db: Session) -> RegisterSportsSessionResponseModel:
        repository = self.repository_factory.create_object(RegisterSessionRepository)
        return repository.create(model, db)
