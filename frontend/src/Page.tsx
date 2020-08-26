import React from "react";
import App from "./App";

export default function Page() {
    return (
        <>
            <div className="navbar">
                <span className="brand">Classful</span>
            </div>
            <App />
            <footer>
                <p>
                    Made with &hearts; by <a href="https://tomn.me">@lecafard</a><br/>
                    Heavily inspired by <a href="https://tutorifull.chybby.com/">Tutorifull</a><br/>
                    <a href="https://github.com/lecafard/classful">Source</a>
                </p>
            </footer>
        </>
    );
}
