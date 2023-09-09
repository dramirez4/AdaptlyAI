import TestPage from "./features/Index";
import { Route, RootRoute } from "@tanstack/react-router";
import onboardingRoutes from "./features/onboarding/routes";

// Create a root route
export const baseRoute = new RootRoute();

export const indexRoute = new Route({
  getParentRoute: () => baseRoute,
  path: "/",
  component: TestPage,
});

baseRoute.addChildren(onboardingRoutes);


// Create the route tree using your routes
export const routeTree = baseRoute.addChildren([indexRoute, ...onboardingRoutes]);
