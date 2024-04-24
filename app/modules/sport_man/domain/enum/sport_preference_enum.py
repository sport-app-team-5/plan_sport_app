from enum import Enum


class SportPreference(Enum):
    ATHLETICS = "Atletismo"
    CYCLING = "Ciclismo"


class SporExperience(Enum):
    SI = "Si"
    NO = "No"


class SportDedication(Enum):
    ONETHREEHOURS = "1 a 3 horas"
    THREEFIVEHOURS = "3 a 5 horas"
    FIVESEVENHOURS = "5 a 7 horas"
    SEVENEIGHTHOURS = "7 a 8 horas"
    MOREEIGHTHOURS = "Mas de 8 horas"
