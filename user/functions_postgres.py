import uuid
from user.postgres.models_postgres import relations_table, users_table, conn
from sqlalchemy import select


class PostgresTools:

    def user_exists(self, username: str):
        query_if = users_table.select().where(
            (users_table.columns.username == username))
        if_result = conn.execute(query_if)
        conn.commit()
        access = ""
        for row in if_result:
            access += str(row)
        if access != "":
            return True
        else:
            return False

    def get_relation(self, username: str, username_friend: str):
        if self.user_exists(username) and self.user_exists(username_friend):
            query_if = relations_table.select().where(
                (relations_table.columns.username == username) & (
                        relations_table.columns.username_friend == username_friend))
            if_result = conn.execute(query_if)
            conn.commit()
            return if_result

    def relation_exists(self, username: str, username_friend: str):
        if_result = self.get_relation(username, username_friend)
        access = ""
        for row in if_result:
            access += str(row)
        return access

    def get_users(self):
        result = conn.execute(select(users_table.columns.username)).fetchall()
        conn.commit()
        return result

    def create_user(self, username: str):
        if not (self.user_exists(username)):
            create_user = users_table.insert().values(id=uuid.uuid4(), username=username)
            conn.execute(create_user)
            conn.commit()

    def send_friendship(self, username: str, username_friend: str):
        #if self.relation_exists(username, username_friend) == "":
            create_relation1 = relations_table.insert(relations_table.columns.username,
                                                      relations_table.columns.username_friend,
                                                      relations_table.columns.status).values(username=username,
                                                                                             username_friend=username_friend,
                                                                                             status='outgoing request')
            create_relation2 = relations_table.insert().values(username=username_friend, username_friend=username,
                                                               status='incoming request')
            conn.execute(create_relation1)
            conn.execute(create_relation2)
            conn.commit()

    def accept_friendship(self, username: str, username_friend: str):
        string = self.relation_exists(username, username_friend)
        if ("incoming" in string) or ("follower" in string):
            update_relation = relations_table.update().where(
                relations_table.columns.username == username and relations_table.columns.username == username_friend).values(
                status='friend')
            conn.execute(update_relation)
            conn.commit()

    def reject_friendship(self, username: str, username_friend: str):
        if "incoming" in self.relation_exists(username, username_friend):
            update_relation = relations_table.update().where(
                relations_table.columns.username == username).values(
                status='follower')
            conn.execute(update_relation)
            conn.commit()

    def delete_friendship(self, username: str, username_friend: str):
        if "friend" in self.relation_exists(username, username_friend):
            update_relation1 = relations_table.update().where(
                relations_table.columns.username == username and relations_table.columns.username == username_friend).values(
                status='follower')
            update_relation2 = relations_table.update().where(
                relations_table.columns.username == username_friend and relations_table.columns.username == username).values(
                status='outgoing request')
            conn.execute(update_relation1)
            conn.execute(update_relation2)
            conn.commit()

    def get_outgoing_request(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table)).where(
                relations_table.columns.username == username and relations_table.columns.status == 'outgoing request').fetchall()
            result = conn.execute(select_request)
            conn.commit()
            return result

    def get_incoming_request(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table)).where(
                relations_table.columns.username == username and relations_table.columns.status == 'incoming request' and
                relations_table.columns.status == 'followers').fetchall()
            result = conn.execute(select_request)
            conn.commit()
            return result

    def get_friends(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table)).where(
                relations_table.columns.username == username and relations_table.columns.status == 'friend').fetchall()
            result = conn.execute(select_request)
            conn.commit()
            return result
