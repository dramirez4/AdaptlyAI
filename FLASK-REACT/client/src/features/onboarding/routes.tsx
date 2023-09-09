import {
  Route,
} from "@tanstack/react-router";
import { baseRoute } from "../../routes";
import { Page1 } from "./pages";

const onboardingRoute = new Route({
  path: `app/onboarding`,
  getParentRoute: () => baseRoute,
  component: Page1,
});

export default onboardingRoute;
