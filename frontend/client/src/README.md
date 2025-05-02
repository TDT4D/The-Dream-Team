# Application structure

The application is a simple SPA (single page application) built using React functional components and Vite. The application functionality has been loosely separated into four main categories:
 - [Components](./components/)
 - [Pages](./pages/)
 - [Providers](./providers/)
 - [Services](./services/)

In short the application uses client side routing to host different pages, which in turn can consist of different components. These components may require access to some shared state etc. and thus we wrap all these pages within our providers (React contexts). Finally all functionality not immideatly related to a specific part of the UI is moved to it's own file or "service", which can then be used by multiple different components, pages or providers.

Finally to also ease the communication between all different parts, all common types have been listed and defined under [/types](./types/).

The root of the whole application is contained in [App.tsx](App.tsx). Here we nest all our providers within each other and render the routes (Pages) within these contexts. This application is then combined with [index.scss](./index.scss) (contains all the global styles) in [main.tsx](./main.tsx) to render the application.