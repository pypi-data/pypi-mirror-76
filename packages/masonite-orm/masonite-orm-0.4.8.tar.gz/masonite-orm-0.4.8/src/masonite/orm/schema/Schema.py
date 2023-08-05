from ..connections.ConnectionFactory import ConnectionFactory
from ..blueprint import Blueprint


class Schema:

    _grammar = None
    _default_string_length = "255"
    _dry = False

    @classmethod
    def on(cls, connection):
        """Change the connection from the default connection

        Arguments:
            connection {string} -- A connection string like 'mysql' or 'mssql'.
                It will be made with the connection factory.

        Returns:
            cls
        """
        cls._connection = ConnectionFactory().make(connection)
        return cls

    @classmethod
    def dry(cls):
        """Change the connection from the default connection

        Arguments:
            connection {string} -- A connection string like 'mysql' or 'mssql'.
                It will be made with the connection factory.

        Returns:
            cls
        """
        cls._dry = True
        return cls

    @classmethod
    def create(cls, table):
        """Sets the table and returns the blueprint.

        This should be used as a context manager.

        Arguments:
            table {string} -- The name of a table like 'users'

        Returns:
            masonite.orm.blueprint.Blueprint -- The Masonite ORM blueprint object.
        """
        cls._table = table

        return Blueprint(
            cls._connection.get_grammar(),
            connection=cls._connection,
            table=table,
            action="create",
            default_string_length=cls._default_string_length,
            dry=cls._dry,
        )

    @classmethod
    def table(cls, table):
        """Sets the table and returns the blueprint.

        This should be used as a context manager.

        Arguments:
            table {string} -- The name of a table like 'users'

        Returns:
            masonite.orm.blueprint.Blueprint -- The Masonite ORM blueprint object.
        """
        cls._table = table
        return Blueprint(
            cls._connection.get_grammar(),
            table=table,
            action="alter",
            default_string_length=cls._default_string_length,
            dry=cls._dry,
        )

    @classmethod
    def has_column(cls, table, column, query_only=False):
        """Checks if the a table has a specific column

        Arguments:
            table {string} -- The name of a table like 'users'

        Returns:
            masonite.orm.blueprint.Blueprint -- The Masonite ORM blueprint object.
        """
        grammar = cls._connection.get_grammar()(table=table)
        query = grammar.column_exists(column).to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))

    @classmethod
    def set_default_string_length(cls, length):
        cls._default_string_length = length
        return cls

    @classmethod
    def drop_table(cls, table, query_only=False):
        grammar = cls._connection.get_grammar()(table=table)
        query = grammar.drop_table(table).to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))

    @classmethod
    def drop(cls, *args, **kwargs):
        return cls.drop_table(*args, **kwargs)

    @classmethod
    def drop_table_if_exists(cls, table, exists=False, query_only=True):
        grammar = cls._connection.get_grammar()(table=table)
        query = grammar.drop_table_if_exists(table).to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))

    @classmethod
    def rename(cls, table, new_name, query_only=False):
        grammar = cls._connection.get_grammar()(table=table)
        query = grammar.rename_table(
            current_table_name=table, new_table_name=new_name
        ).to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))

    @classmethod
    def truncate(cls, table, query_only=True):
        grammar = cls._connection.get_grammar()(table=table)
        query = grammar.truncate_table(table=table).to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))

    @classmethod
    def has_table(cls, table, query_only=False):
        """Checks if the a database has a specific table
        Arguments:
            table {string} -- The name of a table like 'users'
        Returns:
            masonite.orm.blueprint.Blueprint -- The Masonite ORM blueprint object.
        """
        grammar = cls._connection.get_grammar()(
            table=table, database=cls._connection.get_database_name()
        )
        query = grammar.table_exists().to_sql()
        if query_only:
            return query
        return bool(cls._connection().make_connection().query(query, ()))
