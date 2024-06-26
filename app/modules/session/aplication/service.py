from sqlalchemy.orm import Session
from app.config.env import env
from app.modules.session.aplication.schemas import RegisterSportsSessionResponseModel, StartSportsSessionRequestModel, \
    StartSportsSessionResponseModel, StopSportsSessionResponseModel
from app.modules.session.aplication.schemas.session_schema import RegisterSportsSessionModel, \
    SportsSessionResponseModel, StopSportsSessionRequestModel
from app.modules.session.domain.repository import RegisterSessionRepository, StartSessionRepository, \
    StopSessionRepository
from app.modules.session.infrastructure.factories import RepositoryFactory
from app.modules.sport_man.aplication.service import SportsManService
from app.seedwork.application.services import Service
import uuid
import boto3
from app.config.env import env


class SessionService(Service):
    def __init__(self):
        self._repository_factory: RepositoryFactory = RepositoryFactory()

    @property
    def repository_factory(self):
        return self._repository_factory

    def start(self, model: StartSportsSessionRequestModel, db: Session,
              user_id: int) -> StartSportsSessionResponseModel:
        repository = self.repository_factory.create_object(StartSessionRepository)
        model.id = str(uuid.uuid4())
        sport_service = SportsManService()
        sportman = sport_service.get_sportsmen_by_id(user_id, db)
        return repository.create(model, db, sportman.id)

    def send_to_pub_sub(self, message: StopSportsSessionRequestModel, topic: str):
        sns_client = boto3.client('sns')
        try:
            sns_client = boto3.client('sns', region_name='us-east-1', 
                           aws_access_key_id=env.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY)
            mensaje_json = message.model_dump_json()
            sns_client.publish(TopicArn=topic, Message=mensaje_json)
        except Exception as e:
            return f'Error: {str(e)}'
        finally:
            sns_client.close()

    def stop(self, user_id: int, model: StopSportsSessionRequestModel, db: Session) -> StopSportsSessionResponseModel:

        sport_service = SportsManService()
        sportman = sport_service.get_sportsmen_by_id(user_id, db)

        model.weight = sportman.weight

        repository = self.repository_factory.create_object(StopSessionRepository)
        self.send_to_pub_sub(model,env.TOPIC_ARN)
        
        repository.update(model.id,model,db)
        sport_indicators_created = repository.create_sport_indicators(model.weight, model,db)        
        sport_profile = sport_service.create_sport_indicators_profile(user_id, sport_indicators_created.ftp, sport_indicators_created.vo2max, sport_indicators_created.time, db)

        repository.update(model.id, model, db)
        sport_indicators_created = repository.create_sport_indicators(model.weight, model, db)
        sport_profile = sport_service.create_sport_indicators_profile(user_id, sport_indicators_created.ftp,
                                                                      sport_indicators_created.vo2max,
                                                                      sport_indicators_created.time, db)

        sportman.sport_profile_id = sport_profile.id
        sport_service.update_sportsmen(sportman.id, sportman, db)
        return sport_indicators_created

    def register(self, model: RegisterSportsSessionModel, db: Session) -> RegisterSportsSessionResponseModel:
        repository = self.repository_factory.create_object(RegisterSessionRepository)
        return repository.create(model, db)

    def get_by_id(self, id_session: int, db: Session) -> SportsSessionResponseModel:
        repository = self.repository_factory.create_object(StartSessionRepository)
        return repository.get_by_id(id_session, db)
