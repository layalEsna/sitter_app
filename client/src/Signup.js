import React from 'react';
import { useFormik } from 'formik';
import { HashRouter, useNavigate } from 'react-router-dom'
import * as Yup from 'yup';

function SignupForm() {

    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$/;

    const formik = useFormik({
        initialValues: {
            user_name: '',
            password: '',
            confirm_password: ''
        },
        validationSchema: Yup.object({
            user_name: Yup.string()
                .required('Username is required.')
                .min(5, 'Username must be at least 5 characters long.'),
            password: Yup.string()
                .required('Password is required.')
                .min(8, 'Password must be at least 8 characters long.')
                .matches(passwordPattern, 'Password must be at least 8 characters long and include at least 1 lowercase letter, 1 uppercase letter, and 1 special character (!@#$%^&*).'),
            confirm_password: Yup.string()
                .oneOf([Yup.ref('password'), null], 'Password must match.')
                .required('Confirm password is required.')

        }),

        onSubmit: (values) => {
            fetch('/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'

                },
                body: JSON.stringify(values)
            })
                .then(res => {
                    if (!res.ok) {
                        throw new Error('Failed to signup.')
                    }
                    return res.json()
                })
                .then(data => console.log(data))
                .catch(e => console.error('Network or server error', e))

        }


    })
    return (
        <div>
            <h1>Create an Acount</h1>

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
                <div>
                    <label htmlFor='confirm_password'>confirm password</label>
                    <input
                        id='confirm_password'
                        name='confirm_password'
                        type='password'
                        value={formik.values.confirm_password}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}

                    />
                    {formik.errors.confirm_password && formik.touched.confirm_password && (
                        <div>{formik.errors.confirm_password}</div>
                    )}
                </div>
                <br />
                <div><button type='submit'>signup</button></div>

            </form>
        </div>
    )

}

export default SignupForm

