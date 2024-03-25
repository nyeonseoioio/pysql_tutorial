# actor 테이블의 crud 클래스를 만들기

import psycopg2

class ActorCRUD:
    def __init__(self):
        self.conn_params = {
            'dbname': 'testdb',
            'user': 'postgres',
            'password': '1234',
            'host': 'localhost',
            'port': '5432'
        }
        self.conn = None
        self.connect()

    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    def create_actor(self, first_name, last_name ):
        print(first_name, last_name)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO actor (first_name, last_name)
                VALUES (%s, %s) RETURNING actor_id;
                        """,(first_name,last_name))
            actor_id = cur.fetchone()[0]
            self.conn.commit()
            print(f"배우 '{first_name} {last_name}' 이(가) actor {actor_id}로 추가되었습니다.")
            return actor_id
        
    def read_actor(self, actor):
        """ actor_id 기반으로 배우 정보를 조회 """
        with self.conn.cursor() as cur:
            cur.execute( "SELECT * FROM actor where actor_id = %s;" ,(actor_id,))
            actor = cur.fetchone()
            if actor:
                print(actor)
                return actor
            else:
                print("배우를 찾을 수 없습니다.")
                return None
    def update_actor(self, actor_id, first_name,last_name):
        """actor 정보를 업데이트"""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE actor
                SET first_name = %s, last_name = %s
                WHERE actor_id = %s;
                       """, (first_name, last_name, actor_id))
            self.conn.commit()
            print(f"배우 {first_name} {last_name} 님의 정보가 업데이트되었습니다.")


    def delete_actor(self, actor_id, first_name, last_name):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM actor WHERE actor_id = %s;", (actor_id,))
            self.conn.commit()
            print(f"배우 {first_name} {last_name}의 정보가 삭제되었습니다.")

    def close(self):
        if self.conn:
            self.conn.close()
            print("데이터베이스 연결을 종료합니다.")


actor_crud = ActorCRUD()
actor_id = actor_crud.create_actor("유","또연")
actor_crud.read_actor(actor_id)
actor_crud.update_actor(224, "정","현종")
actor_crud.delete_actor(230,"유","또연")

actor_crud.close()

