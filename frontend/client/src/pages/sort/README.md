# Contents
This folder contains the code that defines the sort page.

## sort.page.scss
The page's styling.

## sort.page.tsx
The page reactive component.

## drag-helpers.ts
Contains all the helper functions used in handling dragging of student cards and drag events etc.

## label-helpers.ts
Contains all the helper functions used in updating each student's labels.

## score-helpers.ts
Contains the function that fetches the scores for the given project and adds this to each student object.

## sorting.ts
Contains a function that returns another function that can be used to sort students. The returned function is determined by the given sort method.

## students-to-columns.ts
Contains two functions that both basically turn the input Student[] into StudentWithLocation[]. Essentially this means that these set the locations (column and row) for each applicant. One function just does the initial settins aka. sets each applicant to the "Selected" column and the second function sets each applicant to the column based on the returned output of the machine learning model.