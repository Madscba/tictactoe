from pydantic import BaseModel

class VisualizeBoard(BaseModel):
    def visualize(self, board) -> None:
        pass

class VisualizeBoardInTerminal(VisualizeBoard):
    def visualize(self, board):
        print(board)

