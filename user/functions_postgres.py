import uuid
from user.postgres.models_postgres import relations_table, users_table, conn
from sqlalchemy import select


class PostgresTools:

    def get_list(self, cursor):
        result = []
        for row in cursor:
            row2 = list(map(str, list(row)))
            result.append(f'{row2[1]} -> {row2[2]} = {row2[3]}')
        return result

    def user_exists(self, username: str):
        if username != '':
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
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.user2 == username_friend))
            if_result = conn.execute(query_if)
            conn.commit()
            return if_result

    def relation_exists(self, username: str, username_friend: str):
        if_result = self.get_relation(username, username_friend)
        access = ""
        if if_result is not None:
            for row in if_result:
                access += str(row)
        return access

    def get_users(self):
        select_requests = conn.execute(select(users_table.columns.username)).fetchall()
        conn.commit()
        result = []
        for row in select_requests:
            row2 = list(map(str, list(row)))
            result.append(row2)
        return result

    def get_relations(self):
        select_requests = conn.execute(select(relations_table)).fetchall()
        conn.commit()
        result = self.get_list(select_requests)
        return result

    def create_user(self, username: str):
        if (not (self.user_exists(username))) and (username != ''):
            create_user = users_table.insert().values(id=uuid.uuid4(), username=username)
            conn.execute(create_user)
            conn.commit()

    def send_friendship(self, user1: str, user2: str):
        if user1 != '' and user2 != '':
            if "outgoing" in self.relation_exists(user2, user1):
                update_relation1 = relations_table.update().where(
                    ((relations_table.columns.user1 == user2) & (relations_table.columns.user2 == user1))).values(
                    status='friend')
                update_relation2 = relations_table.update().where(
                    ((relations_table.columns.user1 == user1) & (relations_table.columns.user2 == user2))).values(
                    status='friend')
                conn.execute(update_relation1)
                conn.execute(update_relation2)
                conn.commit()
            elif self.relation_exists(user1, user2) == "":
                create_relation1 = relations_table.insert().values(user1=user1, user2=user2,
                                                                   status='outgoing request')
                create_relation2 = relations_table.insert().values(user1=user2, user2=user1,
                                                                   status='incoming request')
                conn.execute(create_relation1)
                conn.execute(create_relation2)
                conn.commit()

    def accept_friendship(self, user1: str, user2: str):
        string = self.relation_exists(user1, user2)
        if ("incoming" in string) or ("follower" in string) and user1 != '' and user2 != '':
            update_relation1 = relations_table.update().where(
                ((relations_table.columns.user1 == user1) & (relations_table.columns.user2 == user2))).values(
                status='friend')
            update_relation2 = relations_table.update().where(
                ((relations_table.columns.user1 == user2) & (relations_table.columns.user2 == user1))).values(
                status='friend')
            conn.execute(update_relation1)
            conn.execute(update_relation2)
            conn.commit()

    def reject_friendship(self, username: str, username_friend: str):
        if "incoming" in self.relation_exists(username, username_friend):
            update_relation = relations_table.update().where(
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.user2 == username_friend)).values(
                status='follower')
            conn.execute(update_relation)
            conn.commit()

    def delete_friendship(self, username: str, username_friend: str):
        if "friend" in self.relation_exists(username, username_friend):
            update_relation1 = relations_table.update().where(
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.user2 == username_friend)).values(
                status='follower')
            update_relation2 = relations_table.update().where(
                (relations_table.columns.user1 == username_friend) & (
                        relations_table.columns.user2 == username)).values(
                status='outgoing request')
            conn.execute(update_relation1)
            conn.execute(update_relation2)
            conn.commit()

    def get_outgoing_request(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table).where(
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.status == 'outgoing request'))).fetchall()
            conn.commit()
            result = self.get_list(select_request)
            return result

    def get_incoming_request(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table).where(
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.status == 'incoming request'))).fetchall()
            conn.commit()
            result = self.get_list(select_request)
            return result

    def get_friends(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table).where(
                (relations_table.columns.user1 == username) & (relations_table.columns.status == 'friend'))).fetchall()
            conn.commit()
            result = self.get_list(select_request)
            return result

    def get_followers(self, username: str):
        if self.user_exists(username):
            select_request = conn.execute(select(relations_table).where(
                (relations_table.columns.user1 == username) & (
                        relations_table.columns.status == 'follower'))).fetchall()
            conn.commit()
            result = self.get_list(select_request)
            return result

    def get_status(self, user1: str, user2: str):
        if self.user_exists(user1) and self.user_exists(user2):
            if self.relation_exists(user1, user2) != "":
                select_requests = conn.execute(select(relations_table).where(
                    (relations_table.columns.user1 == user1) & (relations_table.columns.user2 == user2))).fetchall()
                conn.commit()
                result = self.get_list(select_requests)
                return result
            else:
                return [f'{user1} -> {user2} = nothing']
