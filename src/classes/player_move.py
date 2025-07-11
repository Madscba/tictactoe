from pydantic import BaseModel, Field


class Move(BaseModel):
    to_row: int
    to_col: int
    from_row: int = Field(default=-1)
    from_col: int = Field(default=-1)
    move_existing_piece: bool = False

    def isInValidRange(self) -> bool:
        attrs = [self.to_row, self.to_col]
        attrs_names = ["to_row", "to_col"]
        if self.move_existing_piece:
            attrs.extend([self.from_row, self.from_col])
            attrs_names.extend(["from_row", "from_col"])

        for attr_name, attr in zip(attrs_names, attrs):
            if not attr in [0, 1, 2]:
                print(
                    f"attr {attr_name} (w. value {attr}) is invalid. Should be in range (0-2)"
                )
                return False
        return True
