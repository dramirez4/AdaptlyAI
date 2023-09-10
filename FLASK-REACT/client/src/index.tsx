import React from "react";
import ReactDOM from "react-dom/client";
import { MantineProvider } from "@mantine/core";
import { RouterProvider, Router } from "@tanstack/react-router";
import { routeTree } from "./routes";
import TanStackRouterDevtools from "./components/TanStackRouterDevtools";

// Create the router using your route tree
const router = new Router({ routeTree });

// Register your router for maximum type safety
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

const rootElement = document.getElementById("root");
if (rootElement && !rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <MantineProvider>
        <RouterProvider router={router} />
        <TanStackRouterDevtools router={router} />
      </MantineProvider>
    </React.StrictMode>,
  );
} else {
  console.error("Expected element to be exist and be empty", { rootElement });
}
