import {
  Route,
} from "@tanstack/react-router";
import { baseRoute } from "../../routes";
import { Page1 } from "./pages";

const pages = [Page1] as const

const onboardingRoutes = pages.map((p, i) => new Route({
  path: `app/onboarding/${i+1}`,
  getParentRoute: () => baseRoute,
  component: p,
}));

export default onboardingRoutes;
