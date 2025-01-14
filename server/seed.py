
from models import db, PetSitter
from app import app



pet_sitters = [
    PetSitter(name='John Doe', location='123 Main St, Baton Rouge, LA, 70801', price=55),
    PetSitter(name='Jane Smith', location='456 Elm St, Baton Rouge, LA, 70802', price=60),
    PetSitter(name='Jim Brown', location='789 Oak St, Baton Rouge, LA, 70803', price=65),
    PetSitter(name='Mary Green', location='101 Pine St, Baton Rouge, LA, 70804', price=50),
    PetSitter(name='Tom White', location='202 Cedar St, Baton Rouge, LA, 70805', price=55),
    PetSitter(name='Emily Black', location='303 Birch St, Baton Rouge, LA, 70806', price=60),
    PetSitter(name='Chris Blue', location='404 Maple St, Baton Rouge, LA, 70807', price=65),
    PetSitter(name='Patricia Red', location='505 Ash St, Baton Rouge, LA, 70808', price=70),
    PetSitter(name='Michael Yellow', location='606 Redwood St, Baton Rouge, LA, 70809', price=55),
    PetSitter(name='Linda Purple', location='707 Pinecone St, Baton Rouge, LA, 70810', price=60),
]

with app.app_context():
    db.session.query(PetSitter).delete()  # This deletes all pet sitters in the table
    db.session.commit()
    for sitter in pet_sitters:
        db.session.add(sitter)
    db.session.commit()
    for sitter in PetSitter.query.all():
        print(sitter.name, sitter.location, sitter.price)

        