import TestPage from "./features/Index";
import QueryPage from "./features/query/QueryPage";
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

// Create the route tree using your routes
export const routeTree = baseRoute.addChildren([indexRoute, onboardingRoute, queryRoute]);
