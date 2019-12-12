from predicthq.endpoints.schemas import Model, StringType, DateTimeType, ModelType


class Industry(Model):

    id = StringType()
    name = StringType()


class Account(Model):

    id = StringType()
    name = StringType()
    description = StringType()
    industry = ModelType(Industry)
    created_at = DateTimeType()
    updated_at = DateTimeType()
