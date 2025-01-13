import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import SignupForm from './Signup';

function App() {
    return (
        <BrowserRouter> {/* Use BrowserRouter to wrap your app */}
            <div>
                <h1>Hello, React!</h1>
                <Routes>
                    <Route path="/" element={<SignupForm />} />
                    {/* Add other routes here */}
                </Routes>
            </div>
        </BrowserRouter>
    );
}

export default App;
