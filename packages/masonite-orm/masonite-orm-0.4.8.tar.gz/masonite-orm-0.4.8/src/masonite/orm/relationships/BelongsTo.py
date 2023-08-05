from .BaseRelationship import BaseRelationship


class BelongsTo(BaseRelationship):
    """Belongs To Relationship Class.
    """

    def apply_query(self, foreign, owner, foreign_key, local_key):
        """Apply the query and return a dictionary to be hydrated

        Arguments:
            foreign {oject} -- The relationship object
            owner {object} -- The current model oject.
            foreign_key {string} -- The column to access on the relationship model.
            local_key {string} -- The column to access on the current model.

        Returns:
            dict -- A dictionary of data which will be hydrated.
        """
        return foreign.where(foreign_key, owner.__attributes__[local_key]).first()

    def fetch_relation(self, relation, foreign, primary_key_value):
        return relation.where(foreign, primary_key_value).first()
