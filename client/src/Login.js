import React, { useState } from 'react';
import { useFormik } from 'formik';
import { useNavigate } from 'react-router-dom'
import * as Yup from 'yup';

function LoginForm() {
    const [errorMessage, setErrorMessage] = useState('')
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$/;
    const navigate = useNavigate()
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
                .then((res) => {
                    if (!res.ok) {
                        return res.json().then(e => {
                            throw new Error(e.error || 'Failed to loginn.')
                        })

                    }
                    return res.json()
                })

                .then(data => {
                    // console.log('Server response:', data)
                    if (data.message === "Successful login.") {
                        // console.log('Redirecting to sitters...')
                        navigate('/sitters');
                    } else {
                        setErrorMessage(data.error || 'Login failed.');
                    }


                    // console.log('Server response:', data); // Log server response
                    // if (data.success) {
                    //     navigate('/sitters'); // Redirect if login is successful
                    // } else {
                    //     setErrorMessage(data.error || 'Login failed.');
                    // }
                    //     if (data.success) {
                    //         console.log('Server response:', data)

                    //         navigate('/sitters')

                    //     } else {
                    //         setErrorMessage(data.error || 'Login failed')

                    // }
                })

                .catch(e => {
                    setErrorMessage(e.message)
                    console.error('Network or server error', e)
                })
        }
    })

    return (
        <div>
            <h1>Login</h1>
            {errorMessage && <div className='error'>{errorMessage}</div>}

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
                        <div className='error'>{formik.errors.user_name}</div>
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
                        <div className='error'>{formik.errors.password}</div>
                    )}
                </div>
                <br />

                <div><button type='submit'>login</button></div>

            </form>









        </div>
    )





}

export default LoginForm

