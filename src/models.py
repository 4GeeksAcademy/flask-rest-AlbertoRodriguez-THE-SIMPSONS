from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_table = Table(
    "favorite",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

favoriteLocation_table = Table(
    "favoriteLocation",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("locations.id"), primary_key=True)
)


class User(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    favorites: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favorite_table,
        back_populates="favorite_by"
    )

    favorite_locations: Mapped[list["Locations"]] = relationship(
        "Locations",
        secondary=favoriteLocation_table,
        back_populates="favorite_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [character.serialize() for character in self.favorites],
            "favorite_locations": [locations.serialize() for locations in self.favorite_locations]

        }


class Character(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    quote: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)

    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_table,
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "quote": self.quote,
            "image": self.image,
            # do not serialize the password, its a security breach
        }


class Locations (db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    town: Mapped[str] = mapped_column(String(120), nullable=True)
    use: Mapped[str] = mapped_column(String(120), nullable=True)

    favorite_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favoriteLocation_table,
        back_populates="favorite_locations"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "town": self.town,
            "use": self.use


            # do not serialize the password, its a security breach
        }
