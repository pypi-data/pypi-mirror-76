from catcher.steps.external_step import ExternalStep
from catcher.steps.step import update_variables

from catcher_modules.database import SqlAlchemyDb


class Oracle(ExternalStep, SqlAlchemyDb):
    """
    :Input:

    :conf:  oracle configuration. Can be a single line string or object. Dialect is not mandatory. **Required**.

    - dbname: name of the database to connect to
    - user: database user
    - host: database host
    - password: user's password
    - port: database port

    :query: query to run. **Required**

    :Examples:

    Select all from test, use object configuration
    ::

        oracle:
          request:
              conf:
                  dbname: test
                  user: user
                  password: password
                  host: localhost
                  port: 1521
              query: 'select count(*) from test'
          register: {documents: '{{ OUTPUT }}'}

    Insert into test, using string configuration
    ::

        oracle:
          request:
              conf: 'user:password@localhost:1521/test'
              query: 'insert into test(id, num) values(3, 3);'

    Insert into test, using string configuration with dialect
    ::

        oracle:
          request:
              conf: 'oracle+cx_oracle://user:password@localhost:1521/test'
              query: 'insert into test(id, num) values(3, 3);'

      """

    @property
    def dialect(self) -> str:
        return "oracle+cx_oracle"

    @update_variables
    def action(self, includes: dict, variables: dict) -> any:
        body = self.simple_input(variables)
        return variables, self.execute(body)
