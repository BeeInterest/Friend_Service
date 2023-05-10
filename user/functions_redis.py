from .functions_postgres import PostgresTools

from .redis.models_redis import Relation, RedisDB


class RedisTools(RedisDB):
    tool = PostgresTools()

    @classmethod
    def get_list(cls, cursor):
        result = []
        for row in cursor:
            row2 = list(map(str, list(row)))
            result.append(row2[0])
        return result

    @classmethod
    def get_request(cls, cursor, status: str):
        result = []
        for row in cursor[0]:
            row2 = list(map(str, list(row)))
            result.extend([f'{row2[1]}_{status}', row2[2]])
        for row in cursor[1:]:
            row2 = list(map(str, list(row)))
            result.append(row2[2])
        return result

    def completion_user(self):
        all_users = self.get_list(self.tool.get_users())
        for row in all_users:
            user = row
            self.set_user(user)

    def completion_relations(self):
        all_relations = []
        for user in self.get_list(self.tool.get_users()):
            all_relations.extend(self.get_request(self.tool.get_outgoing_request(user), 'outgoing'))
        for user in self.get_list(self.tool.get_users()):
            all_relations.extend(self.get_request(self.tool.get_incoming_request(user), 'incoming'))
        for user in self.get_list(self.tool.get_users()):
            all_relations.extend(self.get_request(self.tool.get_incoming_request(user), 'friend'))
        for user in self.get_list(self.tool.get_users()):
            all_relations.extend(self.get_request(self.tool.get_incoming_request(user), 'follower'))
        for row in all_relations:
            relation = Relation(row[0], row[1:])
            self.set_relation(relation)

    def add_relation(self, user: str, user_friend: str):
        relation1 = Relation(f'{user}_outgoing', list(user_friend))
        relation2 = Relation(f'{user}_incoming', list(user_friend))
        self.set_relation(relation1)
        self.set_relation(relation2)
