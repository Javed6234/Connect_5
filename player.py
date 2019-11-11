class Player:
    def __init__(self, player_id, disc, conn):
        self.id = player_id
        self.disc = disc
        self.connection = conn

    def get_id(self):
        return self.id

    def get_disc(self):
        return self.disc

    def get_connection(self):
        return self.connection
