import React from "react";
import { render } from "react-dom";

import Header from "./Header";

export default function App() {
    return <Header />;
}

const container = document.getElementById("app");
render(<App />, container);
