import TestPage from "./features/Index";
import QueryPage from "./features/query/QueryPage";
import SlideshowPage from "./features/slides/SlideshowPage";
import { Route, RootRoute } from "@tanstack/react-router";
import onboardingRoute from "./features/onboarding/routes";

// Create a root route
export const baseRoute = new RootRoute();

export const indexRoute = new Route({
  getParentRoute: () => baseRoute,
  path: "/",
  component: TestPage,
});

export const queryRoute = new Route({
  getParentRoute: () => baseRoute,
  path: "/app/query",
  component: QueryPage,
});

export const slidesRoute = new Route({
  getParentRoute: () => baseRoute,
  path: "/app/slides",
  component: SlideshowPage,
});

// Create the route tree using your routes
export const routeTree = baseRoute.addChildren([indexRoute, onboardingRoute, queryRoute, slidesRoute]);
