import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { update_profile } from '../../../actions/profile';
import { delete_account } from '../../../actions/auth';

const UserProfile = ({
    delete_account,
    update_profile,
    first_name_global,
    last_name_global,
    email_global
}) => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: ''
    });

    const { first_name, last_name, email } = formData;

    useEffect(() => {
        setFormData({
            first_name: first_name_global,
            last_name: last_name_global,
            email: email_global
        });
    }, [first_name_global]);

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();

        update_profile(first_name, last_name, email); 
    };

    return (
        <div className='container'>
            <h1 className='mt-3'>User Profile Page</h1>
            <p className='mt-3 mb-3'>Update your user profile below:</p>
            <form onSubmit={e => onSubmit(e)}>
                <div className='form-group'>
                    <label className='form-label' htmlFor='first_name'>First Name</label>
                    <input
                        className='form-control'
                        type='text'
                        name='first_name'
                        placeholder={`${first_name_global}`}
                        onChange={e => onChange(e)}
                        value={first_name}
                    />
                </div>
                <div className='form-group'>
                    <label className='form-label mt-3' htmlFor='last_name'>Last Name</label>
                    <input
                        className='form-control'
                        type='text'
                        name='last_name'
                        placeholder={`${last_name_global}`}
                        onChange={e => onChange(e)}
                        value={last_name}
                    />
                </div>
                <div className='form-group'>
                    <label className='form-label mt-3' htmlFor='email'>Email</label>
                    <input
                        className='form-control'
                        type='text'
                        name='email'
                        placeholder={`${email_global}`}
                        onChange={e => onChange(e)}
                        value={email}
                    />
                </div>
                <button className='btn btn-primary mt-3' type='submit'>Update Profile</button>
            </form>
            <p className='mt-5'>
                Click the button below to delete your user account:
            </p>
            <a
                className='btn btn-danger'
                href='#!'
                onClick={delete_account}
            >
                Delete Account
            </a>
        </div>
    )
};

const mapStateToProps = state => ({
    first_name_global: state.profile.first_name,
    last_name_global: state.profile.last_name,
    email_global: state.profile.email,
});

export default connect(mapStateToProps, { 
    delete_account,
    update_profile
 })(UserProfile);