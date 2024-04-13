from typing import List
from sqlalchemy.orm import Session
from app.modules.allergy.domain.entities import Allergy



def allergies_seed(db: Session):
    allergies_to_create = [
        Allergy(name="Lactose", description="Allergy to lactose"),
        Allergy(name="Gluten", description="Allergy to gluten"),
        Allergy(name="Peanuts", description="Allergy to peanuts"),
        Allergy(name="Shellfish", description="Allergy to shellfish"),
        Allergy(name="Soy", description="Allergy to soy"),
        Allergy(name="Eggs", description="Allergy to eggs"),
        Allergy(name="Fish", description="Allergy to fish"),
        Allergy(name="Tree nuts", description="Allergy to tree nuts"),
        Allergy(name="Milk", description="Allergy to milk"),
        Allergy(name="Wheat", description="Allergy to wheat"),
        Allergy(name="Sesame", description="Allergy to sesame"),
        Allergy(name="Mustard", description="Allergy to mustard"),
        Allergy(name="Celery", description="Allergy to celery"),
        Allergy(name="Sulfites", description="Allergy to sulfites"),
        Allergy(name="Lupin", description="Allergy to lupin"),
        Allergy(name="Molluscs", description="Allergy to molluscs"),
        Allergy(name="Corn", description="Allergy to corn"),
        Allergy(name="Meat", description="Allergy to meat"),
        Allergy(name="Chicken", description="Allergy to chicken"),
        Allergy(name="Beef", description="Allergy to beef"),
        Allergy(name="Pork", description="Allergy to pork"),
        Allergy(name="Rice", description="Allergy to rice"),
        Allergy(name="Pasta", description="Allergy to pasta"),
        Allergy(name="Sugar", description="Allergy to sugar"),
        Allergy(name="Salt", description="Allergy to salt"),
        Allergy(name="Pepper", description="Allergy to pepper"),
        Allergy(name="Cinnamon", description="Allergy to cinnamon"),
        Allergy(name="Garlic", description="Allergy to garlic"),
        Allergy(name="Onion", description="Allergy to onion"),
        Allergy(name="Tomato", description="Allergy to tomato"),
        Allergy(name="Potato", description="Allergy to potato"),
        Allergy(name="Carrot", description="Allergy to carrot"),
        Allergy(name="Broccoli", description="Allergy to broccoli"),
        Allergy(name="Spinach", description="Allergy to spinach"),
        Allergy(name="Lettuce", description="Allergy to lettuce"),
        Allergy(name="Cabbage", description="Allergy to cabbage"),
        Allergy(name="Cauliflower", description="Allergy to cauliflower"),
        Allergy(name="Pumpkin", description="Allergy to pumpkin"),
        Allergy(name="Zucchini", description="Allergy to zucchini"),
        Allergy(name="Eggplant", description="Allergy to eggplant"),
        Allergy(name="Cucumber", description="Allergy to cucumber"),
        Allergy(name="Peas", description="Allergy to peas"),
        Allergy(name="Beans", description="Allergy to beans"),
        Allergy(name="Lentils", description="Allergy to lentils"),
        Allergy(name="Chickpeas", description="Allergy to chickpeas"),
        Allergy(name="Soybeans", description="Allergy to soybeans"),
        Allergy(name="Almonds", description="Allergy to almonds"),
        Allergy(name="Hazelnuts", description="Allergy to hazelnuts"),
        Allergy(name="Walnuts", description="Allergy to walnuts"),
        Allergy(name="Pistachios", description="Allergy to pistachios"),
        Allergy(name="Cashews", description="Allergy to cashews")
    ]
    create_or_update(db, allergies_to_create)
    db.commit()


def create_or_update(db: Session, allergies: List[Allergy]):
    for allergy in allergies:
        allergy_db = db.query(Allergy).filter_by(name=allergy.name).first()

        if allergy_db:
            allergy_db.description = allergy.description
            allergy_db.name = allergy.name
        else:
            db.add(allergy)
