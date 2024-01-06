import React, { Fragment } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { connect } from 'react-redux';
import { logout } from '../actions/auth';

const navbar = ({ isAuthenticated, logout }) => {
    const authLinks = (
        <Fragment>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/dashboard'>Dashboard</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/stockportfolio'>StockPortfolio</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/portfolio'>Portfolio</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/watchlistitems'>Watchlist Items</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/addwatchlistitem'>Add watchlist item</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/userprofile'>User Profile</NavLink>
            </li>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/' onClick={logout}>Logout</NavLink>
            </li>
        </Fragment>
    );

    const guestLinks = (
        <Fragment>
            <li className='nav-item'>
                <NavLink className='nav-link' to='/login'>Login</NavLink>
            </li>
        </Fragment>
    );

    return (
        <nav className='navbar navbar-expand-lg navbar-light bg-light'>
            <div className='container-fluid'>
                <Link className='navbar-brand' exact to='/'>AO Investments</Link>
                <button 
                    className='navbar-toggler' 
                    type='button' 
                    data-bs-toggle='collapse' 
                    data-bs-target='#navbarNav' 
                    aria-controls='navbarNav' 
                    aria-expanded='false' 
                    aria-label='Toggle navigation'
                >
                    <span className='navbar-toggler-icon'></span>
                </button>
                <div className='collapse navbar-collapse' id='navbarNav'>
                    <ul className='navbar-nav'>
                        { isAuthenticated ? authLinks : guestLinks }
                    </ul>
                </div>
            </div>
        </nav>
    );
};

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(navbar);