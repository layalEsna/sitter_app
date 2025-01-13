import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import SignupForm from './Signup';
import LoginForm from './Login';

function App() {
    return (
        <BrowserRouter> {/* Use BrowserRouter to wrap your app */}
            <div>
                <h1>Hello, React!</h1>
                <Routes>
                    <Route path="/signup" element={<SignupForm />} />
                    <Route path="/login" element={<LoginForm/>} />
                </Routes>
            </div>
        </BrowserRouter>
    );
}

export default App;
