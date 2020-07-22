"""Model definitions for database"""
from peewee import (
    CharField,
    CompositeKey,
    DateField,
    DateTimeField,
    IntegerField,
    TextField,
)
from playhouse.shortcuts import model_to_dict

from .app import db


class Person(db.Model):
    firstname = CharField()
    lastname = CharField()
    camp_id = CharField()
    id = CharField()

    def __unicode__(self):
        return self.firstname


class Camps(db.Model):
    id = CharField()
    organisation_id = CharField()
    name = CharField()

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_camps():
        return Camps.select().order_by(Camps.name)


class Cms_Usergroups_Camps(db.Model):
    camp_id = CharField()
    cms_usergroups_id = CharField()

    class Meta:
        # Cms_Usergroups_Camps has no primary key,
        # so we construct a composite to use as one here
        primary_key = CompositeKey("camp_id", "cms_usergroups_id")

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_camp_id(usergroup_id):
        return Cms_Usergroups_Camps.select(Cms_Usergroups_Camps.camp_id).where(
            Cms_Usergroups_Camps.cms_usergroups_id == usergroup_id
        )


class Cms_Users(db.Model):
    id = CharField()
    organisation_id = CharField()
    name = CharField(column_name="naam")
    email = CharField()
    cms_usergroups_id = CharField()
    valid_firstday = DateField()
    valid_lastday = DateField()
    lastlogin = DateTimeField()
    lastaction = DateTimeField()

    def __unicode__(self):
        return self.name

    @staticmethod
    def get_all_users():
        return Cms_Users.select().order_by(Cms_Users.name)

    @staticmethod
    def get_user(email):
        user = Cms_Users.select().where(Cms_Users.email == email).get()
        camps = Cms_Usergroups_Camps.get_camp_id(user.cms_usergroups_id)
        # camps is a peewee ModelSelect (so, many objects).
        # convert to dict 1 at a time,
        # and pull the camp_id from that dict, and put in a list
        user.camp_id = [model_to_dict(item)["camp_id"] for item in camps]

        return user


class Stock(db.Model):
    id = CharField()
    box_id = CharField()
    product_id = IntegerField()
    size_id = IntegerField()
    items = IntegerField()
    location_id = IntegerField()
    qr_id = IntegerField()
    comments: TextField()
    gender: CharField()  # from product table
    deleted: DateTimeField()
    box_state_id: IntegerField()

    def __unicode__(self):
        return self.box_id

    @staticmethod
    def get_box(id):
        box = Stock.select().where(Stock.id == id).get()

        return box
