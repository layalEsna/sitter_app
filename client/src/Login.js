import React from 'react';
import { useFormik } from 'formik';
import { HashRouter, useNavigate } from 'react-router-dom'
import * as Yup from 'yup';

function LoginForm() {
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$/;

    const formik = useFormik({
        initialValues: {
            user_name: '',
            password: ''
        },
        validationSchema: Yup.object({
            user_name: Yup.string()
                .required('Username is required.')
                .min(5, 'Username must be at least 5 characters long.'),
            password: Yup.string()
                .required('Password is required.')
                .min(8, 'Password must be at least 8 characters long.')
                .matches(passwordPattern, 'Password must be at least 8 characters long and include at least 1 lowercase letter, 1 uppercase letter, and 1 special character (!@#$%^&*).'),
            
        }),

        onSubmit: (values) => {
            fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'

                },
                body: JSON.stringify(values)
            })
                .then(res => {
                    if (!res.ok) {
                        throw new Error('Failed to login.')
                    }
                    return res.json()
                })
                .then(data => console.log(data))
                .catch(e => console.error('Network or server error', e))

        }


    })
    return (
        <div>
            <h1>Login</h1>

            <form onSubmit={formik.handleSubmit}>
                <div>
                    <label htmlFor='user_name'>username</label>
                    <input
                        id='user_name'
                        name='user_name'
                        type='text'
                        value={formik.values.user_name}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    />
                    {formik.errors.user_name && formik.touched.user_name && (
                        <div>{formik.errors.user_name}</div>
                    )}
                </div>
                <br />
                <div>
                    <label htmlFor='password'>password</label>
                    <input
                        id='password'
                        name='password'
                        type='password'
                        value={formik.values.password}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                    />
                    {formik.errors.password && formik.touched.password && (
                        <div>{formik.errors.password}</div>
                    )}
                </div>
                <br />
                
                <div><button type='submit'>login</button></div>

            </form>
        </div>
    )

}

export default LoginForm

