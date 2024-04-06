from abc import ABC
from app.seedwork.domain.repositories import Repository

class StartSessionRepository(Repository, ABC):
    ...

class StopSessionRepository(Repository, ABC):
    ...
    
class RegisterSessionRepository(Repository, ABC):
    ...
