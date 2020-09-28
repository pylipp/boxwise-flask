from datetime import datetime

from peewee import (
    SQL,
    CharField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
)

from boxwise_flask.db import db
from boxwise_flask.models.organisation import Organisation
from boxwise_flask.models.user import User


class Base(db.Model):
    name = CharField(null=True)
    currency_name = CharField(
        column_name="currencyname", constraints=[SQL("DEFAULT 'Tokens'")]
    )

    adult_age = IntegerField(constraints=[SQL("DEFAULT 15")])
    bicycle = IntegerField(constraints=[SQL("DEFAULT 0")])
    bicycle_closingtime = CharField(constraints=[SQL("DEFAULT '17:30'")], null=True)
    bicycle_closingtime_saturday = CharField(
        constraints=[SQL("DEFAULT '16:30'")], null=True
    )
    bicyclerenttime = IntegerField(constraints=[SQL("DEFAULT 120")])
    created = DateTimeField(null=True)
    created_by = ForeignKeyField(
        column_name="created_by", field="id", model=User, null=True
    )

    cyclestart = DateTimeField(default=datetime.now(), null=True)
    daystokeepdeletedpersons = IntegerField(
        constraints=[SQL("DEFAULT 9999")], null=True
    )
    delete_inactive_users = IntegerField(constraints=[SQL("DEFAULT 30")])
    deleted = DateTimeField(null=True)
    dropcapadult = IntegerField(constraints=[SQL("DEFAULT 99999")])
    dropcapchild = IntegerField(constraints=[SQL("DEFAULT 99999")])
    dropsperadult = CharField(constraints=[SQL("DEFAULT '100'")])
    dropsperchild = CharField(constraints=[SQL("DEFAULT '100'")])
    extraportion = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    familyidentifier = CharField(constraints=[SQL("DEFAULT 'Container'")])
    food = IntegerField(constraints=[SQL("DEFAULT 0")])
    idcard = IntegerField(constraints=[SQL("DEFAULT 0")])
    laundry = IntegerField(constraints=[SQL("DEFAULT 0")])
    laundry_cyclestart = DateField(default=datetime.now(), null=True)
    market = IntegerField(constraints=[SQL("DEFAULT 1")])
    maxfooddrops_adult = IntegerField(constraints=[SQL("DEFAULT 25")], null=True)
    maxfooddrops_child = IntegerField(constraints=[SQL("DEFAULT 25")], null=True)
    modified = DateTimeField(null=True)
    modified_by = ForeignKeyField(
        backref="cms_users_modified_by_set",
        column_name="modified_by",
        field="id",
        model=User,
        null=True,
    )
    organisation = ForeignKeyField(
        column_name="organisation_id", field="id", model=Organisation
    )
    resettokens = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    schedulebreak = CharField(constraints=[SQL("DEFAULT '1'")])
    schedulebreakduration = CharField(constraints=[SQL("DEFAULT '1'")])
    schedulebreakstart = CharField(constraints=[SQL("DEFAULT '13:00'")])
    schedulestart = CharField(constraints=[SQL("DEFAULT '11:00'")])
    schedulestop = CharField(constraints=[SQL("DEFAULT '17:00'")])
    scheduletimeslot = CharField(constraints=[SQL("DEFAULT '0.5'")])
    seq = IntegerField()
    workshop = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "camps"

    def __str__(self):
        return (
            str(self.id)
            + " "
            + str(self.organisation_id)
            + " "
            + self.name
            + " "
            + self.currency_name
        )

    @staticmethod
    def get_all_bases():
        return Base.select().order_by(Base.name)

    @staticmethod
    def get_for_organisation(org_id):
        return Base.select().where(Base.organisation_id == org_id)

    @staticmethod
    def get_from_id(base_id):
        base = Base.select().where(Base.id == base_id).get()
        return base
