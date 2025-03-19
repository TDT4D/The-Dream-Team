export const enum LabelType {
    Applied,
    Selected
}

export type LabelContent = {
    content: string
}

export type Label = {
    isType: LabelType
    contains: LabelContent
}