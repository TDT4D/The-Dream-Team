export type DragID = {
  columnId: number;
  cardId?: number;
};

export type DragAreaStyle = {
  backgroundColor?: string;
  border?: string;
};

export type ParsedDragIDs = {
  dragging: DragID;
  target?: DragID;
};
