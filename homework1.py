class World:
   # def __init__(self):
        



    def ask(self, sentence):
       class Player:
        """
        The player in the Wumpus world
        The player should be able to (1) make inference
        
        """

        def __init__(self, kb):
             self.kb = kb

        def make_inference(self, query):
        
         return False;

        

        if __name__ == '__main__':
            kb = [
                ('NOT','P11')
                ('NOT','W11')
                ('NOT','B11')
                ('NOT','S11')
            ]
            player = Player(kb=kb)
            query = 'P21'
            print(player.make_inferences(query))