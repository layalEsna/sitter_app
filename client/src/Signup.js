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
        
        // onSubmit: (values) => {
        //     fetch('/signup', {
        //         method: 'POST',
        //         headers: {
        //             'Content-Type': 'application/json'

        //         },
        //         body: JSON.stringify(values)
        //     })
        //         .then(res => {
        //             if (!res.ok) {
        //                 throw new Error('Failed to signup.')
        //             }
        //             return res.json()
        //         })
        //         .then(data => console.log(data))
        //         .catch(e => console.error('Network or server error', e))

        // }

         
    })

}

export default SignupForm

// "Add Formik validation schema and initial values for signup form."
// Implement onSubmit function with fetch request for signup

// "Implement onSubmit function with fetch request to handle signup form submission."